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
