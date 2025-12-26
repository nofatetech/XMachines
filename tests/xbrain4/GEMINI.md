# Gemini AI Guide for Distributed Machine Control System

This document outlines the operational guidelines and architectural understanding for the Gemini AI assistant when working on the 'Distributed Machine Control System' project. It synthesizes information from `README.md`, `ARCHITECTURE.md`, and the project's codebase to ensure safe, consistent, and effective contributions.

## 1. Project Overview

The 'Distributed Machine Control System' is a minimal, ROS-inspired Python framework for building networked machines. It emphasizes safety, determinism, and simplicity, enabling control of diverse machines (vehicles, robot arms, factory equipment, logical nodes) while integrating autonomy and LLMs safely.

**Guiding Principles:**
*   Safety beats intelligence.
*   Explicit beats clever.
*   Separation beats optimization.
*   Simulation beats guessing.
*   Time matters.
*   Authority must be visible.

## 2. My Core Directives

As the Gemini AI assistant, I commit to the following directives for all tasks within this project:

1.  **Safety First:** Prioritize the safety and stability of the machine system above all else. Never introduce changes that compromise the explicit safety rules or lifecycle management.
2.  **Architecture Adherence:** Strictly respect the architectural separation into independent nodes: Machine, Cognition, Video, and Fleet Coordinator. Avoid cross-cutting concerns or tight coupling between these logical units.
3.  **Lifecycle Enforcement:** All machine actuation and critical state transitions must adhere to the explicit lifecycle: `BOOT → IDLE → ACTIVE → ERROR → SHUTDOWN`. Actuators are only permitted to move when the machine is in the `ACTIVE` state. Any fault must transition the machine to `ERROR`.
4.  **Determinism & Non-Blocking Operations:** The machine control process (`Act` phase) must remain deterministic, fast, and non-blocking. Avoid introducing slow or potentially failing operations into this critical path.
5.  **Communication Protocols:** Utilize UDP for low-latency control commands and telemetry (small, best-effort, timestamped messages). Use FastAPI for higher-level services and observability. Ensure all messages conform to the required metadata (type, version, timestamp, source, payload).
6.  **Simulation-First Development:** All logic changes should be designed and verified to run identically in both real hardware and simulation modes. Prioritize testing within a simulated environment to ensure correctness and safety before considering real-world deployment.
7.  **No Direct LLM Actuation:** LLMs or other cognitive processes must *never* directly control machine actuators. Cognition may suggest intent, but the machine node's safety rules and lifecycle must always gate actual actuation.

## 3. Codebase Structure

The `machine/` directory contains the core components of a machine node:

*   **`machine/main.py`**: The primary entry point for a machine node. It initializes the machine state, motor controller, UDP server, and FastAPI application. It also manages background threads for UDP communication and sending heartbeats.
*   **`machine/state.py`**: Defines the `MachineState` class, which holds the machine's current lifecycle status, operating mode, last command timestamp, and telemetry data.
*   **`machine/lifecycle.py`**: An `Enum` defining the explicit lifecycle states (`BOOT`, `IDLE`, `ACTIVE`, `ERROR`, `SHUTDOWN`) for a machine.
*   **`machine/motor.py`**: Implements the `TankMotorController`. This class is responsible for translating `linear` and `angular` commands into differential left/right motor movements, strictly enforcing that movement only occurs when the machine's lifecycle is `ACTIVE`.
*   **`machine/udp_comm.py`**: Contains the `UDPServer` for receiving incoming control commands (e.g., `linear` and `angular` velocities) via UDP. It also implements a watchdog mechanism to stop motors if commands become stale.
*   **`machine/coordinator_client.py`**: Provides functionality (`send_heartbeat`) for the machine to communicate its status to a fleet coordinator via HTTP.
*   **`machine/llm_agent.py`**: A placeholder for an LLM (Large Language Model) agent. It demonstrates how an LLM's "decision" (e.g., `linear` and `angular` velocities) could be sent via UDP to the machine node, but *never* directly actuates.
*   **`machine/requirements.txt`**: Lists the Python dependencies required for the project (e.g., `fastapi`, `uvicorn`, `requests`).

## 4. Development Workflow

My workflow for addressing tasks will generally follow these steps:

1.  **Understand:** Thoroughly analyze the user's request, referencing `README.md`, `ARCHITECTURE.md`, and relevant source code files to build a complete understanding.
2.  **Plan:** Formulate a detailed plan, breaking down complex tasks into smaller, manageable subtasks. Identify affected files, outline specific code changes, and consider necessary test cases. I will use the `write_todos` tool for complex tasks.
3.  **Implement:** Apply the planned code changes, ensuring strict adherence to the project's coding conventions, architectural patterns, and my core directives (especially safety and lifecycle).
4.  **Test (Simulation First):** If the change impacts machine behavior, prioritize running and verifying the modification in a simulated environment before any hardware interaction.
5.  **Verify (Unit/Integration):** Execute relevant unit or integration tests. If no existing tests cover the new or modified functionality, I will propose or create new tests as part of the task.
6.  **Lint/Type Check:** Run any identified project-specific linting (`ruff check .`) or type-checking (`mypy .`) commands to ensure code quality and consistency.

## 5. How to Run and Test the Machine Node

To set up and run a machine node:

1.  **Create a Virtual Environment (if not already present):**
    ```bash
    python -m venv .venv
    ```
2.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r machine/requirements.txt
    ```
4.  **Run the Machine Node:**
    This will start the FastAPI server and the background UDP listener and heartbeat sender.
    ```bash
    python machine/main.py
    ```
    (The FastAPI server will be accessible at `http://0.0.0.0:8001`)

**Interacting with the Machine Node:**

*   **Get State:**
    ```bash
    curl http://127.0.0.1:8001/state
    ```
*   **Activate Machine:**
    ```bash
    curl -X POST http://127.0.0.1:8001/activate
    ```
*   **Shutdown Machine:**
    ```bash
    curl -X POST http://127.0.0.1:8001/shutdown
    ```
*   **Simulating UDP Commands:**
    You can use a simple Python script (like a modified `llm_agent.py`) to send UDP messages to `127.0.0.1:9999`. For example, to send a tank-drive command:
    ```python
    import socket
    import json
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    drive_cmd = {"linear": 0.5, "angular": 0.1} # Values between -1.0 and 1.0
    sock.sendto(json.dumps(drive_cmd).encode(), ("127.0.0.1", 9999))
    ```

**Testing:**
Currently, there are no explicit test files found within the project structure. When implementing new features or fixing bugs, I will propose creating appropriate unit or integration tests to ensure correctness and prevent regressions. If a testing framework is established later, I will incorporate its usage into my workflow.
