# app/config.py

# Attempt to import credentials, but handle the case where the file doesn't exist.
try:
    from credentials import WIFI_SSID, WIFI_PASS
except ImportError:
    print("Warning: 'credentials.py' not found. Using default empty credentials.")
    WIFI_SSID = ""
    WIFI_PASS = ""

# Application settings
APP_NAME = "ESP32 Vehicle Control"
APP_VERSION = "0.1.0"
DEBUG = True
