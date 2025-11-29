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
# or
php artisan reverb:start --host=127.0.0.1 --port=8080


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