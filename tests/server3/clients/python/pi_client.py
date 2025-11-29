import requests
import websocket
import json
import threading
import time
import random
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import ollama # New import
from collections import deque # New import
import socket

# Attempt to import OLED libraries
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

OLLAMA_HOST = os.getenv('OLLAMA_HOST', "http://localhost:11434") # New: Ollama server address
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', "phi3") # New: Default LLM model

DATA_LOG_FILE = f"machine_{MACHINE_ID}_training_data.csv"

# --- NEW: Thread-safe state management ---
state_lock = threading.Lock()
last_received_command = "None"

# Global variable to hold machine state received from API response
current_machine_state = {
    'is_auto_driving': False,
    'happiness': 50,
    'hunger': 0,
    'temperature': 0,
    'motor_left_speed': 0,
    'motor_right_speed': 0,
    'lights_on': False,
    'fog_lights_on': False,
}

# --- NEW: Function to get local IP for display ---
def get_ip_address():
    """Tries to get the local IP address. Returns 'N/A' on failure."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) # Connect to a public DNS server
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"

# --- NEW: OLED Display Management Thread ---
def manage_oled_display():
    """Manages the OLED display in a separate thread."""
    if not LUMA_OLED_AVAILABLE:
        return # Exit if library is not installed

    try:
        # Initialize the OLED device (assuming I2C on port 1, address 0x3C)
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
    except Exception as e:
        print(f"[OLED] Could not initialize display: {e}. Is it connected correctly?")
        return

    ip_address = get_ip_address() # Get IP once at the start

    while True:
        # Safely copy the state and last command to avoid holding the lock for too long
        with state_lock:
            state_copy = current_machine_state.copy()
            last_cmd = last_received_command

        with canvas(device) as draw:
            # Line 1: Machine ID and Status
            draw.text((0, 0), f"Machine #{MACHINE_ID} - Online", fill="white")
            # Line 2: IP Address
            draw.text((0, 10), f"IP: {ip_address}", fill="white")
            # Line 3: Tamagotchi Stats
            hap = state_copy.get('happiness', '--')
            hun = state_copy.get('hunger', '--')
            draw.text((0, 20), f"HAP: {hap}  HUN: {hun}", fill="white")
            # Line 4: Last Command Received
            draw.text((0, 32), f"CMD: {last_cmd}", fill="white")

        time.sleep(1) # Refresh the screen every second

# --- GPIO Placeholder (Replace with actual RPi.GPIO or pigpio calls) ---
def set_motor_speed(motor, speed):
    print(f"[GPIO] Setting {motor} speed to {speed}%") # Uncomment for debugging
    pass

def toggle_light(light_type):
    print(f"[GPIO] Toggling {light_type} lights") # Uncomment for debugging
    pass

# --- Data Logging --- #
def setup_data_logger():
    if not os.path.exists(DATA_LOG_FILE):
        with open(DATA_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'temperature', 'motor_left_speed', 'motor_right_speed',
                'lights_on', 'fog_lights_on', 'happiness', 'hunger', 'is_auto_driving',
                'command_received'
            ])

def log_data(machine_data, command_received=None):
    """Logs the full machine state (from API response) and command to CSV."""
    with open(DATA_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            machine_data.get('temperature'),
            machine_data.get('motor_left_speed'),
            machine_data.get('motor_right_speed'),
            machine_data.get('lights_on'),
            machine_data.get('fog_lights_on'),
            machine_data.get('happiness'),
            machine_data.get('hunger'),
            machine_data.get('is_auto_driving'),
            command_received
        ])

# --- RAG and LLM Integration ---
def read_recent_logs(num_lines=50):
    """Reads the last N lines from the data log file to use as context."""
    if not os.path.exists(DATA_LOG_FILE):
        return "No recent log data available."
    
    with open(DATA_LOG_FILE, 'r') as f:
        # Use deque to efficiently get the last N lines
        lines = deque(f, num_lines + 1) # +1 for header
    
    # Exclude header if present
    if len(lines) > 0 and 'timestamp' in lines[0]:
        lines.popleft()

    if not lines:
        return "No recent log data available."
    
    return "\n".join(lines)

def ask_brain(question: str):
    """Queries the local LLM (Ollama) with RAG context from recent logs."""
    print(f"[LLM] Asking brain: {question}")
    recent_logs = read_recent_logs()
    
    prompt = f"""You are the AI mind of Machine #{MACHINE_ID}. 
