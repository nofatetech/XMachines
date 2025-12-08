# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

import routers.api
import routers.ws
import routers.system       
import database.engine
import database.Base
import config.settings
import services.tamagotchi.start_tamagotchi_loop


# ------------------------------------------------------------------
# 1. Load Laravel .env from project root
# ------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if not os.path.exists(ENV_PATH):
    print(f"ERROR: .env not found at {ENV_PATH}")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv(ENV_PATH)

# ------------------------------------------------------------------
# 2. Read configuration
# ------------------------------------------------------------------
APP_MODE = os.getenv("APP_MODE", "MACHINE").upper()        # SERVER or MACHINE
MACHINE_ID = os.getenv("MACHINE_ID", "unknown")
LEADER_HOST_WS = os.getenv("LEADER_HOST_WS", "ws://127.0.0.1:8080")
LEADER_HOST_WEB = os.getenv("LEADER_HOST_WEB", "http://127.0.0.1:8000")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
REVERB_APP_KEY = os.getenv("REVERB_APP_KEY")
MACHINE_API_TOKEN = os.getenv("MACHINE_API_TOKEN")

# ------------------------------------------------------------------
# 3. Mode check
# ------------------------------------------------------------------
if APP_MODE not in ["SERVER", "MACHINE"]:
    print(f"Invalid APP_MODE='{APP_MODE}'. Must be SERVER or MACHINE")
    sys.exit(1)

if not REVERB_APP_KEY:
    print("ERROR: REVERB_APP_KEY not found in .env file.")
    sys.exit(1)

if not MACHINE_API_TOKEN and APP_MODE == "MACHINE":
    print("ERROR: MACHINE_API_TOKEN not found in .env file. Required for authentication.")
    sys.exit(1)

if APP_MODE == "SERVER":
    print(f"[{MACHINE_ID}] SERVER mode detected → xbrain1 disabled")
    sys.exit(0)

print(f"[{MACHINE_ID}] Starting xbrain1 in MACHINE mode")
print(f"   → Leader WS : {LEADER_HOST_WS}")
print(f"   → Leader Web: {LEADER_HOST_WEB}")
print(f"   → Ollama    : {OLLAMA_HOST}/api/generate ({OLLAMA_MODEL})")


app = FastAPI(
    title="XBrain1",
    description="FastAPI brain for XMachine fleet",
    version="1.0.0"
)

app.include_router(api.router)
app.include_router(ws.router)
app.include_router(system.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    # Auto-register this car when brain boots
    from routers.system import register_or_update
    from database import SessionLocal
    db = SessionLocal()
    await register_or_update(db=db)
    db.close()

    # Start tamagotchi & any other background loops
    asyncio.create_task(start_tamagotchi_loop())
    print("XBrain1 is starting up...")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8089, reload=True)
