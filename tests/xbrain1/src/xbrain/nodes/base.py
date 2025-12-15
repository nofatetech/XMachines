import asyncio
from abc import ABC, abstractmethod
from src.xbrain.events.event_bus import EventBus, event_bus

class Node(ABC):
    """
    Abstract base class for all nodes in the system.
    Provides a common interface for starting, stopping, and running nodes.
    """
    def __init__(self, bus: EventBus = event_bus):
        self._event_bus = bus
        self._task: asyncio.Task | None = None

    @abstractmethod
    async def run(self):
        """The main entry point and long-running loop for the node."""
        pass

    def start(self):
        """Starts the node's run loop as a background task."""
        if self._task is None:
            self._task = asyncio.create_task(self.run())
            return self._task

    async def stop(self):
        """Stops the node's run loop."""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                # This is expected
                pass
        self._task = None
