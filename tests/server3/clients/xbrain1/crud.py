from sqlalchemy.orm import Session
import models
import schemas
import config

def get_machine_by_uuid(db: Session):
    return db.query(models.Machine).filter(models.Machine.uuid == config.settings.MACHINE_UUID).first()

def update_motors(db: Session, motor: schemas.MotorControl):
    machine = get_machine_by_uuid(db)
    if machine:
        machine.motor_left_speed = motor.left
        machine.motor_right_speed = motor.right
        db.commit()
    return machine

def update_lights(db: Session, lights: schemas.LightsControl):
    machine = get_machine_by_uuid(db)
    if machine:
        machine.lights_on = lights.lights_on
        machine.fog_lights_on = lights.fog_lights_on
        db.commit()
    return machine
