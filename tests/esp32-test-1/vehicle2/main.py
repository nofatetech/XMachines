# main.py
import uasyncio as asyncio
import network
import gc

from app.app import create_app
from app.config import WIFI_SSID, WIFI_PASS, DEBUG
from app.tasks import get_scheduled_tasks

def connect_wifi():
    """Connect to the configured WiFi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to WiFi SSID: {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        # Wait for connection with a timeout
        max_wait = 15
        while not wlan.isconnected() and max_wait > 0:
            print(".", end="")
            asyncio.run(asyncio.sleep(1))
            max_wait -= 1
        
        if wlan.isconnected():
            print("\nWiFi Connected!")
            print("IP Info:", wlan.ifconfig())
        else:
            print("\nFailed to connect to WiFi. Proceeding without network.")
    else:
        print("WiFi already connected.")
        print("IP Info:", wlan.ifconfig())
    return wlan.isconnected()

def start_app():
    """
    Main application entry point.
    Initializes the app, starts background tasks, and runs the web server.
    """
    # Create the MicroDot web application
    app = create_app()

    # Get the list of background tasks. This also schedules them.
    get_scheduled_tasks()

    print("Starting web server...")
    try:
        # Get the current event loop
        loop = asyncio.get_event_loop()

        # Create the server task
        loop.create_task(app.start_server(host="0.0.0.0", port=80, debug=DEBUG))
        
        # Run the event loop forever. This is non-blocking for the REPL.
        loop.run_forever()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, shutting down.")
    finally:
        # You might add cleanup code here if needed
        print("Application stopped.")
        
if __name__ == "__main__":
    print("--- Starting Application ---")
    gc.collect() # Clean up memory before starting
    
    connect_wifi()
    
    gc.collect() # Clean up after network connection
    
    start_app()
