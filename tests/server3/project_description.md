# XMachines - Autonomous Machine Ecosystem

## Project Overview

XMachines is a modular application designed to serve as the "heart" for intelligent, autonomous machines (e.g., Raspberry Pi-powered RC cars). It provides a flexible architecture where a single codebase can operate in two distinct modes:

1.  **SERVER Mode:** Acts as a central monitoring and control dashboard for a group of "MACHINE" instances.
2.  **MACHINE Mode:** Runs directly on a device, serving as its local brain, managing its internal state, and providing a local display.

This setup allows for the creation of decentralized "groups" of machines, enabling complex interactions while maintaining simplicity at each node.

## Key Technologies & Components

*   **Laravel (PHP):** The core application framework, handling web serving, API endpoints, database management, and event broadcasting.
*   **Laravel Reverb (WebSockets):** Provides real-time, self-hosted WebSocket communication for instant status updates and control commands.
*   **DaisyUI (Tailwind CSS):** Used for a modern, component-based, and visually appealing user interface across all views.
*   **Python (`pi_client.py`):** A client-side script running on devices (like Raspberry Pi) responsible for:
    *   Direct GPIO interaction (sensors, motors, lights).
    *   Sending status updates via HTTP POST to its designated Laravel server.
    *   Listening for control commands via WebSockets.
    *   Local data logging (CSV) for future ML.
*   **Pykka (Actor Model):** The Python client is structured using the actor model to ensure robustness, concurrency, and modularity.
*   **SQLite:** Used as the default local database, particularly suitable for self-contained "MACHINE" instances.

## Core Features Implemented

*   **Real-time Status Monitoring:** Dashboards (in SERVER mode) update instantly via WebSockets with machine telemetry.
*   **Real-time Control:** Commands sent from dashboards are instantly pushed to target machines via WebSockets.
*   **Machine Lifecycle ("Tamagotchi Features"):** Machines possess internal states like `happiness`, `hunger`, and `is_auto_driving`, which evolve through scheduled commands.
*   **Client-Side Offline Detection:** Dashboard UI visually marks machines as "Offline" if no status updates are received within a defined timeout.
*   **Dynamic Routing & UI:** Application behavior and navigation links adapt automatically based on the `APP_MODE` environment variable.
*   **Reusable UI Components:** Machine cards are built as Blade components for consistent branding and easier maintenance.
*   **External API Integration:** Dedicated API endpoint (`/api/machine/{id}/status`) for secure (though initially unauthenticated for simplicity) machine-to-server status reporting.

---

## Future Vision: Reinforcement Learning for True Autonomy

The next major evolution for XMachines is to implement a learning system that allows machines to develop true autonomous behavior. The goal is to replace the placeholder `auto-driving` logic with an intelligent **policy** trained via Reinforcement Learning (RL). This policy will enable the machine to make its own decisions to navigate its environment and maintain its well-being.

### RL Technology Stack

*   **Core Libraries:** `PufferLib` will be used to structure the RL environment, ensuring a clean separation between the environment and the learning algorithm. `PyTorch` will serve as the underlying deep learning framework for training the neural network policy.

### The RL Environment Definition

To teach the machine, we must first define the "game" it is playing.

#### 1. State Space (What the Machine Observes)

The state is a collection of all critical information the machine can perceive about itself and its environment. This includes:
*   **Internal State ("Tamagotchi"):** `happiness`, `hunger`.
*   **Sensor Data:** `temperature`, `motor_left_speed`, `motor_right_speed`.
*   **Environmental Data:** `distance_from_obstacle` (from an ultrasonic or infrared distance sensor).

#### 2. Action Space (What the Machine Can Do)

The machine will have a set of discrete actions it can choose from at any given moment:
*   `0`: **Do Nothing**
*   `1`: **Move Forward** (e.g., set both motors to 50%)
*   `2`: **Turn Left** (e.g., right motor 40%, left motor -40%)
*   `3`: **Turn Right** (e.g., left motor 40%, right motor -40%)

#### 3. Reward Function (How the Machine Learns Good vs. Bad)

The reward function is critical for shaping the machine's behavior. The goal is to maximize the cumulative reward.
*   **Positive Rewards (Incentives):**
    *   `+0.1` for each second `happiness` is above 70.
    *   `+0.1` for each second `hunger` is below 30.
    *   `+0.2` for moving forward when `distance_from_obstacle` is large (encourages exploration).
