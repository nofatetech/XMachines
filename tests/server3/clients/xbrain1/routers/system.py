# routers/system.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from .. import models, crud, schemas
from ..database import get_db
from ..config import settings
import socket

router = APIRouter(tags=["system"])

@router.get("/ping")
async def ping():
    return {
        "car": settings.MACHINE_NAME,
        "uuid": settings.MACHINE_UUID,
        "ip": socket.gethostbyname(socket.gethostname())
    }

@router.post("/register")
async def register_or_update(db: Session = Depends(get_db)):
    machine = crud.get_machine_by_uuid(db)
    if not machine:
        machine = models.Machine(uuid=settings.MACHINE_UUID, name=settings.MACHINE_NAME)
        db.add(machine)
    machine.is_online = True
    machine.name = settings.MACHINE_NAME
    db.commit()
    return {"status": "registered", "id": machine.id}