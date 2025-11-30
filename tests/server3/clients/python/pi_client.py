import requests
import websocket
import json
import threading
import time
import random
import os
import csv
import socket
from datetime import datetime
from dotenv import load_dotenv
from collections import deque
import pykka
import ollama

# --- Attempt to import OLED libraries ---
try:
    from luma.core.interface.serial import i2c
    from luma.core.render import canvas
    from luma.oled.device import ssd1306
    LUMA_OLED_AVAILABLE = True
except ImportError:
    LUMA_OLED_AVAILABLE = False

# --- CONFIGURATION ---
load_dotenv(dotenv_path='../../.env')

MACHINE_ID = int(os.getenv('MACHINE_ID', '1'))
LARAVEL_HOST = os.getenv('LEADER_HOST') if os.getenv('APP_MODE') == 'MACHINE' else os.getenv('APP_URL').replace('http://', '')
if not LARAVEL_HOST:
    LARAVEL_HOST = "127.0.0.1:8000"

REVERB_APP_KEY = os.getenv('REVERB_APP_KEY', "some_random_key")
WS_URL = f"ws://{LARAVEL_HOST}/app/{REVERB_APP_KEY}"
OLLAMA_HOST = os.getenv('OLLAMA_HOST', "http://localhost:11434")
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', "phi3")
DATA_LOG_FILE = f"machine_{MACHINE_ID}_training_data.csv"

# --- HELPER FUNCTIONS ---
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"

def setup_data_logger():
    if not os.path.exists(DATA_LOG_FILE):
        with open(DATA_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'temperature', 'motor_left_speed', 'motor_right_speed',
                             'lights_on', 'fog_lights_on', 'happiness', 'hunger', 'is_auto_driving',
                             'command_received'])

def log_data(machine_data, command_received=None):
    with open(DATA_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), machine_data.get('temperature'),
                         machine_data.get('motor_left_speed'), machine_data.get('motor_right_speed'),
                         machine_data.get('lights_on'), machine_data.get('fog_lights_on'),
                         machine_data.get('happiness'), machine_data.get('hunger'),
                         machine_data.get('is_auto_driving'), command_received])

def read_recent_logs(num_lines=50):
    if not os.path.exists(DATA_LOG_FILE): return "No recent log data available."
    with open(DATA_LOG_FILE, 'r') as f: lines = deque(f, num_lines + 1)
    if len(lines) > 0 and 'timestamp' in lines[0]: lines.popleft()
    return "\n".join(lines) if lines else "No recent log data available."

# --- ACTOR DEFINITIONS ---

class StateActor(pykka.ThreadingActor):
    """Manages the machine's state centrally."""
    def __init__(self):
        super().__init__()
        self.machine_state = {
            'is_auto_driving': False, 'happiness': 50, 'hunger': 0,
            'temperature': 0, 'motor_left_speed': 0, 'motor_right_speed': 0,
            'lights_on': False, 'fog_lights_on': False
        }
        self.last_command = "None"

    def on_receive(self, message):
        action = message.get('action')
        if action == 'get_all':
            return {
                'state': self.machine_state.copy(),
                'last_command': self.last_command
            }
        elif action == 'get_state':
            return self.machine_state.copy()
        elif action == 'update_state':
            self.machine_state.update(message.get('data', {}))
            # Also log the updated state
            log_data(self.machine_state)
            return self.machine_state
        elif action == 'update_last_command':
            self.last_command = message.get('command', 'unknown')
        elif action == 'toggle_auto_driving':
            self.machine_state['is_auto_driving'] = not self.machine_state['is_auto_driving']

class GPIOActor(pykka.ThreadingActor):
    """Handles all GPIO interactions."""
    def on_receive(self, message):
        command = message.get('command')
        if command == 'set_motor_speed':
            print(f"[GPIO] Setting {message['motor']} speed to {message['speed']}%")
        elif command == 'toggle_light':
            print(f"[GPIO] Toggling {message['light_type']} lights")

