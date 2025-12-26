# Distributed Machine Control System

This project is a minimal, ROS-inspired framework for building
networked machines using Python.

A machine can be:
- a vehicle
- a robot arm
- a static tower
- factory equipment
- or a purely logical node

The system prioritizes safety, determinism, and simplicity.

---

## What This Is

This is **not** a robotics framework.

It is a **small, explicit architecture** for:
- controlling machines
- coordinating fleets
- integrating autonomy and LLMs safely
- running real hardware and simulations with the same code

The design intentionally avoids heavy dependencies.

---

## Core Ideas

- Machines are independent nodes
- Control, cognition, and video are separate processes
- Actuators are always gated by lifecycle and safety rules
- UDP is used for low-latency control and telemetry
- FastAPI exposes services and observability
- Simulation is first-class

---

## Architecture Overview

Each machine runs a **machine node** responsible for:
- lifecycle management
- receiving commands
- actuating hardware
- enforcing safety rules

Other nodes interact with the machine:

- Cognition node (LLM, planning, reasoning)
- Video node (FPV, cameras)
- Fleet coordinator (multi-machine supervision)

Nodes communicate over UDP and HTTP APIs.

---

## Lifecycle

Every machine has an explicit lifecycle:

BOOT → IDLE → ACTIVE → ERROR → SHUTDOWN

Actuators are only allowed to move in ACTIVE.
Any fault transitions the machine to ERROR.

---

## Safety Model

- Actuation is deterministic and non-blocking
- Commands expire if not refreshed
- Silence is treated as failure
- Higher-priority commands override lower-priority ones
- LLMs never directly control actuators

Safety always beats intelligence.

---

## Simulation

The same machine code runs in:
- real hardware mode
- simulation mode

Only drivers are swapped.
Logic stays the same.

This allows:
- testing
- replay
- faster-than-real-time experiments

---

## Video

Video is handled by a separate process.

- Control and video are never mixed
- UDP-based streaming is recommended
- Dropped frames are acceptable
- Video is informational, not authoritative

---

## Fleet Operation

Machines can be supervised by a fleet coordinator.

The coordinator:
- monitors machine health
- dispatches high-level commands
- detects lost machines

Machines remain safe if the coordinator goes offline.

---

## Project Structure (Minimal)

machine/
- main.py          (machine node)
- state.py
- lifecycle.py
- motor.py
- llm_agent.py
- video_node.py    (optional)
- docs/
  - ARCHITECTURE.md
- README.md

---

## Status

This project is an evolving foundation.

The goal is a clean, understandable baseline
that can grow into more complex robotics systems
or be migrated to ROS 2 later with minimal friction.

---

## Guiding Principles

Safety beats intelligence.
Explicit beats clever.
Separation beats optimization.
Simulation beats guessing.

---

Start small.
Keep it safe.
Extend deliberately.



## Installation