Your current state is: {json.dumps(current_machine_state, indent=2)}
Here is a log of your most recent actions and sensor readings:
```csv
{recent_logs}
```
Based on this context and your current state, answer the following question: '{question}'
Respond concisely and focus on facts from your logs or current state if applicable.
"""
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {'role': 'user', 'content': prompt}
        ])
        llm_response = response['message']['content']
        print(f"[LLM] Brain response: {llm_response}")
        return llm_response
    except Exception as e:
        print(f"[LLM] Error communicating with Ollama: {e}")
        return f"Error: Could not connect to brain ({e})"

# --- WebSocket App for Command Listening ---
def on_message(ws, message):
    """Called when a new message is received from the server."""
    global last_received_command
    data = json.loads(message)
    event_name = data.get('event')
    event_payload = json.loads(data.get('data', '{}'))
    
    print(f"---|> Received event: {event_name}, Payload: {event_payload}")

    if event_name == 'machine.control-sent':
        command = event_payload.get('command')
        
        # NEW: Safely update the last received command for the OLED display
        with state_lock:
            last_received_command = command
            
        print(f"---|> Processing command: {command}")
        # --- ADD YOUR GPIO LOGIC HERE ---
        if command == 'toggle_lights':
            toggle_light('main')
        elif command == 'toggle_fog_lights':
            toggle_light('fog')
        elif command == 'toggle_auto_driving':
            # This command will primarily update the DB. We update current_machine_state
            # to reflect this. The Pi will react via its next heartbeat.
            with state_lock:
                current_machine_state['is_auto_driving'] = not current_machine_state.get('is_auto_driving', False)
            print(f"Auto driving toggled. Pi will react on next status update response.")
        elif command == 'feed':
            print("Machine fed!") # Pi doesn't do much here, server updates hunger
        elif command == 'play':
            print("Machine played with!") # Pi doesn't do much here, server updates happiness
        elif command == 'ask_llm': # New command to query the LLM
            question = event_payload.get('question', 'What is my current status?')
            llm_response = ask_brain(question)
            # In a real scenario, you might send this response back to the server
            # or display it locally on the Pi's screen.
            print(f"[LLM Response for '{question}'] {llm_response}")
        # ... other control commands

def on_error(ws, error):
    """Called on WebSocket errors."""
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Called when the connection is closed."""
    print("### WebSocket connection closed ###")

def on_open(ws):
    """Called when the WebSocket connection is established."""
    print("### WebSocket connection opened ###")
    # Subscribe to this machine's specific control channel
    subscription_message = {
        "event": "pusher:subscribe",
        "data": {
            "channel": f"machine.{MACHINE_ID}.control"
        }
    }
    ws.send(json.dumps(subscription_message))
    print(f"Subscribed to channel: machine.{MACHINE_ID}.control")

def run_websocket_listener():
    """Sets up and runs the WebSocket listener."""
    while True:
        try:
            ws = websocket.WebSocketApp(WS_URL,
                                      on_open=on_open,
                                      on_message=on_message,
                                      on_error=on_error,
                                      on_close=on_close)
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# --- Status Heartbeat Thread ---
def send_status_heartbeat():
    """Sends machine status to the Laravel API every 2 seconds."""
    status_url = f"http://{LARAVEL_HOST}/api/machine/{MACHINE_ID}/status"
    
    while True:
        try:
            # --- GATHER YOUR SENSOR DATA HERE ---
            current_temperature = round(random.uniform(20.0, 40.0), 2)
            current_motor_left_speed = random.randint(0, 100)
            current_motor_right_speed = random.randint(0, 100)
            current_lights_on = random.choice([True, False])
            current_fog_lights_on = random.choice([True, False])

            payload = {
                "temperature": current_temperature,
                "motor_left_speed": current_motor_left_speed,
                "motor_right_speed": current_motor_right_speed,
                "lights_on": current_lights_on,
                "fog_lights_on": current_fog_lights_on,
            }
            
            response = requests.post(status_url, json=payload, timeout=5)
            response.raise_for_status() # Raise an exception for bad status codes
            
            response_data = response.json()
            print(f"<--- Sent status heartbeat. Response: {response.status_code}")
            
            # IMPORTANT: Update the global current_machine_state with the FULL state from the server
            # This includes Tamagotchi fields and auto_driving status.
            if 'machine' in response_data:
                global current_machine_state
                # NEW: Use lock for thread-safe update
                with state_lock:
                    current_machine_state.update(response_data['machine'])
            
            # --- AUTO-DRIVING LOGIC (placeholder) ---
            # NEW: Safely read state for auto-driving logic
            with state_lock:
                is_auto_driving = current_machine_state.get('is_auto_driving', False)

            if is_auto_driving:
                print("[AUTO-DRIVE] Machine is in auto-driving mode.")
                # Implement your auto-driving logic here based on sensor data
                # Example: current_machine_state has all data including happiness, hunger
                # if current_machine_state['hunger'] > 70:
                #     print("[AUTO-DRIVE] Feeling hungry, looking for food...")
                #     set_motor_speed('left', 20)
                #     set_motor_speed('right', 20)
                # else:
                #     set_motor_speed('left', 0)
                #     set_motor_speed('right', 0)
                pass
            else:
                # If not auto-driving, ensure motors are off unless controlled manually
                set_motor_speed('left', 0)
                set_motor_speed('right', 0)
            
            with state_lock:
                state_to_log = current_machine_state.copy()
            log_data(state_to_log) # Log the full, updated state

        except requests.exceptions.ConnectionError as e:
            print(f"Network connection error: {e}. Retrying in 5 seconds...")
        except requests.exceptions.Timeout:
            print(f"Request timed out after 5 seconds. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Error sending status heartbeat: {e}")
            
        time.sleep(2) # Send an update every 2 seconds


# --- Main Execution ---
if __name__ == "__main__":
    setup_data_logger()

    # Start the OLED display thread if the library is available
    if LUMA_OLED_AVAILABLE:
        oled_thread = threading.Thread(target=manage_oled_display, daemon=True)
        oled_thread.start()
        print("[OLED] Display thread started.")
    else:
        print("[OLED] luma.oled library not found. Skipping display. Install with: pip install luma.oled")

    # Start the WebSocket listener in a background thread
    ws_thread = threading.Thread(target=run_websocket_listener, daemon=True)
    ws_thread.start()

    # Start the status heartbeat in the main thread
    send_status_heartbeat()
```
