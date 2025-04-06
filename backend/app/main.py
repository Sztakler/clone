from fastapi import FastAPI, Depends
from utils.logging import configure_logging
from services.robot_service import RobotService
from models import RobotControlCommand
import logging

app = FastAPI()

configure_logging(log_level="DEBUG")

def get_robot_service():
    return RobotService()

@app.get("/")
def root():
    logging.info("Endpoint / called")
    return {"status": "OK"}

@app.get("/state")
async def get_state(robot_service: RobotService = Depends(get_robot_service)):
    robot_state = robot_service.get_state()
    if robot_state:
        logging.info("Acquired robot state")
    return robot_state

@app.post("/control")
async def control_robot(action: RobotControlCommand):
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
