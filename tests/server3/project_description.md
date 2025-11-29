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
*   **SQLite:** Used as the default local database, particularly suitable for self-contained "MACHINE" instances.

## Core Features Implemented

*   **Real-time Status Monitoring:** Dashboards (in SERVER mode) update instantly via WebSockets with machine telemetry.
*   **Real-time Control:** Commands sent from dashboards are instantly pushed to target machines via WebSockets.
*   **Machine Lifecycle ("Tamagotchi Features"):** Machines possess internal states like `happiness`, `hunger`, and `is_auto_driving`, which evolve through scheduled commands.
*   **Client-Side Offline Detection:** Dashboard UI visually marks machines as "Offline" if no status updates are received within a defined timeout.
*   **Dynamic Routing & UI:** Application behavior and navigation links adapt automatically based on the `APP_MODE` environment variable.
*   **Reusable UI Components:** Machine cards are built as Blade components for consistent branding and easier maintenance.
*   **External API Integration:** Dedicated API endpoint (`/api/machine/{id}/status`) for secure (though initially unauthenticated for simplicity) machine-to-server status reporting.

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
    *   Open `http://127.0.0.1:8000/dashboard` in your browser.
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
