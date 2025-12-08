# routers/system.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
import models
import crud
import schemas
import database
import config
import socket

router = APIRouter(tags=["system"])

@router.get("/ping")
async def ping():
    return {
        "car": config.settings.MACHINE_NAME,
        "uuid": config.settings.MACHINE_UUID,
        "ip": socket.gethostbyname(socket.gethostname())
    }

@router.post("/register")
async def register_or_update(db: Session = Depends(database.get_db)):
    machine = crud.get_machine_by_uuid(db)
    if not machine:
        machine = models.Machine(uuid=config.settings.MACHINE_UUID, name=config.settings.MACHINE_NAME)
        db.add(machine)
    machine.is_online = True
    machine.name = config.settings.MACHINE_NAME
    db.commit()
    return {"status": "registered", "id": machine.id}
