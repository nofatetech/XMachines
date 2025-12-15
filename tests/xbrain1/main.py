import asyncio
from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager

from src.xbrain.nodes.websocket_node import WebSocketNode
from src.xbrain.nodes.state_aggregator_node import StateAggregatorNode

# --- Configuration ---
MACHINE_ID = "machine-001"


# --- Application Components ---
nodes = [
    StateAggregatorNode(machine_id=MACHINE_ID),
    WebSocketNode(machine_id=MACHINE_ID),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("--- xBrain Runtime Starting ---")
    # Start all nodes
    for node in nodes:
        node.start()
    print(f"Started {len(nodes)} nodes.")
    
    yield
    
    # --- Shutdown ---
    print("--- xBrain Runtime Shutting Down ---")
    # Stop all nodes
    for node in nodes:
        await node.stop()
    print("All nodes stopped.")


app = FastAPI(lifespan=lifespan)
ws_node = next(node for node in nodes if isinstance(node, WebSocketNode))


# --- API Endpoints ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """The main WebSocket endpoint for the machine agent."""
    await ws_node.handle_connection(websocket)

@app.get("/")
def read_root():
    """A simple HTTP endpoint to confirm the service is running."""
    return {"message": f"x-Brain edge runtime for machine '{MACHINE_ID}' is active."}