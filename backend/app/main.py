from fastapi import FastAPI, Depends, HTTPException
from utils.logging import configure_logging, LogLevel
from services.robot_service import RobotService
from models import RobotControlCommand, RobotState, RobotAction
import logging

app = FastAPI()

configure_logging(log_level=LogLevel.DEBUG)

def get_robot_service():
    return RobotService()

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

    robot_service = RobotService()

    match command.action:
        case RobotAction.ON:
            robot_service.turn_on
            logging.info("Turning robot ON")
        case RobotAction.OFF:
            # TODO: Call robot turn_off()
            logging.info("Turning robot OFF")
        case RobotAction.RESET:
            # TODO: Call robot reset()
            logging.info("Resetting robot")
        case RobotAction.FAN:
            # TODO: Adjust fan mode to: {command.fan_mode}
            logging.info(f"Setting fan mode to: {command.fan_mode}")
        case _:
            logging.warning(f"Unsupported action: {command.action}")
            raise HTTPException(status_code=400, detail=f"Unsupported action: {command.action}")

    return {"status": "success", "action": command.action}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