class TextBrainActor(pykka.ThreadingActor):
    """Handles text-based LLM interactions."""
    def __init__(self, state_actor):
        super().__init__()
        self.state_actor = state_actor

    def ask(self, question):
        print(f"[LLM] Asking text brain: {question}")
        current_state = self.state_actor.ask({'action': 'get_state'})
        recent_logs = read_recent_logs()
        prompt = f"""You are the AI mind of Machine #{MACHINE_ID}.
Your current state is: {json.dumps(current_state, indent=2)}
Recent logs:
```csv
{recent_logs}
```
Answer the question: '{question}'"""
        try:
            response = ollama.chat(model=OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}])
            llm_response = response['message']['content']
            print(f"[LLM] Brain response: {llm_response}")
            return llm_response
        except Exception as e:
            error_msg = f"Error communicating with Ollama: {e}"
            print(f"[LLM] {error_msg}")
            return f"Error: Could not connect to brain ({e})"

class VisualBrainActor(pykka.ThreadingActor):
    """Placeholder for image generation."""
    def generate_image(self, prompt):
        print(f"[VISUAL BRAIN] Received request to generate image for: '{prompt}'. This feature is not yet implemented.")
        # In the future, this would call an image generation model.
        time.sleep(5) # Simulate long-running task
        return "Image generation is a future feature."

class OledActor(pykka.ThreadingActor):
    """Manages the OLED display."""
    def __init__(self, state_actor):
        super().__init__()
        self.state_actor = state_actor
        self.device = None
        self.ip_address = "N/A"

    def on_start(self):
        if not LUMA_OLED_AVAILABLE:
            print("[OLED] luma.oled library not found. Skipping display.")
            return
        try:
            serial = i2c(port=1, address=0x3C)
            self.device = ssd1306(serial)
            self.ip_address = get_ip_address()
            self.actor_ref.tell({'action': 'update_display'}, delay=1)
            print("[OLED] Display actor started.")
        except Exception as e:
            print(f"[OLED] Could not initialize display: {e}")
            self.stop()

    def on_receive(self, message):
        if message.get('action') == 'update_display':
            if not self.device: return

            all_data = self.state_actor.ask({'action': 'get_all'})
            state = all_data['state']
            last_cmd = all_data['last_command']

            with canvas(self.device) as draw:
                draw.text((0, 0), f"Machine #{MACHINE_ID} - Online", fill="white")
                draw.text((0, 10), f"IP: {self.ip_address}", fill="white")
                hap = state.get('happiness', '--')
                hun = state.get('hunger', '--')
                draw.text((0, 20), f"HAP: {hap}  HUN: {hun}", fill="white")
                draw.text((0, 32), f"CMD: {last_cmd}", fill="white")

            # Schedule the next update
            self.actor_ref.tell({'action': 'update_display'}, delay=1)


