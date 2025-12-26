# Distributed Machine Architecture

This project implements a distributed control system for machines
(vehicles, towers, robot arms, factory equipment, or purely logical nodes).

It is inspired by ROS concepts but implemented with minimal tooling:
Python, UDP, and FastAPI.

This document is a contract.
Code must follow these rules.

---

## 1. What Is a Machine

A machine is a networked state machine with:

- inputs (commands, intents, sensors)
- internal state
- actuators
- services (API)
- safety rules

A machine may be:
- mobile (cars, drones, rovers)
- semi-static (towers, sensors, cameras)
- static (robot arms, factory cells)
- purely logical (planners, coordinators)

Mobility is optional.

---

## 2. Process Separation (Mandatory)

The system is split into separate processes.

At minimum:

- Machine node (control, actuators, safety)
- Cognition node (LLM, planning, reasoning)
- Video node (camera streaming)
- Fleet coordinator (optional but recommended)

Rules:

- Blocking work must never run in the machine control process
- LLMs never control actuators directly
- If cognition crashes, the machine must remain safe
- If video crashes, control must continue

Cognition may suggest intent.
Only the machine node actuates.

---

## 3. Machine Lifecycle

Every machine has an explicit lifecycle.

States:

- BOOT
- IDLE
- ACTIVE
- ERROR
- SHUTDOWN

Rules:

- Actuators may only move in ACTIVE
- Any fault transitions to ERROR
- Recovery must be explicit
- SHUTDOWN is terminal

Lifecycle gates all actuation.

---

## 4. Determinism Boundaries

Execution is divided into phases:

Sense → Decide → Act

Rules:

- Act must never block
- Decide may be slow or fail
- Sense never trusts Decide blindly
- LLMs only participate in Decide

The Act phase must always be deterministic and fast.

---

## 5. Communication Model

Control and telemetry use UDP.

Characteristics:

- Small messages
- Best-effort delivery
- Timestamped
- Stateless

Dropped packets are acceptable.
Late packets are ignored.

---

## 6. Video and FPV

Video is a separate pipeline.

Rules:

- Video never shares channels with control
- Video uses UDP-based streaming (RTP / H.264 recommended)
- Dropped frames are acceptable
- Control must never depend on video timing

Control decides now.
Video shows the past.

---

## 7. Authority and Arbitration

Every command has a source.

Priority order (highest to lowest):

- Emergency
- Safety
- Human
- Autonomy
- Simulation

Rules:

- Higher priority always wins
- Lower priority commands are ignored
- No implicit overrides
- Arbitration happens before actuation

---

## 8. Watchdogs and Time

Time is part of correctness.

Rules:

- Every command has a timestamp
- Stale commands are ignored
- Missing input is a failure condition
- Silence triggers safe behavior

Fail silent means fail safe.

---

## 9. Simulation Is First-Class

Simulation is not a toy mode.

Rules:

- Real and simulated machines run the same logic
- Only drivers (actuators and sensors) are swapped
- Simulation supports testing, replay, and experimentation

Swap drivers, not logic.

---

## 10. Fleet Architecture

Machines are independent nodes.

A fleet coordinator:

- monitors machine health
- tracks liveness
- dispatches high-level commands
- does not control actuators directly

If the fleet coordinator fails, machines must continue safely.

---

## 11. Message Structure

All messages include metadata.

Required fields:

- type
- version
- timestamp
- source
- payload

Unknown fields must be ignored, not treated as errors.

Message schemas are versioned and forward-compatible.

---

## 12. Failure Philosophy

Assume failure is normal.

Assumptions:

- Networks partition
- Packets drop
- Processes crash
- Machines reboot

Rules:

- Fail safe, not clever
- Explicit recovery
- No hidden state transitions
- Safety beats availability

---

## 13. Security Baseline

Rules:

- Control interfaces are authenticated
- Video streams are not public
- Machines trust as little as possible
- Raw UDP is never exposed directly to the internet

Isolation is preferred over complexity.

---

## 14. ROS Compatibility

This architecture maps directly to ROS 2 concepts.

- Machine node maps to ROS node
- UDP topics map to DDS topics
- FastAPI maps to ROS services
- Lifecycle maps to managed nodes
- Simulation maps to Gazebo-style driver swapping
- Fleet coordinator maps to a supervisor node

Migration to ROS 2 should require minimal redesign.

---

## 15. Guiding Principles

Safety beats intelligence.
Explicit beats clever.
Separation beats optimization.
Simulation beats guessing.
Time matters.
Authority must be visible.

---

End of document.
