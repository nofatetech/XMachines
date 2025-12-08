from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
import database
import crud
import config

async def get_current_machine(db: Session = Depends(database.get_db)):
    machine = crud.get_machine_by_uuid(db)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not registered")
    return machine
