# services/tamagotchi.py
import asyncio
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..crud import get_machine_by_uuid

async def start_tamagotchi_loop():
    while True:
        await asyncio.sleep(60)  # every minute
        db: Session = SessionLocal()
        try:
            machine = get_machine_by_uuid(db)
            if machine and machine.is_online:
                machine.hunger = min(100, machine.hunger + 1)
                if abs(machine.motor_left_speed) + abs(machine.motor_right_speed) > 20:
                    machine.happiness = min(100, machine.happiness + 2)
                else:
                    machine.happiness = max(0, machine.happiness - 1)
                db.commit()
        finally:
            db.close()