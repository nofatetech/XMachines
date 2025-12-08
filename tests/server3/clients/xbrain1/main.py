# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

from .routers import api, ws, system
from .database import engine, Base
from .config import settings
from .services.tamagotchi import start_tamagotchi_loop

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
    from .routers.system import register_or_update
    from .database import SessionLocal
    db = SessionLocal()
    await register_or_update(db=db)
    db.close()

    # Start tamagotchi & any other background loops
    asyncio.create_task(start_tamagotchi_loop())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)