import requests

def send_heartbeat(machine_id, lifecycle):
    try:
        requests.post(
            "http://127.0.0.1:8000/heartbeat",
            json={"id": machine_id, "state": lifecycle.value},
            timeout=0.2,
        )
    except Exception:
        pass
