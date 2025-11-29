import requests
import websocket
import json
import threading
import time
import random
import os
import csv
from datetime import datetime

# --- CONFIGURATION ---
# IMPORTANT: These should be set as environment variables on the Raspberry Pi
# For testing, you can uncomment and set them here.
# os.environ['MACHINE_ID'] = '1'
# os.environ['LARAVEL_HOST'] = '127.0.0.1:8000' # Use `localhost:8000` if Laravel is on the same Pi

MACHINE_ID = int(os.getenv('MACHINE_ID', '1'))  # Default to 1 if not set
LARAVEL_HOST = os.getenv('LARAVEL_HOST', "127.0.0.1:8000")

# These details come from your .env file and Reverb config
REVERB_APP_KEY = os.getenv('REVERB_APP_KEY', "some_random_key") # REVERB_APP_KEY from .env
WS_URL = f"ws://{LARAVEL_HOST}/app/{REVERB_APP_KEY}"

DATA_LOG_FILE = f"machine_{MACHINE_ID}_training_data.csv"

# Global variable to hold machine state received from dashboard (e.g., is_auto_driving)
# This is a simplified approach; a more robust solution might use a local database.
current_machine_state = {'is_auto_driving': False}

# --- GPIO Placeholder (Replace with actual RPi.GPIO or pigpio calls) ---
def set_motor_speed(motor, speed):
    # print(f"[GPIO] Setting {motor} speed to {speed}%")
    pass

def toggle_light(light_type):
    # print(f"[GPIO] Toggling {light_type} lights")
    pass

# --- Data Logging --- #
def setup_data_logger():
    if not os.path.exists(DATA_LOG_FILE):
        with open(DATA_LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'temperature', 'motor_left_speed', 'motor_right_speed',
                'lights_on', 'fog_lights_on', 'happiness', 'hunger', 'is_auto_driving',
                'command_received' # The command that triggered this state (if any)
            ])

def log_data(payload, command_received=None):
    with open(DATA_LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            payload.get('temperature'),
            payload.get('motor_left_speed'),
            payload.get('motor_right_speed'),
            payload.get('lights_on'),
            payload.get('fog_lights_on'),
            payload.get('happiness'), # These will be updated from DB response if sent to API
            payload.get('hunger'),    # or from local simulation in machine:life-cycle
            payload.get('is_auto_driving'),
            command_received
        ])

# --- WebSocket App for Command Listening ---
def on_message(ws, message):
    """Called when a new message is received from the server."""
    data = json.loads(message)
    event_name = data.get('event')
    # The actual data is a stringified JSON within the 'data' field
    event_payload = json.loads(data.get('data', '{}')) 
    
    print(f"---|> Received event: {event_name}, Payload: {event_payload}")

    if event_name == 'machine.control-sent':
        command = event_payload.get('command')
        print(f"---|> Processing command: {command}")
        # --- ADD YOUR GPIO LOGIC HERE ---
        if command == 'toggle_lights':
            toggle_light('main')
        elif command == 'toggle_fog_lights':
            toggle_light('fog')
        elif command == 'toggle_auto_driving':
            # This command will primarily update the DB, the Pi will react via the next heartbeat
            print("Auto driving toggled. Pi will react on next status update response.")
        elif command == 'feed':
            print("Machine fed!") # Pi doesn't do much here, server updates hunger
        elif command == 'play':
            print("Machine played with!") # Pi doesn't do much here, server updates happiness
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
    # Continually try to reconnect
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
            # Replace with actual sensor readings from GPIO
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
                # No need to send happiness/hunger/auto_driving from client, server handles these
            }
            
            response = requests.post(status_url, json=payload, timeout=5)
            response.raise_for_status() # Raise an exception for bad status codes
            
            response_data = response.json()
            print(f"<--- Sent status heartbeat. Response: {response.status_code}")
            
            # Update local state based on server's response (e.g., if auto_driving was toggled)
            # In a more complex system, the server might send the full machine state back.
            # For now, we assume the server's DB is the source of truth for these.
            # A dedicated 'machine.status-updated' event would be ideal here if Pi was listening to it
            
            # --- AUTO-DRIVING LOGIC (placeholder) ---
            if current_machine_state['is_auto_driving']:
                print("[AUTO-DRIVE] Machine is in auto-driving mode.")
                # Implement your auto-driving logic here based on sensor data
                # For example:
                # if current_temperature > 35: 
                #     set_motor_speed('left', 0) # Stop if too hot
                # else:
                #     set_motor_speed('left', 50)
                pass
            else:
                # If not auto-driving, ensure motors are off unless controlled manually
                set_motor_speed('left', 0)
                set_motor_speed('right', 0)

            log_data(payload)

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

    # Start the WebSocket listener in a background thread
    ws_thread = threading.Thread(target=run_websocket_listener, daemon=True)
    ws_thread.start()

    # Start the status heartbeat in the main thread
    send_status_heartbeat()

```
