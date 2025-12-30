import time
import os
from dotenv import load_dotenv

# Load environment variables first (specific to this machine instance)
load_dotenv()

# Setup logging before importing other modules that might log
from machine.utils.logging_config import setup_logging
setup_logging()

import logging
import threading

from machine.core.state import MachineState
from machine.core.lifecycle import Lifecycle
from machine.nodes.tank_motor import SimulatedTankMotorController, DCTankMotorController, StepperTankMotorController, NullMotorController, AbstractTankMotorController
from machine.nodes.robotic_arm import SimulatedRoboticArmController, GPIORoboticArmController, AbstractRoboticArmController, NullRoboticArmController

from machine.udp_comm import UDPServer # UDP server is a node that also manages other nodes
from machine.services.api_service import APIService
from machine.services.heartbeat_service import HeartbeatService
# from machine.tui import MachineTUI

def create_motor_controller(state: MachineState) -> AbstractTankMotorController:
    """Factory function to create the appropriate motor controller based on configuration."""
    execution_mode = os.getenv("EXECUTION_MODE", "simulation").lower()
    motor_type = os.getenv("MOTOR_TYPE", "none").lower()

    if execution_mode == "simulation":
        logging.info(f"🕹️  [MACHINE1] Using SimulatedTankMotorController (mimicking '{motor_type}')")
        return SimulatedTankMotorController(state, motor_type=motor_type)
    
    elif execution_mode == "real":
        logging.info(f"🤖 [MACHINE1] Using REAL hardware controller for motor type: '{motor_type}'")
        if motor_type == "dc":
            return DCTankMotorController(state)
        elif motor_type == "stepper":
            return StepperTankMotorController(state)
        elif motor_type == "none":
            return NullMotorController(state)
        else:
            raise ValueError(f"Invalid MOTOR_TYPE for real execution: {motor_type}")
    
    else:
        raise ValueError(f"Invalid EXECUTION_MODE: {execution_mode}")

def create_arm_controller(state: MachineState) -> AbstractRoboticArmController:
    """Factory function to create the appropriate arm controller."""
    execution_mode = os.getenv("EXECUTION_MODE", "simulation").lower()
    arm_type = os.getenv("ARM_TYPE", "none").lower()

    if execution_mode == "simulation":
        logging.info(f"🦾 [MACHINE1] Using SimulatedRoboticArmController (mimicking '{arm_type}')")
        return SimulatedRoboticArmController(state, arm_type=arm_type)

    elif execution_mode == "real":
        logging.info(f"🦾 [MACHINE1] Using REAL hardware controller for arm type: '{arm_type}'")
        if arm_type == "gpio":
            return GPIORoboticArmController(state)
        elif arm_type == "none":
            return NullRoboticArmController(state)
        else:
            raise ValueError(f"Invalid ARM_TYPE for real execution: {arm_type}")
    
    else:
        raise ValueError(f"Invalid EXECUTION_MODE: {execution_mode}")



# --- Main Execution ---
if __name__ == "__main__":
    logging.info("Starting Machine 1 Application...")
    # --- Initialization ---
    machine_id = os.getenv("MACHINE_ID", "machine-001")
    state = MachineState(machine_id=machine_id)

    # Initialize nodes
    motor_controller = create_motor_controller(state)
    arm_controller = create_arm_controller(state)

    udp_server = UDPServer(state)
    udp_server.register_command("drive", motor_controller.drive)
    if not isinstance(arm_controller, NullRoboticArmController):
        udp_server.register_command("set_pose", arm_controller.set_pose)

    # Start nodes (if they have active components like UDP server poll loop)
    # UDP server runs its own internal loop and manages command dispatch to motor/arm
    
    # Initialize services
    api_service = APIService(state)
    heartbeat_service = HeartbeatService(state)

    # Start services
    api_service.start()
    heartbeat_service.start()

    state.lifecycle = Lifecycle.IDLE
    logging.info(f"Machine {state.machine_id} is in {state.lifecycle.value} state.")

    # Main application loop for nodes that need continuous updates
    # UDP server has its own internal thread, so we manage its poll here
    # In a more complex system, this loop would iterate over a list of active nodes
    # and call their .update() method. For now, we manually poll the UDP server.
    try:
        udp_server.start() # This starts the UDP polling loop in a new thread
        while state.lifecycle != Lifecycle.SHUTDOWN:
            time.sleep(0.1) # Small sleep to prevent busy-waiting
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Shutting down Machine 1...")
    finally:
        logging.info("Initiating graceful shutdown of Machine 1.")
        udp_server.stop() # Stop the UDP server's thread
        api_service.stop()
        heartbeat_service.stop()
        state.lifecycle = Lifecycle.SHUTDOWN
        logging.info("Machine 1 application shut down.")
