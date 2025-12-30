# Running a Machine Application

This guide explains the project's architecture and provides step-by-step instructions for running a custom machine application, such as `machine1`.

## Core Architecture

The project is divided into two main parts:

1.  **`/machine` (The Core Framework):** This is a reusable Python package containing the fundamental building blocks for creating distributed machine control systems. It includes:
    *   **Core Abstractions (`/machine/core`):** Defines the base classes for `Nodes` (hardware interfaces) and `Services` (background processes).
    *   **Base Nodes (`/machine/nodes`):** A library of standard, reusable nodes like `TankMotorController` and `RoboticArmController`.
    *   **Core Services (`/machine/services`):** Common services like the `APIService` (FastAPI server) and a generic `UDPServer` for command dispatch.

2.  **`/machine1` (A Custom Application):** This directory represents a specific, physical machine (e.g., an RC car). It consumes the `/machine` framework and assembles the components required for its unique configuration.
    *   **`main.py`:** The primary entry point for this specific machine. It initializes the state, creates the necessary nodes (e.g., a motor controller), and registers them with the appropriate services.
    *   **`.env`:** The specific configuration for this machine, including which nodes to use and their GPIO pin assignments.
    *   **`/nodes`:** A place to define custom nodes that are unique to this machine.

This separation allows for the development of a robust, common framework while keeping each machine's implementation clean, isolated, and easy to manage.

## How to Run the `machine1` RC Car

Follow these steps to set up and run the `machine1` application.

### 1. Set up the Environment

All commands should be run from the root of the project directory.

First, create a dedicated Python virtual environment for `machine1`:

```bash
python -m venv machine1/.venv
```

Activate the virtual environment:

```bash
source machine1/.venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r machine1/requirements.txt
```

Finally, create your local configuration file from the example template:

```bash
cp machine1/.env.example machine1/.env
```

### 2. Configure the Machine

Edit the `machine1/.env` file to match your hardware setup.

*   **For Simulation:** To run without any physical hardware, ensure the `MOTOR_CONTROLLER` is set to `"simulation"`.

    ```
    MOTOR_CONTROLLER="simulation"
    ARM_CONTROLLER="none" # Or "simulation" if you are testing an arm
    ```

*   **For a Real DC Motor:** To control a physical robot, set the `MOTOR_CONTROLLER` to `"dc"` and provide the correct GPIO pin numbers for your motor driver HAT or board.

    ```
    MOTOR_CONTROLLER="dc"

    # Example for DC Motors (gpiozero Motor)
    LEFT_MOTOR_FORWARD_PIN=17
    LEFT_MOTOR_BACKWARD_PIN=18
    RIGHT_MOTOR_FORWARD_PIN=27
    RIGHT_MOTOR_BACKWARD_PIN=22
    ```

### 3. Run the Machine Application

Execute the main entry point for `machine1`:

```bash
python machine1/main.py
```

The application will start, and you will see log messages in your terminal indicating that the API service, UDP server, and other components are running.

### 4. Control the Machine

With the machine application running, open a **new, separate terminal** to run a controller script.

*   **Keyboard Control:**
    ```bash
    python control/controller_keyboard.py
    ```
    Use the `W/A/S/D` keys to drive the machine.

*   **Joystick/Gamepad Control:**
    *(Requires `pygame` to be installed in the environment you run the controller from).*
    ```bash
    python control/controller_pygame.py
    ```
    Use the joystick to control the machine's movement.

The controller script will send UDP commands to the machine application. You will see the simulated motors react in the logs, or your physical motors will move if you have configured them.
