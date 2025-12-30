# Machine Application: `machine1`

This directory contains the code and configuration for a specific machine application that uses the core `/machine` framework.

## Running the Stepper Motor RC Car

This application is pre-configured to run a tank-drive RC car using stepper motors.

### 1. Set up the Environment

Ensure you have created and activated the virtual environment and installed the requirements as described in the main `docs/running_a_machine.md` guide.

### 2. Configure for Stepper Motors

Copy the pre-made stepper motor environment file to `.env`:

```bash
cp machine1/.env.stepper_tank machine1/.env
```

Next, **edit `machine1/.env`** and set the correct GPIO pin numbers for your specific stepper motor driver board.

### 3. Run the Application

Launch the machine application:

```bash
python machine1/main.py
```

### 4. Drive the Car

In a new terminal, use one of the controller scripts to send drive commands:

```bash
# For keyboard control
python control/controller_keyboard.py

# For joystick/gamepad control
python control/controller_pygame.py
```
