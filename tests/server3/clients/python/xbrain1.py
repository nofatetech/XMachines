#!/usr/bin/env python3
import os
import sys
import time
import json
import signal
import threading
import requests
from dataclasses import dataclass

# ------------------------------------------------------------------
# 1. Load Laravel .env from project root
# ------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if not os.path.exists(ENV_PATH):
    print(f"ERROR: .env not found at {ENV_PATH}")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv(ENV_PATH)

# ------------------------------------------------------------------
# 2. Read configuration
# ------------------------------------------------------------------
APP_MODE = os.getenv("APP_MODE", "MACHINE").upper()        # SERVER or MACHINE
MACHINE_ID = os.getenv("MACHINE_ID", "unknown")
LEADER_HOST_WS = os.getenv("LEADER_HOST_WS", "ws://127.0.0.1:8080")
LEADER_HOST_WEB = os.getenv("LEADER_HOST_WEB", "http://127.0.0.1:8000")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

# ------------------------------------------------------------------
# 3. Mode check
# ------------------------------------------------------------------
if APP_MODE not in ["SERVER", "MACHINE"]:
    print(f"Invalid APP_MODE='{APP_MODE}'. Must be SERVER or MACHINE")
    sys.exit(1)

if APP_MODE == "SERVER":
    print(f"[{MACHINE_ID}] SERVER mode detected → xbrain1 disabled")
    sys.exit(0)

print(f"[{MACHINE_ID}] Starting xbrain1 in MACHINE mode")
print(f"   → Leader WS : {LEADER_HOST_WS}")
print(f"   → Leader Web: {LEADER_HOST_WEB}")
print(f"   → Ollama    : {OLLAMA_HOST}/api/generate ({OLLAMA_MODEL})")

# ------------------------------------------------------------------
# 4. Heavy imports only when running as MACHINE
# ------------------------------------------------------------------
import RPi.GPIO as GPIO
import websocket

# ------------------------------------------------------------------
# 5. Hardware config (stepper motors)
# ------------------------------------------------------------------
LEFT_STEP, LEFT_DIR   = 17, 27
RIGHT_STEP, RIGHT_DIR = 22, 23
ENABLE_PIN = 24

@dataclass
class Config:
    max_speed: int = 1400
    acceleration: int = 1200
    microsteps: int = 16
    wheel_track: float = 0.16        # meters
    steps_per_rev: int = 200
    wheel_diameter: float = 0.065    # meters

    @property
    def steps_per_meter(self):
        return (self.steps_per_rev * self.microsteps) / (3.14159 * self.wheel_diameter)

cfg = Config()

# ------------------------------------------------------------------
# 6. Stepper Driver
# ------------------------------------------------------------------
class StepperBrain:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for p in [LEFT_STEP, LEFT_DIR, RIGHT_STEP, RIGHT_DIR, ENABLE_PIN]:
            GPIO.setup(p, GPIO.OUT); GPIO.output(p, GPIO.LOW)

        self.target_l = self.target_r = 0
        self.running = False
        self.stop_event = threading.Event()

    def drive(self, linear: float, angular: float):
        l_mps = linear - angular * cfg.wheel_track / 2
        r_mps = linear + angular * cfg.wheel_track / 2
        self.target_l = int(l_mps * cfg.steps_per_meter)
        self.target_r = int(r_mps * cfg.steps_per_meter)

        GPIO.output(LEFT_DIR,  GPIO.HIGH if self.target_l >= 0 else GPIO.LOW)
        GPIO.output(RIGHT_DIR, GPIO.HIGH if self.target_r >= 0 else GPIO.LOW)

        if not self.running:
            self.stop_event.clear()
            threading.Thread(target=self._pulse_loop, daemon=True).start()

    def stop(self):
        self.stop_event.set()
        self.target_l = self.target_r = 0

    def _pulse_loop(self):
        self.running = True
        GPIO.output(ENABLE_PIN, GPIO.LOW)
        cur_l = cur_r = 0.0

        while not self.stop_event.is_set():
            # Ramp
            for cur, tgt in [(cur_l, self.target_l), (cur_r, self.target_r)]:
                diff = tgt - cur
                step = cfg.acceleration * 0.01
                cur += step if diff > 0 else (-step if diff < 0 else 0)
                if abs(diff) < step:
                    cur = tgt
            cur_l, cur_r = cur_l, cur_r

            delay = 0.0006
            if abs(cur_l) > 10:
                GPIO.output(LEFT_STEP, 1); time.sleep(delay); GPIO.output(LEFT_STEP, 0)
            if abs(cur_r) > 10:
                GPIO.output(RIGHT_STEP, 1); time.sleep(delay); GPIO.output(RIGHT_STEP, 0)
            time.sleep(0.001)

        GPIO.output(ENABLE_PIN, GPIO.HIGH)
        self.running = False

    def cleanup(self):
        self.stop()
        time.sleep(0.2)
        GPIO.cleanup()