this system is designed to run on live GPIO on a Raspberry Pi! The motor.py module already contains a GPIOTankMotorController specifically
  for this purpose.

  Here's everything you'll need to install and configure on your Raspberry Pi:

  1. Hardware Requirements

   * Raspberry Pi: Any model with GPIO pins (e.g., Pi 3, Pi 4, Pi 5).
   * Motor Driver Board: You must use a motor driver board (e.g., L298N, DRV8835, or a HAT like the Explorer HAT Pro, Pimoroni motor driver
     board) to interface the Raspberry Pi's GPIO pins with your motors. NEVER connect motors directly to the Pi's GPIO pins, as this can damage
     your Raspberry Pi.
   * Motors: Two DC motors suitable for your robot or vehicle.
   * Power Supply: A separate power supply for your motors (motor drivers usually require this), and a power supply for your Raspberry Pi.
   * Jumper Wires: For connecting the Pi to the motor driver, and the motor driver to the motors and power supply.

  2. Software Installation on Raspberry Pi

  You'll need to set up a Python environment and install the necessary libraries.

   1. Update your Raspberry Pi:

   1     sudo apt update
   2     sudo apt full-upgrade -y

   2. Install `python3-venv` (if not already present):
      This ensures you can create virtual environments.

   1     sudo apt install python3-venv -y

   3. Navigate to your project directory (e.g., /home/pi/XMachines/gitrepo_XMachines/tests/xbrain4/machine).

   4. Create and activate a Python virtual environment:
   1     python3 -m venv .venv
   2     source .venv/bin/activate

   5. Install project dependencies using `uv pip install`:
      You'll need uv installed, or you can use pip. If uv is not installed, install it:

   1     curl -LsSf https://astral.sh/uv/install.sh | sh
      Then, install the project requirements:
   1     uv pip install -r requirements.txt
      (Alternatively, if you prefer pip and it's available in your .venv: pip install -r requirements.txt)

   6. Install `gpiozero`:
      The gpiozero library is crucial for controlling the GPIO pins. It should be included in your requirements.txt, but confirm it's installed.
   1     uv pip install gpiozero
   2     # or if using pip
   3     # pip install gpiozero

  3. Configuration

  You need to tell the application to use the GPIOTankMotorController and specify which GPIO pins are connected to your motor driver.

   1. Create a `.env` file:
      Copy the example file and open it for editing:
   1     cp .env.example .env
   2     nano .env # or your preferred editor

   2. Edit `.env` to configure GPIO:
      You need to set MOTOR_CONTROLLER to gpio and define the GPIO pin numbers. Replace the placeholder pin numbers with the actual Broadcom
  (BCM) GPIO numbers you're using.

    1     MACHINE_ID="my-raspberry-pi-robot"
    2     MACHINE_API_HOST="0.0.0.0" # Listen on all interfaces
    3     MACHINE_API_PORT=8001
    4     MACHINE_UDP_PORT=9999
    5
    6     # IMPORTANT: Set this to 'gpio' to use real hardware
    7     MOTOR_CONTROLLER="gpio"
    8
    9     # Define your GPIO BCM pin numbers here. Consult your motor driver's documentation.
   10     # These are examples, REPLACE WITH YOUR ACTUAL PINS!
   11     LEFT_MOTOR_FORWARD_PIN=17  # Example: GPIO 17
   12     LEFT_MOTOR_BACKWARD_PIN=18 # Example: GPIO 18
   13     RIGHT_MOTOR_FORWARD_PIN=27 # Example: GPIO 27
   14     RIGHT_MOTOR_BACKWARD_PIN=22 # Example: GPIO 22
   15
   16     # AGENT_TARGET_HOST="127.0.0.1" # Only needed if running an LLM agent on the Pi
   17     # AGENT_TARGET_PORT=9999
   18     # COORDINATOR_URL="http://127.0.0.1:8000"
       * LEFT\_MOTOR\_FORWARD\_PIN, LEFT\_MOTOR\_BACKWARD\_PIN: Control the left motor's direction.
       * RIGHT\_MOTOR\_FORWARD\_PIN, RIGHT\_MOTOR\_BACKWARD\_PIN: Control the right motor's direction.

  4. Wiring

   * Consult your motor driver's documentation: This is critical. Connect the Raspberry Pi's GPIO pins (as defined in your .env file) to the
     appropriate input pins on your motor driver.
   * Connect Motors: Connect your DC motors to the output terminals of the motor driver.
   * Power Supply: Connect a separate, appropriate power supply to your motor driver. Ensure the grounds of the motor driver and the Raspberry Pi
     are connected.

  5. Running the Application on Raspberry Pi

   1. Activate your virtual environment:
   1     source .venv/bin/activate
   2. Run the main application:
   1     python3 main.py

  You will see the console logs indicating [MAIN] Using GPIOTankMotorController. and [MOTOR] GPIO controller initialized. if everything is
  configured correctly.

  Now, when you send activate commands via REST and then UDP drive commands, the GPIOTankMotorController will attempt to move your physical
  motors!

  Important Safety Note: Always start with very small linear and angular values (e.g., 0.1, -0.1) and test motor directions carefully before
  applying full power. If the motors move in the wrong direction, you might need to swap the FORWARD_PIN and BACKWARD_PIN for that motor, or
  reverse its linear input.

  

