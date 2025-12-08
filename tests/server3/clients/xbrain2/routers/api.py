# routers/api.py
from fastapi import APIRouter, Depends, BackgroundTasks
import schemas
import crud
import dependencies
import services.motors as motors
import services.lights as lights

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/motors")
async def api_set_motors(control: schemas.MotorControl,
                         machine = Depends(dependencies.get_current_machine),
                         db = Depends(dependencies.get_db)):
    crud.update_motors(db, control)
    motors.set_tank_drive(control.left, control.right)
    return {"status": "ok"}

@router.post("/lights")
async def api_set_lights(control: schemas.LightsControl,
                        db = Depends(dependencies.get_db)):
    crud.update_lights(db, control)
    lights.apply_lights(control.lights_on, control.fog_lights_on)
    return {"status": "ok"}

@router.get("/status", response_model=schemas.MachineStatus)
async def get_status(machine = Depends(dependencies.get_current_machine)):
    return machine