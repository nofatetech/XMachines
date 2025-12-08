from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
import crud
import schemas
import dependencies
import services.motors
import services.lights

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db = Depends(dependencies.get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "motors":
                motor = schemas.MotorControl(**data["payload"])
                await crud.update_motors(db, motor)
                # immediately apply to actual GPIO here
                services.motors.set_tank_drive(motor.left, motor.right)

            elif action == "lights":
                lights = schemas.LightsControl(**data["payload"])
                crud.update_lights(db, lights)
                services.lights.apply_lights(lights)

            await websocket.send_json({"status": "ok"})
    except WebSocketDisconnect:
        pass
