# ROS-Inspired Fleet System – Main Design Reference
(WebSocket-only, autonomous machines (cars, arms, etc), web-native stack)

---

## Core Intent

- Build a small-vehicle fleet system inspired by ROS concepts
- Avoid ROS tooling, keep web and backend friendly
- Machines are autonomous agents
- Server coordinates intent and visibility
- Safety and reality override everything

---

## Fundamental Principles

- State ≠ Command ≠ Event
- Commands describe desired outcome, not actions
- Machines enforce physics and safety
- Server never micromanages hardware
- UI observes truth, never assumptions
- System must survive:
  - network loss
  - duplicated messages
  - delayed delivery
  - partial failures
  - car reboots

---

## Communication Model

- One persistent WebSocket per car
- JSON messages only
- Server is logical time authority
- Car timestamps local actions
- Sequence numbers used for ordering
- No blocking calls, no request/response coupling

---

## Message Envelope (All Messages)

- type: state | command | event
- car_id: unique identifier
- ts: timestamp (server or local)
- seq: monotonically increasing sequence
- payload: message-specific content

---

## Command Messages (Server → Car)

- Declarative intent
- Idempotent
- May be resent safely
- Never assumed successful

Command fields:
- cmd_id (UUID)
- name (action identifier)
- params (desired end state)

Rules:
- Duplicate cmd_id ignored
- Commands describe target state
- Commands accepted only in valid car states

---

## State Messages (Car → Server)

- Ground truth only
- Published continuously
- Aggregated locally
- Never includes intent

Typical state includes:
- battery level
- speed
- position or encoder data
- lights status
- current mission / step
- health indicators

---

## Event Messages (Car → Server)

- Discrete facts
- Logged permanently
- Severity levels: info, warn, error
- May trigger alerts or state transitions

Used for:
- faults
- safety triggers
- mission lifecycle changes
- diagnostics

---

## Car Internal Architecture

- Node-based design
- One responsibility per node
- Nodes do not call each other directly
- All communication via internal event bus
- Nodes are restartable independently

Typical nodes:
- WebSocket client
- Command router
- Motor controller
- Light controller
- Sensor reader
- State aggregator
- Safety / watchdog node

---

## Internal Event Bus (Car)

- In-memory pub/sub
- Topic-based routing
- Async message passing
- No shared mutable state
- Enables simulation and replay

Benefits:
- Hardware abstraction
- Easy fault injection
- Deterministic testing
- Clean separation of concerns

---

## Fleet State Machine

Car states:
- OFFLINE
- CONNECTING
- IDLE
- ACTIVE
- ERROR

Rules:
- Commands only accepted in IDLE or ACTIVE
- ERROR only accepts reset / recovery commands
- OFFLINE is read-only from server perspective
- State transitions explicitly validated

---

## Safety and Failsafe Design

Safety is local and absolute.

Mandatory behaviors:
- Motor stop on timeout or fault
- Hazard or blink lights on error
- Immediate ERROR state emission
- Events sent before shutdown if possible

Priority order:
- Safety logic
- Motor control
- Command execution
- Server intent

Server cannot override safety decisions.

---

## Watchdogs (Car-Side)

- Command inactivity timeout
- Heartbeat timeout
- Sensor sanity checks
- Power / voltage limits

Failure triggers:
- Safe stop
- ERROR state
- Event emission

---

## Idempotent Command Pattern

- Every command has a unique ID
- Car tracks processed command IDs
- Replayed commands do nothing
- Commands describe final desired state

Design rule:
- Re-sending a command must not change outcome

---

## Fleet-Level Scheduler

Responsibilities:
- Assign missions or commands
- Evaluate car availability and health
- Consider battery and priority
- Never execute hardware logic

Scheduler outputs intent only.

---

## Mission Definitions

- JSON-based DSL
- Versioned
- Step-based
- Interruptible
- Resume-capable

Execution:
- Parsed locally by car
- Progress reported via state/events
- Abortable at any time

---

## Simulation Mode

- Fake cars use identical protocol
- Same message schemas
- Same state machine
- Same timing constraints

Simulates:
- latency
- packet loss
- battery drain
- random faults

Rule:
- If it works in simulation, it works IRL

---

## Replay and Time-Travel Debugging

- Log all commands, states, events
- Deterministic replay of timelines
- Reproduce bugs reliably
- Post-mortem analysis of failures
