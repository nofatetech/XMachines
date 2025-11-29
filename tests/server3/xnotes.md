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

### Terminal 3 (for Testing - Dashboard Mode): Simulate a Machine Update

To test the system when running in `APP_MODE=SERVER`, you can pretend to be an RC car sending a status update. Run this command in a new terminal.

```bash
curl http://localhost:8000/machine-update
```

---

### Important Instructions (for `APP_MODE=SERVER`):

1.  **Start the Servers:** Make sure both the `php artisan serve` and `php artisan reverb:start` commands are running in their own terminals.
2.  **Open the Dashboard:** Navigate to your application's URL (e.g., `http://127.0.0.1:8000/dashboard`) in your browser.
3.  **Simulate an Update:** Run the `curl` command in the third terminal. You will see a random machine on the dashboard instantly switch to "Online" and its data will update.
4.  **Test the Timeout:** Wait 5 seconds *without* running the `curl` command again. You will see the machine's status switch back to "Offline" on the dashboard. This is the client-side timeout logic at work.
5.  **Test Controls:** Click the "Toggle Lights" or "Toggle Fog" buttons on any machine card. While no physical device will react, you can open your browser's developer console (F12) to see the log messages confirming that the control command was sent.

---
---

# Raspberry Pi Python Client (`clients/python/pi_client.py`)

This script is the heart of your physical machine (RC car). It runs on the Raspberry Pi and communicates with the Laravel server.

### Setup on the Raspberry Pi (or your local dev machine to test):

1.  **Install Python libraries:**
    ```bash
    pip install requests websocket-client python-dotenv
    ```
2.  **Locate the Code:** The `pi_client.py` script is located at `clients/python/pi_client.py` in this project.
3.  **Configure `.env` (for the Laravel app on the Pi):**
    If you're running the Laravel app *on the Pi itself* as a "machine heart" (`APP_MODE=MACHINE`), update its local `.env` file:
    ```
    APP_MODE=MACHINE
    MACHINE_ID=1 # This Pi's ID in the database
    LEADER_HOST=192.168.1.XXX:8000 # IP of the central server (if any) if this Pi is a follower
    REVERB_APP_KEY=some_random_key # Match your main .env
    ```
    *Note: The `pi_client.py` script will read from the main project's `.env` when run from `clients/python/`. If you move it to a Pi, ensure the Pi's environment variables or local `.env` provide the necessary `MACHINE_ID`, `LEADER_HOST`, and `REVERB_APP_KEY`.*
4.  **Run `pi_client.py`:**
    ```bash
    python clients/python/pi_client.py
    ```
    *(When running this from your project root, it will load the `../../.env` file for config)*

### Key aspects of the Python Script:

*   **Status Heartbeat:** It sends a POST request to `/api/machine/{MACHINE_ID}/status` (e.g., `http://127.0.0.1:8000/api/machine/1/status`) every 2 seconds with its sensor data.
*   **Command Listener:** It connects via WebSocket to the Reverb server (e.g., `ws://127.0.0.1:8000/app/{REVERB_APP_KEY}`) and subscribes to `machine.{MACHINE_ID}.control` to receive commands.
*   **GPIO Integration:** Includes placeholders for you to add your actual `RPi.GPIO` or `pigpio` calls.
*   **Data Logging:** Sets up and logs data to `machine_{MACHINE_ID}_training_data.csv` for future ML.

---

**To test a machine running as its own heart:**

1.  **Configure:** Change the `.env` on your local development machine to `APP_MODE=MACHINE` and set `MACHINE_ID` to an existing machine (e.g., `1`).
2.  **Start Laravel & Reverb:** `php artisan serve` and `php artisan reverb:start` (locally).
3.  **Run the Python client:** `python clients/python/pi_client.py` (locally, in a third terminal, ensuring `MACHINE_ID` and `LARAVEL_HOST` are set correctly in the Python script itself).
4.  **Open the Display:** Go to `http://172.0.0.1:8000/display` in your browser. You should see the single machine's card updating.