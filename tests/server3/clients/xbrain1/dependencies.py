from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .crud import get_machine_by_uuid
from .config import settings

async def get_current_machine(db: Session = Depends(get_db)):
    machine = get_machine_by_uuid(db)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not registered")
    return machine