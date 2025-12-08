# FastAPI Server Management for XBrain1

This document provides instructions for starting, stopping, restarting, and setting up the XBrain1 FastAPI server for persistent operation on a Linux system using `systemd`.

**Project Root Directory:** `/home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/server3`
**FastAPI Application Directory:** `/home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/server3/clients/xbrain1`

---

## 1. Manual Startup (for Development)

This method is suitable for development, as it allows for automatic reloading on code changes and easy termination.

### Start the Server

1.  **Navigate to the application directory:**
    ```bash
    cd /home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/server3/clients/xbrain1
    ```
2.  **Run uvicorn from the virtual environment:**
    ```bash
    .venv/bin/uvicorn main:app --reload
    ```
    *   `main`: Refers to the `main.py` file.
    *   `app`: Refers to the `app = FastAPI()` object within `main.py`.
    *   `--reload`: Automatically restarts the server on code changes.

### Kill the Server

If the server is running in the foreground (you see logs in your terminal):
*   Press `Ctrl+C` in the terminal where the server is running.

If the server was started in the background (e.g., with `&`):
1.  **Find the process ID (PID):**
    ```bash
    pgrep -f "uvicorn main:app"
    ```
    This will output one or more PIDs.
2.  **Kill the process:**
    ```bash
    kill <PID>
    ```
    Replace `<PID>` with the actual process ID you found. For example, if the PID was `72388`:
    ```bash
    kill 72388
    ```

### Restart the Server

To restart a manually run server, simply kill the existing process and then run the start command again.

---

## 2. "Always On" Setup with `systemd` (for Production/Persistence)

For robust, "always on" operation, especially in production environments, `systemd` is the recommended method on Linux. It ensures your application starts automatically on boot and recovers from crashes.

### Step 1: Create a `systemd` Service File

You need to create a service definition file.

1.  **Create the file:** You will need `sudo` permissions to create this file.
    ```bash
    sudo nano /etc/systemd/system/xbrain1.service
    ```
    (You can use `vim` or another editor instead of `nano`).

2.  **Paste the following content into the file:**
    ```ini
    [Unit]
    Description=XBrain1 FastAPI Server
    After=network.target

    [Service]
    User=user1
    Group=user1
    WorkingDirectory=/home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/server3/clients/xbrain1
    ExecStart=/home/user1/Documents/dev/XMachines/gitrepo_XMachines/tests/server3/clients/xbrain1/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
    Restart=always
    RestartSec=3

    [Install]
    WantedBy=multi-user.target
    ```
    *   **Important:** Ensure `User` and `Group` match your system's user and group for running the service.
    *   `ExecStart`: Specifies the exact command to run your FastAPI application.

3.  **Save and close the file.**

### Step 2: Manage the `systemd` Service

After creating the service file, use these `systemctl` commands to manage your application:

1.  **Reload `systemd` daemon:** This makes `systemd` aware of your new service file.
    ```bash
    sudo systemctl daemon-reload
    ```
2.  **Enable the service:** This configures the service to start automatically every time the system boots.
    ```bash
    sudo systemctl enable xbrain1.service
    ```
3.  **Start the service:** This starts your FastAPI application immediately.
    ```bash
    sudo systemctl start xbrain1.service
    ```
4.  **Stop the service:**
    ```bash
    sudo systemctl stop xbrain1.service
    ```
5.  **Restart the service:**
    ```bash
    sudo systemctl restart xbrain1.service
    ```
6.  **Check the service status and logs:**
    ```bash
    # View current status
    sudo systemctl status xbrain1.service
    
    # View real-time logs (press Ctrl+C to exit)
    sudo journalctl -u xbrain1.service -f
    ```
