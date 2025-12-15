import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect

from src.xbrain.nodes.base import Node
from src.xbrain.domain.models import Message, CommandMessage, StateMessage, EventMessage
from src.xbrain.events.event_bus import event_bus

class WebSocketNode(Node):
    """
    Manages the persistent WebSocket connection with the fleet server.
    It handles both incoming commands and outgoing state/event messages.
    """

    def __init__(self, machine_id: str):
        super().__init__()
        self._machine_id = machine_id
        self._websocket: WebSocket | None = None
        self._state_out_queue = self._event_bus.subscribe("state_out")
        self._event_out_queue = self._event_bus.subscribe("event_out")

    async def handle_connection(self, websocket: WebSocket):
        """
        This method is called by the FastAPI endpoint when a client connects.
        It manages the lifecycle of the WebSocket connection.
        """
        await websocket.accept()
        self._websocket = websocket
        print("WebSocketNode: Connection accepted.")

        # Run send and receive loops concurrently
        receive_task = asyncio.create_task(self._receive_loop())
        send_task = asyncio.create_task(self._send_loop())

        done, pending = await asyncio.wait(
            [receive_task, send_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        
        for task in pending:
            task.cancel()

        self._websocket = None
        print("WebSocketNode: Connection closed.")

    async def _receive_loop(self):
        """Listens for incoming messages from the server."""
        if not self._websocket:
            return
        
        try:
            while True:
                data = await self._websocket.receive_text()
                # In a real implementation, you'd parse this into a CommandMessage
                # and publish it to a "command_in" topic.
                await self._event_bus.publish("command_in", data)
                print(f"WebSocketNode: Received data: {data}")
        except WebSocketDisconnect:
            print("WebSocketNode: Client disconnected.")
        except Exception as e:
            print(f"WebSocketNode: Receive loop error: {e}")

    async def _send_loop(self):
        """Waits for messages from internal nodes and sends them to the server."""
        if not self._websocket:
            return

        # Create tasks to wait on each queue
        state_task = asyncio.create_task(self._state_out_queue.get())
        event_task = asyncio.create_task(self._event_out_queue.get())

        try:
            while True:
                done, pending = await asyncio.wait(
                    [state_task, event_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                # Process whichever task finished
                if state_task in done:
                    message: StateMessage = state_task.result()
                    await self._websocket.send_text(message.model_dump_json())
                    print(f"WebSocketNode: Sent state message seq={message.seq}")
                    # Create a new task to wait for the next state message
                    state_task = asyncio.create_task(self._state_out_queue.get())
                
                if event_task in done:
                    message: EventMessage = event_task.result()
                    await self._websocket.send_text(message.model_dump_json())
                    print(f"WebSocketNode: Sent event message name={message.payload.name}")
                    # Create a new task to wait for the next event message
                    event_task = asyncio.create_task(self._event_out_queue.get())

        except Exception as e:
            print(f"WebSocketNode: Send loop error: {e}")
        finally:
            # Cleanup tasks on exit
            state_task.cancel()
            event_task.cancel()

    async def run(self):
        """
        The run method for this node is passive. Its main logic is triggered
        by the handle_connection method, which is controlled by FastAPI.
        This loop just keeps the node alive conceptually.
        """
        print("WebSocketNode: Started and waiting for connections.")
        while True:
            # We could add periodic health checks or other background tasks here
            await asyncio.sleep(3600)
