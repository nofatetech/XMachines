# Fleet System – Architecture & Tech Specs
(ROS-inspired, WebSocket-only, hardware-agnostic)

---

## 1. High-Level Architecture

- Distributed agent-based system
- Each machine is an autonomous runtime
- Central server coordinates intent and visibility
- No hard dependency between machines
- System tolerates partial failure

---

## 2. Component Breakdown

### machine (Edge Runtime)

- Language: Python
- Framework: FastAPI (async)
- Communication: WebSocket client
- Execution model: async tasks / workers
- Hardware access: GPIO / I2C / UART / USB
- OS: Linux (preferred), RTOS optional

### Fleet Server

- Language: PHP
- Framework: Laravel
- Communication: WebSockets
- Role: orchestration, scheduling, logging
- Persistence: SQL + cache
- Auth & permissions centralized

### Dashboard / UI

- Web-based
- Real-time updates via WebSockets
- Read-only view of machine state
- Command issuing gated by permissions

---

## 3. Communication Model

- One persistent WebSocket per machine
- Server is time authority
- Messages are JSON
- All messages versioned
- All messages timestamped
- Ordering handled via sequence numbers

---

## 4. Message Flow

- machine publishes state periodically
- machine emits events on change or fault
- Server sends declarative commands
- Server never blocks waiting for response
- Command success inferred from state

---

## 5. machine Runtime Design

- Node-based internal structure
- Each node has one responsibility
- Nodes communicate via internal event bus
- Nodes are restartable independently
- Safety node has highest priority

---

## 6. Internal Event Bus

- In-memory pub/sub
- Topic-based routing
- Async message passing
- No shared state between nodes
- Supports simulation and replay

---

## 7. State Management

- State is aggregated locally on the machine
- Server caches latest known state
- UI reads state, never commands
- Historical state stored for replay

---

## 8. Fleet State Machine

- Server tracks logical machine state
- machine tracks physical state
- Server state may be stale
- machine state is authoritative for safety

---

## 9. Scheduler

- Stateless or lightly stateful
- Evaluates machine availability
- Assigns missions or commands
- Never executes hardware logic
- Resilient to machine disconnects

---

## 10. Mission Execution

- Missions defined as JSON
- Parsed and executed locally on machine
- Steps are atomic and interruptible
- Mission progress reported as state/events

---

## 11. Safety Architecture

- Hardware limits enforced locally
- Watchdogs for command and heartbeat
- Emergency stop is local-only
- Server cannot override safety

---

## 12. Failure Handling

- Network failure triggers safe mode
- Duplicate commands ignored
- Late commands evaluated safely
- Reboot resumes in known-safe state

---

## 13. Simulation & Testing

- Fake machines use identical protocol
- Simulation injects faults and latency
- Fleet logic tested without hardware
- CI can run full fleet simulations

---

## 14. OTA Updates

- Updates pulled by machine
- Verified via signatures
- Applied only in safe states
- Rollback on failure
- Staged rollout supported

---

## 15. Calibration Layer

- Per-machine calibration profiles
- Motor and sensor compensation
- Stored locally and versioned
- Adjustable without redeploy

---

## 16. Security Model

- machine identity verified on connect
- Commands authorized per role
- Messages validated strictly
- Updates cryptographically signed
- No implicit trust between components

---

## 17. Observability

- Structured logging everywhere
- Event severity levels
- Metrics for latency and uptime
- Replayable timelines for debugging

---

## 18. Scalability Notes

- machines scale horizontally
- Server can be sharded
- WS connections load-balanced
- No machine-to-machine dependencies

---

## 19. Design Constraints

- Assume unreliable networks
- Assume hardware imperfections
- Assume partial outages
- Favor determinism over cleverness

---

## 20. Guiding Principle

- Simple protocols
- Explicit state
- Autonomous edges
- Coordinated, not controlled