*   **Negative Rewards (Punishments):**
    *   `-0.5` for each second `hunger` is above 80.
    *   `-10.0` (large penalty) if `distance_from_obstacle` is below a critical threshold (e.g., 5cm), to strongly discourage collisions.

### MLOps Workflow & Phased Implementation Plan

We will adopt a professional MLOps workflow that separates training from on-device execution (inference).

#### Short Term (Phase 1): Architecture & Data Collection
1.  **Integrate Distance Sensor:** The `HeartbeatActor` in `pi_client.py` will be updated to read data from the distance sensor and include it in the status payload.
2.  **Create `RLPolicyActor`:** A new actor will be created in the client. Initially, it will implement a simple, hard-coded policy (e.g., select a random action).
3.  **Rich Data Logging:** The client will log comprehensive state-action pairs to the CSV file. This data is the raw material for training our first model.

#### Mid Term (Phase 2): Offline Training & On-Device Inference (Recommended Approach)
1.  **Create Training Script:** A separate Python script (`train_rl.py`) will be developed to run on a powerful development machine (not the Pi).
2.  **Train the Model:** This script will use PufferLib and PyTorch to load the CSV data collected in Phase 1 and train a policy model.
3.  **Deploy & Infer:** The resulting trained model file (e.g., `policy.pt`) will be deployed to the Raspberry Pi. The `RLPolicyActor` will be updated to load this model and use it to make intelligent, real-time decisions when auto-driving is enabled.

#### Long Term (Phase 3): Exploration of On-Device Learning
While offline training is the most robust and efficient method, the modular architecture being built sets the stage for future experimentation.
*   **Future Possibility:** We can explore advanced techniques like **model distillation** (training a smaller, faster model from a larger one) or **transfer learning** to potentially allow for lightweight model updates or fine-tuning directly on the device. This maintains a path toward greater on-device adaptability without compromising the stability of the core system.

---

## Vibe Check

This project was developed with a "vibe coding" approach, emphasizing iterative development, clear communication, and collaborative problem-solving to build a flexible and functional system.

---

## How to Test

This guide outlines how to test the two primary application modes locally. Both require three separate terminal windows.

### Testing the Server (`APP_MODE=SERVER`)

This tests the central dashboard's ability to monitor a connecting client.

1.  **Configure `.env`:** Ensure your `.env` file is set to `APP_MODE=SERVER`.
    ```ini
    APP_MODE=SERVER
    ```
2.  **Run Processes:**
    *   **Terminal 1 (Web Server):** `php artisan serve`
    *   **Terminal 2 (WebSocket Server):** `php artisan reverb:start`
    *   **Terminal 3 (Simulated Machine):** `python clients/python/pi_client.py`
3.  **Verify:**
    *   Open `http://1227.0.0.1:8000/dashboard` in your browser.
    *   **Observe:** The card for "Machine 1" should appear and switch to "Online" within a few seconds as the Python script sends its first heartbeat.
    *   **Interact:** Click the control buttons on the "Machine 1" card.
    *   **Observe:** Watch Terminal 3 to see the `Received command: ...` messages printed in real-time.

### Testing a Machine (`APP_MODE=MACHINE`)

This tests the on-device display and the machine's ability to run as a self-contained unit.

1.  **Configure `.env`:** Change your `.env` file to `APP_MODE=MACHINE` and specify which machine this instance represents.
    ```ini
    APP_MODE=MACHINE
    MACHINE_ID=1
    ```
2.  **Run Processes:**
    *   **Terminal 1 (Web Server):** `php artisan serve`
    *   **Terminal 2 (WebSocket Server):** `php artisan reverb:start`
    *   **Terminal 3 (Physical Interface):** `python clients/python/pi_client.py`
3.  **Verify:**
    *   Open `http://127.0.0.1:8000/display` in your browser. (Note: not `/dashboard`).
    *   **Observe:** The single card for "Machine 1" should appear. It will switch to "Online" as the local Python client (Terminal 3) sends its heartbeat to the local Laravel server (Terminal 1). The data (temp, motors, etc.) will update every few seconds.
    *   This setup verifies that the machine can operate as its own self-contained "heart" and "brain."
