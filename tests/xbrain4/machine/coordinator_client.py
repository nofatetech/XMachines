import requests
import os

def send_heartbeat(machine_id, lifecycle):
    coordinator_url = os.getenv("COORDINATOR_URL", "http://127.0.0.1:8000")
    if not coordinator_url:
        return 

    try:
        requests.post(
            f"{coordinator_url}/heartbeat",
            json={"id": machine_id, "state": lifecycle.value},
            timeout=0.2,
        )
    except Exception:
        pass
