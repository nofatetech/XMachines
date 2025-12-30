import time
import os
from dotenv import load_dotenv

# Load environment variables first (specific to this machine instance)
load_dotenv()

# Setup logging before importing other modules that might log
from machine.logging_config import setup_logging
setup_logging()

import logging
import threading

from machine.state import MachineState
from machine.lifecycle import Lifecycle
from machine.nodes.tank_motor import SimulatedTankMotorController, DCTankMotorController, StepperTankMotorController, NullMotorController, AbstractTankMotorController
from machine.nodes.robotic_arm import SimulatedRoboticArmController, GPIORoboticArmController, AbstractRoboticArmController, NullRoboticArmController

from machine.udp_comm import UDPServer # UDP server is a node that also manages other nodes
from machine.services.api_service import APIService
from machine.services.heartbeat_service import HeartbeatService
# from machine.tui import MachineTUI

def create_motor_controller(state: MachineState) -> AbstractTankMotorController:
    """Factory function to create the appropriate motor controller based on configuration."""
    # Default to 'simulation' for safety and ease of use.
    controller_type = os.getenv("MOTOR_CONTROLLER", "simulation").lower()
    
    if controller_type == "simulation":
        logging.info("🕹️  [MACHINE1] Using SimulatedTankMotorController.")
        return SimulatedTankMotorController(state)
    elif controller_type == "dc":
        logging.info("🤖 [MACHINE1] Using DC Motor Controller (via GPIO).")
        return DCTankMotorController(state)
    elif controller_type == "stepper":
        logging.info("⚙️ [MACHINE1] Using StepperTankMotorController.")
        return StepperTankMotorController(state)
    elif controller_type == "none":
        logging.info("💨 [MACHINE1] Using NullMotorController.")
        return NullMotorController(state)
    else:
        raise ValueError(f"Invalid MOTOR_CONTROLLER type: {controller_type}")

def create_arm_controller(state: MachineState) -> AbstractRoboticArmController:
    """Factory function to create the appropriate arm controller."""
    controller_type = os.getenv("ARM_CONTROLLER", "none").lower()

    if controller_type == "simulation":
        logging.info("🦾 [MACHINE1] Using SimulatedRoboticArmController.")
        return SimulatedRoboticArmController(state)
    elif controller_type == "gpio":
        logging.info("🦾 [MACHINE1] Using GPIORoboticArmController.")
        return GPIORoboticArmController(state)
    elif controller_type == "none":
        logging.info("🦾 [MACHINE1] Using NullRoboticArmController.")
        return NullRoboticArmController(state)
    else:
        raise ValueError(f"Invalid ARM_CONTROLLER type: {controller_type}")



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
