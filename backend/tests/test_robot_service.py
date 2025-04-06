import unittest
from app.models import RobotState, RobotStatus, FanMode
from app.services.robot_service import RobotService

class TestRobotService(unittest.TestCase):
    def setUp(self):
        self.robot_service = RobotService()

    def test_turn_on(self):
        self.assertTrue(self.robot_service.turn_on())
        self.assertEqual(self.robot_service.status, RobotStatus.RUNNING)

    def test_turn_off(self):
        self.robot_service.turn_on()
        self.assertTrue(self.robot_service.turn_off())
        self.assertEqual(self.robot_service.status, RobotStatus.OFFLINE)

    def test_calculate_fan_speed(self):
        self.robot_service.status = RobotStatus.RUNNING
        fan_speed = self.robot_service.calculate_fan_speed(16.5)
        self.assertTrue(60 <= fan_speed <= 100)

    def test_get_state(self):
        self.robot_service.turn_on()
        state = self.robot_service.get_state()
        self.assertEqual(state.status, RobotStatus.RUNNING)
        self.assertGreater(state.power, 0)
        self.assertGreater(state.fan_speed, 0)

    def test_fan_mode_required_for_fan_action(self):
        with self.assertRaises(ValueError):
            self.robot_service.fan_mode = None
            self.robot_service.get_state()
            
