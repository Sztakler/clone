from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from utils.logging import configure_logging, LogLevel
from utils.files import read_last_lines
from services.robot_service import RobotService, robot_service
from models import RobotControlCommand, RobotState, RobotAction
import logging
from pydantic import ValidationError
from websockethub import WebSocketHub
import os
from config import config

app = FastAPI()

log_levels = {
    "debug": LogLevel.DEBUG,
    "info": LogLevel.INFO,
    "warning": LogLevel.WARNING,
    "error": LogLevel.ERROR,
    "critical": LogLevel.CRITICAL,
}


def get_robot_service():
    return robot_service

async def start_robot_service():
    await robot_service.generate_state_periodically()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_robot_service())
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
configure_logging(log_levels.get(config.log_level))
    
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    logging.info("Endpoint / called")
    return {"status": "OK"}

@app.get(
         "/state",
         response_model=RobotState,
         summary="Get current robot state",
         tags=["robot"]
         )
async def get_state(robot_service: RobotService = Depends(get_robot_service)):
    """
    Returns the current state of the robot.
    """
    try:
        state = robot_service.get_robot_state()
        logging.info(f"Acquired robot's state: {state}")
        return state
    except Exception as e:
        logging.error(f"Error while getting robot's state: {str(e)}")
        raise HTTPException(status)

@app.post(
          "/control",
          summary="Send control command",
          tags=["robot"],
          response_model=dict[str, str]
      )
async def control_robot(command: RobotControlCommand):
    """
    Accepts a control command for the robot and returns a confirmation message.
    Supported actions: on, off, reset, fan, fan_speed.
    If action is 'fan', a fan_mode must be specified.
    If action is 'fan_speed', a fan_speed must be specified and fan_mode must be 'static'.
    """
    logging.debug(f"Received control command: {command}")

    match command.action:
        case RobotAction.ON:
            logging.info("Turning robot ON")
            robot_service.turn_on()
        case RobotAction.OFF:
            logging.info("Turning robot OFF")
            robot_service.turn_off()
        case RobotAction.RESET:
            logging.info("Resetting robot")
            robot_service.reset()
        case RobotAction.FAN:
            try:
                logging.info(f"Setting fan mode to: {command.fan_mode}")
                robot_service.set_fan_mode(command.fan_mode)
            except Exception as e:
                logging.info(f"{str(e)}")
        case RobotAction.FAN_SPEED:
            logging.info(f"Setting fan speed to {command.fan_speed}")
            robot_service.set_fan_speed(command.fan_speed)
        case _:
            logging.warning(f"Unsupported action: {command.action}")
            raise HTTPException(status_code=400, detail=f"Unsupported action: {command.action}")

    return {"status": "success", "action": command.action}

@app.get(
    "/logs",
    response_class=PlainTextResponse,
    summary="Retrieve latest robot logs",
    tags=["robot"],
    responses={
        200: {
            "description": "Log content retrieved successfully",
            "content": {
                "text/plain": {
                    "example": (
                        "2025-04-08 21:47:03 - INFO - Robot turned ON\n"
                        "2025-04-08 21:47:04 - DEBUG - Fan mode set to AUTO\n"
                        "2025-04-08 21:47:05 - WARNING - Temperature spike detected"
                    )
                }
            }
        },
        404: {
            "description": "Log file not found"
        }
    },
    description="""
Returns the most recent lines from the currently active robot log file (`robot_monitor.log`).

This is intended for real-time inspection and debugging from the frontend interface.

⚠️ Does **not** include archived logs (`.log.1`, `.log.2`, etc.).

- Response type: plain text
"""
)
async def get_logs():
    LOG_FILE_PATH = "robot_monitor.log"
    if not os.path.exists(LOG_FILE_PATH):
        raise HTTPException(status_code=404, detail="Log file not found")

    try:
        lines = read_last_lines(LOG_FILE_PATH, 50)
        print(lines)
        return "\n".join(lines)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

state_hub = WebSocketHub()
control_hub = WebSocketHub()