class WebSocketActor(pykka.ThreadingActor):
    """Manages the WebSocket connection and command dispatching."""
    def __init__(self, state_actor, gpio_actor, text_brain_actor, visual_brain_actor):
        super().__init__()
        self.state_actor = state_actor
        self.gpio_actor = gpio_actor
        self.text_brain_actor = text_brain_actor
        self.visual_brain_actor = visual_brain_actor
        self.ws = None

    def on_start(self):
        # The websocket client runs in its own thread, managed by this actor.
        thread = threading.Thread(target=self.run_forever, daemon=True)
        thread.start()

    def run_forever(self):
        while True:
            try:
                self.ws = websocket.WebSocketApp(WS_URL,
                                                 on_open=self.on_open,
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close)
                self.ws.run_forever()
            except Exception as e:
                print(f"WebSocket connection failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def on_message(self, ws, message):
        data = json.loads(message)
        event_name = data.get('event')
        if event_name != 'machine.control-sent': return

        payload = json.loads(data.get('data', '{}'))
        command = payload.get('command')
        print(f"---|> Received command: {command}")
        self.state_actor.tell({'action': 'update_last_command', 'command': command})

        if command == 'toggle_lights':
            self.gpio_actor.tell({'command': 'toggle_light', 'light_type': 'main'})
        elif command == 'toggle_fog_lights':
            self.gpio_actor.tell({'command': 'toggle_light', 'light_type': 'fog'})
        elif command == 'toggle_auto_driving':
            self.state_actor.tell({'action': 'toggle_auto_driving'})
        elif command == 'ask_llm':
            question = payload.get('question', 'What is my current status?')
            # Ask the brain actor and print the result. .get() makes it non-blocking.
            future = self.text_brain_actor.ask(question)
            # You can handle the response asynchronously if needed
        elif command == 'imagine':
             prompt = payload.get('prompt', 'A robot dreaming.')
             self.visual_brain_actor.tell({'action': 'generate_image', 'prompt': prompt})
        elif command in ['feed', 'play']:
            print(f"Machine action '{command}' noted. Server handles state change.")

    def on_error(self, ws, error): print(f"WebSocket Error: {error}")
    def on_close(self, ws, close_status_code, close_msg): print("### WebSocket connection closed ###")
    def on_open(self, ws):
        print("### WebSocket connection opened ###")
        ws.send(json.dumps({
            "event": "pusher:subscribe",
            "data": {"channel": f"machine.{MACHINE_ID}.control"}
        }))
        print(f"Subscribed to channel: machine.{MACHINE_ID}.control")

class HeartbeatActor(pykka.ThreadingActor):
    """Sends status heartbeats to the server."""
    def __init__(self, state_actor, gpio_actor):
        super().__init__()
        self.state_actor = state_actor
        self.gpio_actor = gpio_actor

    def on_start(self):
        self.actor_ref.tell({'action': 'send_heartbeat'}, delay=2)

    def on_receive(self, message):
        if message.get('action') == 'send_heartbeat':
            self.send_status()
            self.perform_auto_drive_logic()
            # Schedule the next heartbeat
            self.actor_ref.tell({'action': 'send_heartbeat'}, delay=2)

    def send_status(self):
        status_url = f"http://{LARAVEL_HOST}/api/machine/{MACHINE_ID}/status"
        try:
            # --- GATHER SENSOR DATA HERE ---
            payload = {
                "temperature": round(random.uniform(20.0, 40.0), 2),
                "motor_left_speed": random.randint(0, 100),
                "motor_right_speed": random.randint(0, 100),
                "lights_on": random.choice([True, False]),
                "fog_lights_on": random.choice([True, False]),
            }
            response = requests.post(status_url, json=payload, timeout=5)
            response.raise_for_status()
            response_data = response.json()
            print(f"<--- Sent status heartbeat. Response: {response.status_code}")

            if 'machine' in response_data:
                self.state_actor.tell({'action': 'update_state', 'data': response_data['machine']})

        except requests.exceptions.RequestException as e:
            print(f"Error sending status heartbeat: {e}")

    def perform_auto_drive_logic(self):
        state = self.state_actor.ask({'action': 'get_state'})
        if state.get('is_auto_driving'):
            print("[AUTO-DRIVE] Machine is in auto-driving mode.")
            # Future auto-driving logic here
            # e.g., self.gpio_actor.tell({'command': 'set_motor_speed', ...})
        else:
            # Turn motors off if not auto-driving (safety)
            self.gpio_actor.tell({'command': 'set_motor_speed', 'motor': 'left', 'speed': 0})
            self.gpio_actor.tell({'command': 'set_motor_speed', 'motor': 'right', 'speed': 0})


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    setup_data_logger()

    # --- Start Actors ---
    state_actor = StateActor.start().proxy()
    gpio_actor = GPIOActor.start().proxy()
    text_brain_actor = TextBrainActor.start(state_actor=state_actor).proxy()
    visual_brain_actor = VisualBrainActor.start().proxy()
    oled_actor = OledActor.start(state_actor=state_actor).proxy()
    ws_actor = WebSocketActor.start(
        state_actor=state_actor,
        gpio_actor=gpio_actor,
        text_brain_actor=text_brain_actor,
        visual_brain_actor=visual_brain_actor
    ).proxy()
    heartbeat_actor = HeartbeatActor.start(state_actor=state_actor, gpio_actor=gpio_actor).proxy()

    print("--- All actors started. Client is running. Press Ctrl+C to exit. ---")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- Shutting down actors. ---")
        pykka.ActorRegistry.stop_all()

