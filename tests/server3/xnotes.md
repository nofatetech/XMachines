# How to Run and Test the XMachines Dashboard

Here are the commands and instructions to get the full application running. You will need 2-3 separate terminal windows.

---

### Terminal 1: Start the Web Server

This command serves the main Laravel application, including the dashboard.

```bash
php artisan serve
```
*You will access the dashboard at the URL provided by this command (usually `http://127.0.0.1:8000`).*

---

### Terminal 2: Start the Reverb WebSocket Server

This is the real-time server that handles all WebSocket connections. It must be running for the dashboard to receive live updates.

```bash
php artisan reverb:start
```
*Leave this terminal running. You can add `--debug` to see live connection and channel information.*

---

### Terminal 3 (for Testing): Simulate a Machine Update

To test the system, you can pretend to be an RC car sending a status update. Run this command in a new terminal.

```bash
curl http://localhost:8000/machine-update
```

---

### Important Instructions:

1.  **Start the Servers:** Make sure both the `php artisan serve` and `php artisan reverb:start` commands are running in their own terminals.
2.  **Open the Dashboard:** Navigate to your application's URL (e.g., `http://127.0.0.1:8000/dashboard`) in your browser.
3.  **Simulate an Update:** Run the `curl` command in the third terminal. You will see a random machine on the dashboard instantly switch to "Online" and its data will update.
4.  **Test the Timeout:** Wait 5 seconds *without* running the `curl` command again. You will see the machine's status switch back to "Offline" on the dashboard. This is the client-side timeout logic at work.
5.  **Test Controls:** Click the "Toggle Lights" or "Toggle Fog" buttons on any machine card. While no physical device will react, you can open your browser's developer console (F12) to see the log messages confirming that the control command was sent.

---
---

# Raspberry Pi Python Client (`pi_client.py`)

This script is the heart of your physical machine (RC car). It runs on the Raspberry Pi and communicates with the Laravel server.

### Setup on the Raspberry Pi:

1.  **Install Python libraries:**
    ```bash
    pip install requests websocket-client
    ```
2.  **Save the Code:** Save the code below as `pi_client.py` on your Raspberry Pi.
3.  **Configure:** Change the `MACHINE_ID` and `LARAVEL_HOST` variables at the top of the script.
4.  **Run:**
    ```bash
    python pi_client.py
    ```

### Example Python Script:

```python
import requests
import websocket
import json
import threading
import time
import random

# --- CONFIGURATION ---
MACHINE_ID = 1  # IMPORTANT: Change this for each machine!
LARAVEL_HOST = "127.0.0.1:8000"  # Use the IP of the computer running Laravel

# --- WebSocket App for Command Listening ---
def on_message(ws, message):
    """Called when a new message is received from the server."""
    data = json.loads(message)
    event = data.get('event')
    payload = json.loads(data.get('data', '{}')) # The actual data is a stringified JSON
    
    if event == 'machine.control-sent':
        command = payload.get('command')
        print(f"---|> Received command: {command}")
        # --- ADD YOUR GPIO LOGIC HERE ---
        # Example:
        # if command == 'toggle_lights':
        #     toggle_gpio_pin(LIGHTS_PIN)
        # elif command == 'toggle_fog_lights':
        #     toggle_gpio_pin(FOG_LIGHTS_PIN)

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
    # These details come from your .env file and Reverb config
    app_key = "some_random_key" # REVERB_APP_KEY from .env
    ws_url = f"ws://{LARAVEL_HOST}/app/{app_key}"
    
    ws = websocket.WebSocketApp(ws_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

# --- Status Heartbeat Thread ---
def send_status_heartbeat():
    """Sends machine status to the Laravel API every 2 seconds."""
    status_url = f"http://{LARAVEL_HOST}/api/machine/{MACHINE_ID}/status"
    while True:
        try:
            # --- GATHER YOUR SENSOR DATA HERE ---
            payload = {
                "temperature": round(random.uniform(20.0, 40.0), 2),
                "motor_left_speed": random.randint(0, 100),
                "motor_right_speed": random.randint(0, 100),
                "lights_on": random.choice([True, False]),
                "fog_lights_on": random.choice([True, False]),
            }
            
            response = requests.post(status_url, json=payload, timeout=2)
            response.raise_for_status() # Raise an exception for bad status codes
            
            print(f"<--- Sent status heartbeat: {response.status_code} - {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending status heartbeat: {e}")
            
        time.sleep(2) # Send an update every 2 seconds


# --- Main Execution ---
if __name__ == "__main__":
    # Start the WebSocket listener in a background thread
    ws_thread = threading.Thread(target=run_websocket_listener, daemon=True)
    ws_thread.start()

    # Start the status heartbeat in the main thread
    send_status_heartbeat()
```
