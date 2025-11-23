# Smart Vehicle Control Server

This project serves as a comprehensive backend system for managing and remotely controlling smart vehicles. Built on the Laravel PHP framework, it provides a robust platform for real-time interaction, data management, and operational control of a fleet of intelligent vehicles.

## Key Features:

-   **Vehicle Management:** Stores and manages detailed information about each smart vehicle, including unique "tamagotchi attributes" which suggest an advanced state management system for vehicle health, status, and interactive behaviors.
-   **Real-time Communication (MQTT):** Utilizes MQTT (Message Queuing Telemetry Transport) for low-latency, real-time bidirectional communication with vehicles. This enables:
    -   Remote command and control of vehicle functions.
    -   Reception of live vehicle status updates and telemetry data.
-   **Event-Driven Architecture:** Employs Laravel's event system to react to vehicle status changes and other critical events, facilitating responsive and scalable operations.
-   **Console Commands:** Includes dedicated console commands for essential background tasks, such as listening for MQTT messages and managing vehicle "live" states.
-   **External Integrations:**
    -   **Python Scripting:** A `gamepad_mqtt_publisher.py` script suggests an interface for controlling vehicles via MQTT using a gamepad, highlighting flexible control options.
    -   **C++ Components:** The presence of C++ files (`MqttHandler.cpp`, `VehicleControl.cpp`) indicates potential integration with high-performance or hardware-level control modules, possibly for more direct and efficient vehicle operation.

## Technology Stack:

-   **Backend Framework:** Laravel (PHP)
-   **Real-time Messaging:** MQTT
-   **Database:** (Likely MySQL or PostgreSQL, given Laravel's common usage, with migrations defining `vehicles` table and `tamagotchi attributes`)
-   **Frontend:** (Implied by `resources/views`, `public/build`, etc., likely Blade templates with JavaScript/CSS assets)
-   **Supporting Languages:** Python, C++ (for specific functionalities)

## Purpose:

This server acts as the central brain for smart vehicle operations, providing the necessary infrastructure for monitoring, control, and intelligent management of a vehicle fleet. Whether deployed in a central cloud or directly on a vehicle as an embedded server, it forms the core of an autonomous or remotely-operated vehicle system.