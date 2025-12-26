import os
import logging
from abc import ABC, abstractmethod
from state import MachineState

# Attempt to import gpiozero, but don't fail if it's not available.
try:
    from gpiozero import Servo
    from gpiozero.pins.pigpio import PiGPIOFactory
except ImportError:
    logging.warning("⚠️ [ARM] gpiozero library not found. GPIO arm control will not be available.")
    # Define dummy classes so the rest of the file can be parsed
    class Servo: pass
    class PiGPIOFactory: pass

def clamp(v, lo, hi):
    """Clamps a value to a specified range."""
    return max(lo, min(hi, v))

class AbstractArmController(ABC):
    """Abstract base class for all arm controllers."""
    def __init__(self, state: MachineState):
        self.state = state

    @abstractmethod
    def set_pose(self, joint1: float, joint2: float, clamp_val: int):
        """Moves the arm to a specific configuration."""
        pass

    @abstractmethod
    def stop(self):
        """Stops all arm activity."""
        pass


class SimulatedArmController(AbstractArmController):
    """
    An arm controller for simulated environments.
    It logs the commanded joint angles and clamp state.
    """
    def set_pose(self, joint1: float, joint2: float, clamp_val: int):
        # Clamp values to a realistic servo range (-90 to 90 degrees)
        j1_angle = clamp(joint1, -90, 90)
        j2_angle = clamp(joint2, -90, 90)
        cl_state = "OPEN" if clamp_val == 1 else "CLOSED"

        # Update state
        self.state.arm_state['joint1'] = j1_angle
        self.state.arm_state['joint2'] = j2_angle
        self.state.arm_state['clamp'] = clamp_val

        logging.info(f"🦾 [ARM] SIMULATED: J1={j1_angle}° J2={j2_angle}° CLAMP={cl_state}")

    def stop(self):
        logging.info("🛑 [ARM] SIMULATED: STOP")


class GPIOArmController(AbstractArmController):
    """
    An arm controller that interfaces with real servo motors via GPIO pins.
    """
    def __init__(self, state: MachineState):
        super().__init__(state)
        if not Servo or not hasattr(Servo, 'value'): # Check if Servo is the real class
            raise ImportError("Cannot initialize GPIOArmController: gpiozero library is required.")

        try:
            # Using pigpio factory for better servo performance
            factory = PiGPIOFactory()

            # Get pin numbers from environment variables
            joint1_pin = int(os.getenv("JOINT1_PIN"))
            joint2_pin = int(os.getenv("JOINT2_PIN"))
            clamp_pin = int(os.getenv("CLAMP_PIN"))
            
            # min_pulse_width and max_pulse_width may need tuning for your specific servos
            self.joint1_servo = Servo(joint1_pin, pin_factory=factory)
            self.joint2_servo = Servo(joint2_pin, pin_factory=factory)
            self.clamp_servo = Servo(clamp_pin, pin_factory=factory)

            logging.info("✅ [ARM] GPIO arm controller initialized.")

        except (ValueError, TypeError, NameError) as e:
            logging.error(f"❌ [ARM] ERROR: Invalid GPIO pin configuration for arm servos. {e}")
            raise ValueError("Could not initialize GPIO arm servos due to missing or invalid pin configuration.") from e

    def set_pose(self, joint1: float, joint2: float, clamp_val: int):
        # Convert degrees (-90 to 90) to servo values (-1 to 1)
        j1_servo_val = clamp(joint1 / 90.0, -1.0, 1.0)
        j2_servo_val = clamp(joint2 / 90.0, -1.0, 1.0)
        
        # Clamp is binary (0 or 1), map to servo min/max
        clamp_servo_val = 1 if clamp_val == 1 else -1

        # Set servo positions
        self.joint1_servo.value = j1_servo_val
        self.joint2_servo.value = j2_servo_val
        self.clamp_servo.value = clamp_servo_val

        # Update state
        self.state.arm_state['joint1'] = joint1
        self.state.arm_state['joint2'] = joint2
        self.state.arm_state['clamp'] = clamp_val

    def stop(self):
        # Detach servos to stop sending pulses and save power
        self.joint1_servo.detach()
        self.joint2_servo.detach()
        self.clamp_servo.detach()
        logging.info("🛑 [ARM] GPIO: Servos detached")