brain = StepperBrain()

# ------------------------------------------------------------------
# 7. LLM Helper Function (Ollama)
# ------------------------------------------------------------------
def llm(prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
    """
    Call local Ollama model and return response.
    Usage: response = llm("What should the robot do now?")
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return f"LLM failed: {e}"

# Example auto-test on boot (remove if you don’t want it)
# print("LLM test →", llm("In one word, what is this robot called?"))

# ------------------------------------------------------------------
# 8. Websocket to Leader (SERVER)
# ------------------------------------------------------------------
WS_URL = f"{LEADER_HOST_WS.rstrip('/')}/machine/{MACHINE_ID}"
ws = None

def send_status():
    print("send_status!")
    if not (ws and ws.sock and ws.sock.connected):
        print("ws not connected!")
        return
    linear  = (brain.target_l + brain.target_r) / (2 * cfg.steps_per_meter)
    angular = (brain.target_r - brain.target_l) / (cfg.wheel_track * cfg.steps_per_meter)
    status = {
        "type": "status",
        "machine_id": MACHINE_ID,
        "linear": round(linear, 3),
        "angular": round(angular, 3),
        "is_moving": brain.running,
        "cpu_temp": round(float(open('/sys/class/thermal/thermal_zone0/temp').read())/1000, 1)
    }
    ws.send(json.dumps(status))

def on_message(_, message):
    try:
        data = json.loads(message)
        cmd = data.get("command")

        if cmd == "drive":
            brain.drive(float(data.get("linear", 0)), float(data.get("angular", 0)))
        elif cmd == "stop":
            brain.stop()
        elif cmd == "llm":
            # Optional: let server trigger LLM calls
            query = data.get("prompt", "")
            response = llm(query)
            ws.send(json.dumps({"type": "llm_response", "response": response}))
        send_status()
    except Exception as e:
        print("Command error:", e)

def on_open(w):
    print(f"Connected to leader @ {LEADER_HOST_WS}")
    send_status()

def on_close(*_):
    print("Lost connection → reconnecting...")
    time.sleep(5)
    connect_ws()

def connect_ws():
    global ws
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=lambda _, e: print("WS Error:", e)
    )
    ws.run_forever(ping_interval=15, ping_timeout=10)

# ------------------------------------------------------------------
# 9. Background threads
# ------------------------------------------------------------------
def status_loop():
    while True:
        time.sleep(0.8)
        send_status()

# ------------------------------------------------------------------
# 10. Graceful shutdown
# ------------------------------------------------------------------
def shutdown(sig=None, frame=None):
    print(f"\n[{MACHINE_ID}] Shutting down xbrain1...")
    brain.cleanup()
    if ws: ws.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ------------------------------------------------------------------
# 11. Start everything
# ------------------------------------------------------------------
threading.Thread(target=status_loop, daemon=True).start()
threading.Thread(target=connect_ws, daemon=True).start()

print(f"[{MACHINE_ID}] xbrain1 is ALIVE and awaiting orders.")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    shutdown()