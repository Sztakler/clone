import random
import time
import logging
from utils.time_utils import to_uint32
from models import RobotState, RobotStatus, FanMode

class RobotService:
    def __init__(self):
        self.status: RobotStatus = RobotStatus.IDLE
        self.start_time: float= time.time()
        self.uptime: int = 0
        self.fan_speed: int = 0
        self.fan_mode : FanMode = FanMode.PROPORTIONAL
        self.fan_ranges = {
            "idle": (30, 50),    # min, max %
            "running": (60, 100)
        }
        self.power: float = 0.0
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return (
            f"<RobotService(status={self.status}, "
            f"uptime={self.uptime}s, "
            f"fan_speed={self.fan_speed}%, "
            f"fan_mode={self.fan_mode}, "
            f"power={self.power:.2f}W)>"
    )

    def calculate_fan_speed(self, power: float) -> int:
        min_speed, max_speed = self.fan_ranges[self.status]
        range_size = max_speed - min_speed
        if self.status == RobotStatus.IDLE:
            normalized = (power - 7) / (10 - 7)
        else:
            normalized = (power - 15) / (20 - 15)
        return min(100, max(0, int(normalized * range_size + min_speed)))

    def get_uptime(self):
        return to_uint32(time.time() - self.start_time)
    
    def get_state(self) -> RobotState:
        self.logger.debug("Generating robot state...")
        if self.status == RobotStatus.OFFLINE:
            return RobotState(
                temperature = 0.0,
                power = 0.0,
                status = RobotStatus.OFFLINE,
                fan_speed = 0.0,
                uptime = 0,
                logs = ["System offline"]
            )
        self.logger.info(self.status)

        if self.status == RobotStatus.RUNNING:
            power = random.uniform(15, 20)
        else: # IDLE or ERROR
            power = random.uniform(7, 10)

        if self.status == RobotStatus.RUNNING and self.fan_mode is None:
            raise ValueError("fan_mode is required")
        self.power = power
        self.fan_speed = self.calculate_fan_speed(power)

        base_temperature = random.uniform(20, 30)
        temperature = base_temperature + random.uniform(-1, 1) * power - (self.fan_speed * 0.1)

        self.uptime = self.get_uptime()

        return RobotState(
            temperature = round(temperature, 1),
            power = round(power, 1),
            status = self.status,
            fan_speed = self.fan_speed,
            uptime = self.uptime,
            logs = [f"Power: {power:.1f}W", f"Fan speed: {self.fan_speed}%"]
        )

    def turn_on(self):
        self.logger.info(self.status)
        if self.status == RobotStatus.RUNNING:
            self.logger.warning("Robot is already ON.")
            return False

        self.status = RobotStatus.RUNNING
        self.start_time = time.time()
        self.logger.info("Robot turned ON.")
        self.logger.info(self.status)
        return True

    def turn_off(self):
        if self.status == RobotStatus.OFFLINE:
            self.logger.warning("Robot is already OFF.")
            return False

        self.status = RobotStatus.OFFLINE
        self.fan_speed = 0
        self.fan_mode = FanMode.PROPORTIONAL
        self.logger.info("Robot turned OFF.")
        return True

    def reset(self):
        self.status = RobotStatus.IDLE
        self.fan_speed = 0
        self.fan_mode = FanMode.PROPORTIONAL
        self.logger.info("Robot has been reset.")
        return True

    def set_fan_mode(self, fan_mode: FanMode):
        if fan_mode not in FanMode:
            raise ValueError(f"Invalid fan mode: {fan_mode}")

        self.fan_mode = fan_mode
        self.logger.info(f"Fan mode set to {self.fan_mode}.")
        return True

robot_service = RobotService()
        


