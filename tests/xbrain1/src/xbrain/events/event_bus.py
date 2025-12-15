import asyncio
from collections import defaultdict
from typing import Dict, Type, List, Any

class EventBus:
    """A simple in-memory, asynchronous event bus."""

    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)

    def subscribe(self, topic: str) -> asyncio.Queue:
        """
        Subscribe to a topic and get a queue to receive messages.
        """
        queue = asyncio.Queue()
        self._subscribers[topic].append(queue)
        return queue

    async def publish(self, topic: str, message: Any):
        """
        Publish a message to a specific topic.
        """
        for queue in self._subscribers[topic]:
            await queue.put(message)

# A global instance of the event bus to be used throughout the application
event_bus = EventBus()
