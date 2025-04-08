from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
from utils.logging import configure_logging, LogLevel
from services.robot_service import RobotService, robot_service
from models import RobotControlCommand, RobotState, RobotAction
import logging
from pydantic import ValidationError
from websockethub import WebSocketHub

app = FastAPI()

configure_logging(log_level=LogLevel.DEBUG)

def get_robot_service():
    return robot_service

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
        state = robot_service.get_state()
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
    Supported actions: on, off, reset, fan.
    If action is 'fan', a fan_mode must be specified.
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
            logging.info(f"Setting fan mode to: {command.fan_mode}")
            robot_service.set_fan_mode(command.fan_mode)
        case _:
            logging.warning(f"Unsupported action: {command.action}")
            raise HTTPException(status_code=400, detail=f"Unsupported action: {command.action}")

    return {"status": "success", "action": command.action}

state_hub = WebSocketHub()
control_hub = WebSocketHub()

@app.websocket("/ws/state")
async def websocket_endpoint(websocket: WebSocket):
    await state_hub.connect(websocket)
    try:
        while True:
            state = robot_service.get_state()
            await state_hub.broadcast_json(
            {
                "temperature": state.temperature,
                "power": state.power,
                "status": state.status,
                "fan_speed": state.fan_speed,
                "uptime": state.uptime,
            }
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
        const ws = new WebSocket("ws://localhost:8000/ws/state");
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
