import os
import logging
from abc import ABC, abstractmethod

from machine.core.node import AbstractNode
from machine.state import MachineState
from machine.lifecycle import Lifecycle

# Attempt to import gpiozero, but don't fail if it's not available.
# This allows the simulation to run on systems without GPIO hardware or libraries.
try:
    from gpiozero import Motor, PWMOutputDevice, DigitalOutputDevice
except ImportError:
    logging.warning("⚠️ [MOTOR] gpiozero library not found. GPIO motor control will not be available.")
    # Define dummy classes so the rest of the file can be parsed
    class Motor: pass
    class PWMOutputDevice: pass
    class DigitalOutputDevice: pass

def clamp(v, lo=-1.0, hi=1.0):
    """Clamps a value to the specified range [-1.0, 1.0]."""
    return max(lo, min(hi, v))

class AbstractTankMotorController(AbstractNode):
    """Abstract base class for all tank motor controllers."""
    def __init__(self, state: MachineState):
        super().__init__(state)
        self.log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def drive(self, linear: float, angular: float):
        """Drives the machine with a given linear and angular velocity."""
        pass
    
    def start(self):
        self.log.info("Tank Motor Controller started.")

    def update(self):
        # The drive command is received asynchronously via UDP, so the update loop
        # for motors primarily focuses on safety (e.g., watchdog) rather than active driving.
        # The actual driving is triggered by UDP command reception.
        pass

    def stop(self):
        """Stops all motor activity and cleans up resources."""
        self.log.info("Tank Motor Controller stopped.")

class SimulatedTankMotorController(AbstractTankMotorController):
    """
    A motor controller for simulated environments.
    It calculates motor speeds and logs them.
    """
    def drive(self, linear: float, angular: float):
        if self.state.lifecycle != Lifecycle.ACTIVE:
            return

        left = clamp(linear - angular)
        right = clamp(linear + angular)
        if left != 0 and right != 0.0:
            self.log.info(f"🕹️  SIMULATED: LEFT={left:.2f} RIGHT={right:.2f}")

    def stop(self):
        self.log.info("🛑 SIMULATED: STOP")


class DCTankMotorController(AbstractTankMotorController):
    """
    A motor controller that interfaces with DC motors via GPIO pins.
    Uses the gpiozero library to control two motors.
    """
    def __init__(self, state: MachineState):
        super().__init__(state)
        if not Motor or not hasattr(Motor, 'forward'): # Check if Motor is the real class
            raise ImportError("Cannot initialize DCTankMotorController: gpiozero library is required.")
        
        try:
            # Get pin numbers from environment variables
            left_fwd_pin = int(os.getenv("LEFT_MOTOR_FORWARD_PIN"))
            left_bwd_pin = int(os.getenv("LEFT_MOTOR_BACKWARD_PIN"))
            right_fwd_pin = int(os.getenv("RIGHT_MOTOR_FORWARD_PIN"))
            right_bwd_pin = int(os.getenv("RIGHT_MOTOR_BACKWARD_PIN"))

            self.left_motor = Motor(forward=left_fwd_pin, backward=left_bwd_pin)
            self.right_motor = Motor(forward=right_fwd_pin, backward=right_bwd_pin)
            self.log.info("✅ GPIO DC motor controller initialized.")

        except (ValueError, TypeError) as e:
            self.log.error(f"❌ ERROR: Invalid GPIO pin configuration in environment variables. {e}")
            raise ValueError("Could not initialize GPIO DC motors due to missing or invalid pin configuration.") from e

    def drive(self, linear: float, angular:float):
        if self.state.lifecycle != Lifecycle.ACTIVE:
            return # Do not log, to avoid spamming

        # Tank drive kinematics
        left_speed = clamp(linear - angular)
        right_speed = clamp(linear + angular)

        # Control left motor
        if left_speed > 0:
            self.left_motor.forward(speed=left_speed)
        elif left_speed < 0:
            self.left_motor.backward(speed=abs(left_speed))
        else:
            self.left_motor.stop()

        # Control right motor
        if right_speed > 0:
            self.right_motor.forward(speed=right_speed)
        elif right_speed < 0:
            self.right_motor.backward(speed=abs(right_speed))
        else:
            self.right_motor.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.log.info("🛑 GPIO: STOP")


class StepperTankMotorController(AbstractTankMotorController):
    """
    A motor controller for stepper motors using STEP/DIR signals.
    Uses PWM to control the step frequency (velocity).
    """
    MAX_FREQUENCY = 2000 # Steps per second at max speed

    def __init__(self, state: MachineState):
        super().__init__(state)
        if not PWMOutputDevice or not hasattr(PWMOutputDevice, 'frequency'): # Check if it's the real class
             raise ImportError("Cannot initialize StepperTankMotorController: gpiozero library is required.")

        try:
            # Get pin numbers from environment variables
            left_step_pin = int(os.getenv("LEFT_MOTOR_STEP_PIN"))
            left_dir_pin = int(os.getenv("LEFT_MOTOR_DIR_PIN"))
            right_step_pin = int(os.getenv("RIGHT_MOTOR_STEP_PIN"))
            right_dir_pin = int(os.getenv("RIGHT_MOTOR_DIR_PIN"))

            self.left_dir = DigitalOutputDevice(left_dir_pin)
            self.right_dir = DigitalOutputDevice(right_dir_pin)

            # Use PWM to generate step pulses
            self.left_step = PWMOutputDevice(left_step_pin)
            self.right_step = PWMOutputDevice(right_step_pin)
            
            self.log.info("✅ GPIO stepper motor controller initialized.")

        except (ValueError, TypeError) as e:
            self.log.error(f"❌ ERROR: Invalid GPIO pin configuration for stepper motors. {e}")
            raise ValueError("Could not initialize GPIO stepper motors due to missing or invalid pin configuration.") from e

    def drive(self, linear: float, angular: float):
        if self.state.lifecycle != Lifecycle.ACTIVE:
            return

        left_speed = clamp(linear - angular)
        right_speed = clamp(linear + angular)

        # Set direction
        # Note: The mapping of value (0/1) to direction (forward/backward)
        # depends on your specific wiring and motor driver.
        self.left_dir.value = 1 if left_speed < 0 else 0
        self.right_dir.value = 1 if right_speed < 0 else 0

        # Set speed (frequency of step pulses)
        self.left_step.frequency = abs(left_speed) * self.MAX_FREQUENCY
        self.right_step.frequency = abs(right_speed) * self.MAX_FREQUENCY
    
    def stop(self):
        self.left_step.frequency = 0
        self.right_step.frequency = 0
        self.log.info("🛑 GPIO Stepper: STOP")


class NullMotorController(AbstractTankMotorController):
    """A motor controller that does nothing. Used for machines without motors."""
    def drive(self, linear: float, angular: float):
        pass # Do nothing
    
    def stop(self):
        pass # Do nothing
