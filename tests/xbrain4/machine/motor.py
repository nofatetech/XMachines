import os
import logging
from abc import ABC, abstractmethod
from lifecycle import Lifecycle

# Attempt to import gpiozero, but don't fail if it's not available.
# This allows the simulation to run on systems without GPIO hardware or libraries.
try:
    from gpiozero import Motor
except ImportError:
    logging.warning("⚠️ [MOTOR] gpiozero library not found. GPIO motor control will not be available.")
    Motor = None

def clamp(v, lo=-1.0, hi=1.0):
    """Clamps a value to the specified range [-1.0, 1.0]."""
    return max(lo, min(hi, v))

class AbstractMotorController(ABC):
    """Abstract base class for all motor controllers."""
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def drive(self, linear: float, angular: float):
        """Drives the machine with a given linear and angular velocity."""
        pass

    @abstractmethod
    def stop(self):
        """Stops all motor activity."""
        pass

class SimulatedTankMotorController(AbstractMotorController):
    """
    A motor controller for simulated environments.
    It calculates motor speeds and logs them.
    """
    def drive(self, linear: float, angular: float):
        if self.state.lifecycle != Lifecycle.ACTIVE:
            return

        left = clamp(linear - angular)
        right = clamp(linear + angular)
        logging.info(f"🕹️  [MOTOR] SIMULATED: LEFT={left:.2f} RIGHT={right:.2f}")

    def stop(self):
        logging.info("🛑 [MOTOR] SIMULATED: STOP")

class GPIOTankMotorController(AbstractMotorController):
    """
    A motor controller that interfaces with real hardware via GPIO pins.
    Uses the gpiozero library to control two motors.
    """
    def __init__(self, state):
        super().__init__(state)
        if Motor is None:
            raise ImportError("Cannot initialize GPIOTankMotorController: gpiozero library is required.")
        
        try:
            # Get pin numbers from environment variables
            left_fwd_pin = int(os.getenv("LEFT_MOTOR_FORWARD_PIN"))
            left_bwd_pin = int(os.getenv("LEFT_MOTOR_BACKWARD_PIN"))
            right_fwd_pin = int(os.getenv("RIGHT_MOTOR_FORWARD_PIN"))
            right_bwd_pin = int(os.getenv("RIGHT_MOTOR_BACKWARD_PIN"))

            self.left_motor = Motor(forward=left_fwd_pin, backward=left_bwd_pin)
            self.right_motor = Motor(forward=right_fwd_pin, backward=right_bwd_pin)
            logging.info("✅ [MOTOR] GPIO controller initialized.")

        except (ValueError, TypeError) as e:
            logging.error(f"❌ [MOTOR] ERROR: Invalid GPIO pin configuration in environment variables. {e}")
            raise ValueError("Could not initialize GPIO motors due to missing or invalid pin configuration.") from e

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
        logging.info("🛑 [MOTOR] GPIO: STOP")

class NullMotorController(AbstractMotorController):
    """A motor controller that does nothing. Used for machines without motors."""
    def drive(self, linear: float, angular: float):
        pass # Do nothing

    def stop(self):
        pass # Do nothing
