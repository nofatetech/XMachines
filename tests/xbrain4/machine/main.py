import time
import threading
from fastapi import FastAPI
import uvicorn

from state import MachineState
from lifecycle import Lifecycle
from motor import TankMotorController
from udp_comm import UDPServer
from coordinator_client import send_heartbeat

state = MachineState(machine_id="machine-001")
motor = TankMotorController(state)
udp = UDPServer(state, motor)

app = FastAPI()

@app.get("/state")
def get_state():
    return {
        "id": state.machine_id,
        "lifecycle": state.lifecycle.value,
        "mode": state.mode,
    }

@app.post("/activate")
def activate():
    state.lifecycle = Lifecycle.ACTIVE
    return {"status": "activated"}

@app.post("/shutdown")
def shutdown():
    state.lifecycle = Lifecycle.SHUTDOWN
    return {"status": "shutdown"}

@app.post("/mode")
def set_mode(new_mode: dict):
    mode_value = new_mode.get("mode")
    if mode_value not in ["manual", "autonomous"]:
        return {"error": "Invalid mode. Must be 'manual' or 'autonomous'."}, 400
    state.mode = mode_value
    return {"status": f"mode set to {state.mode}"}

def udp_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        udp.poll()
        udp.watchdog()
        time.sleep(0.01)

def heartbeat_loop():
    while state.lifecycle != Lifecycle.SHUTDOWN:
        send_heartbeat(state.machine_id, state.lifecycle)
        time.sleep(1)

if __name__ == "__main__":
    state.lifecycle = Lifecycle.IDLE

    threading.Thread(target=udp_loop, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()

    uvicorn.run(app, host="0.0.0.0", port=8001)
