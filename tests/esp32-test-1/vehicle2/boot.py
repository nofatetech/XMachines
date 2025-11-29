# boot.py
# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import esp

# Disable ESP-IDF debug output on UART
esp.osdebug(None)

# Run garbage collection to free up memory
gc.collect()

print("boot.py finished.")
