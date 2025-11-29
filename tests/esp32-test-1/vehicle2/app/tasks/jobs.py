# app/tasks/jobs.py
from app.tasks import schedule
import uasyncio as asyncio

async def print_status_job():
    """
    A simple background job that prints a message periodically.
    """
    print("Background task: Checking system status... OK")
    # In a real app, you might do something useful here, like:
    # - Read a sensor value
    # - Ping a remote service
    # - Update system state
    await asyncio.sleep(0) # Yield control

# Schedule the job to run every 30 seconds
schedule(print_status_job, delay_sec=30)
