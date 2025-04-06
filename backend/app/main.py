from fastapi import FastAPI
from utils.logging import configure_logging
from services.robot_service import RobotService
from models import RobotControlCommand
import logging

app = FastAPI()

configure_logging(log_level="DEBUG")

@app.get("/")
def root():
    logging.info("Endpoint / called")
    return {"status": "OK"}

@app.get("/state")
async def get_state():
    return robot_service.get_state()

@app.post("/control")
async def control_robot(action: RobotControlCommand):
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
