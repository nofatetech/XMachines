import asyncio
import random
from src.xbrain.nodes.base import Node
from src.xbrain.domain.models import StateMessage, StatePayload, MachineState

class StateAggregatorNode(Node):
    """
    Simulates gathering state from various internal sensors and aggregates it
    into a single state message, publishing it at a regular interval.
    """

    def __init__(self, machine_id: str, publish_interval_seconds: int = 5):
        super().__init__()
        self._machine_id = machine_id
        self._interval = publish_interval_seconds
        self._seq = 0

    async def run(self):
        """
        Periodically gathers machine state and publishes it to the 'state_out' topic.
        """
        print("StateAggregatorNode: Started")
        while True:
            try:
                # In a real scenario, this node would subscribe to topics from
                # other sensor nodes and aggregate their data.
                # For now, we simulate it.
                state_payload = StatePayload(
                    status=random.choice([MachineState.IDLE, MachineState.ACTIVE]),
                    battery_level=round(random.uniform(80.0, 100.0), 2),
                    speed=round(random.uniform(0.0, 1.2), 2),
                )

                message = StateMessage(
                    machine_id=self._machine_id,
                    seq=self._seq,
                    payload=state_payload,
                )

                await self._event_bus.publish("state_out", message)
                self._seq += 1

                await asyncio.sleep(self._interval)
            except asyncio.CancelledError:
                print("StateAggregatorNode: Stopped")
                break
            except Exception as e:
                # In a real system, we'd publish an EventMessage here
                print(f"StateAggregatorNode encountered an error: {e}")
                await asyncio.sleep(self._interval)
