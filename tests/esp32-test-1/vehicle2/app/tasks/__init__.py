# app/tasks/__init__.py
import uasyncio as asyncio

# A list to hold all the task coroutines we want to run
_scheduled_tasks = []

def schedule(coro, delay_sec, *args, **kwargs):
    """
    Schedules a coroutine to run periodically.
    """
    async def wrapper():
        # Give other tasks a moment to start up
        await asyncio.sleep(0.1)
        while True:
            try:
                await coro(*args, **kwargs)
            except Exception as e:
                print(f"Error in scheduled task: {e}")
            await asyncio.sleep(delay_sec)

    print(f"Scheduling task to run every {delay_sec} seconds.")
    _scheduled_tasks.append(wrapper)

def get_scheduled_tasks():
    """
    Returns a list of asyncio Tasks for the event loop to run.
    """
    # Import all jobs to make sure they are scheduled
    from app.tasks import jobs
    
    # Return a list of created asyncio.Task objects
    return [asyncio.create_task(task()) for task in _scheduled_tasks]