@app.websocket("/ws/state")
async def websocket_endpoint(websocket: WebSocket):
    await state_hub.connect(websocket)
    try:
        while True:
            state = robot_service.get_robot_state()
            await state_hub.broadcast_json(
            {
                "temperature": state.temperature,
                "power": state.power,
                "status": state.status,
                "fan_speed": state.fan_speed,
                "uptime": state.uptime,
            }, websocket
            )
            await asyncio.sleep(0.1) # 10 Hz
    except WebSocketDisconnect:
        state_hub.disconnect(websocket)
        logging.info("Client disconnected")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")

@app.websocket("/ws/control")
async def websocket_control(websocket: WebSocket):
    await control_hub.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                command = RobotControlCommand(**data)

                try:
                    match command.action:
                        case RobotAction.ON:
                            logging.info("Turning robot ON")
                            robot_service.turn_on()
                        case RobotAction.OFF:
                            logging.info("Turning robot OFF")
                            robot_service.turn_off()
                        case RobotAction.RESET:
                            logging.info("Resetting robot")
                            robot_service.reset()
                        case RobotAction.FAN:
                            logging.info(f"Setting fan mode to: {command.fan_mode}")
                            robot_service.set_fan_mode(command.fan_mode)
                        case RobotAction.FAN_SPEED:
                            logging.info(f"Setting fan speed to {command.fan_speed}%")
                            robot_service.set_fan_speed(command.fan_speed)
                        case _:
                            logging.warning(f"Unsupported action: {command.action}")
                            raise HTTPException(status_code=400, detail=f"Unsupported action: {command.action}")
                    await control_hub.broadcast_json({
                                                "status": "success",
                                                "action": command.action,
                                                "fan_mode": command.fan_mode
                                              })
                except HTTPException as e:
                    await control_hub.broadcast_json({
                                                      "status": "error",
                                                      "detail": e.detail,
                                                      "code": e.status_code
                                                  })
            except ValidationError as e:
                await control_hub.broadcast_json({
                                              "status": "validation_error",
                                              "detail": e.errors(),
                                              "code": 422,
                                          })
    except WebSocketDisconnect:
        control_hub.disconnect(websocket)
        logging.info("Control client disconnected")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")

# Test HTML
@app.get("/ws_test")
async def ws_test():
    return HTMLResponse("""
    <script>
        const ws = new WebSocket("ws://localhost:5487/ws/state");
        ws.onmessage = (event) => console.log(event.data);
    </script>
    """)

@app.get("/ws-control-test")
async def websocket_control_test():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robot Control WS Test</title>
        <style>
            button { margin: 5px; padding: 10px; }
            .log { margin-top: 20px; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Robot WebSocket Control</h1>
        <div>
            <button onclick="sendCommand('on')">Turn ON</button>
            <button onclick="sendCommand('off')">Turn OFF</button>
            <button onclick="sendCommand('reset')">Reset</button>
        </div>
        <div>
            <button onclick="sendFanCommand('proportional')">Fan: Auto</button>
            <button onclick="sendFanCommand('static')">Fan: Manual</button>
        </div>
        <div class="log" id="log"></div>

        <script>
            const ws = new WebSocket('ws://' + window.location.host + '/ws/control');
            const log = document.getElementById('log');
            
            function addLog(message) {
                log.innerHTML += `<div>${new Date().toISOString()}: ${message}</div>`;
            }
            
            ws.onopen = () => addLog("Connected to WebSocket");
            ws.onclose = () => addLog("Disconnected from WebSocket");
            ws.onerror = (e) => addLog(`Error: ${JSON.stringify(e)}`);
            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                addLog(`Response: ${JSON.stringify(data)}`);
            };
            
            function sendCommand(action) {
                const command = { action };
                ws.send(JSON.stringify(command));
                addLog(`Sent: ${JSON.stringify(command)}`);
            }
            
            function sendFanCommand(fan_mode) {
                const command = { action: 'fan', fan_mode };
                ws.send(JSON.stringify(command));
                addLog(`Sent: ${JSON.stringify(command)}`);
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
  
    print(f"{config.host}")
    uvicorn.run(app, host=f"{config.host}", port=config.port)
