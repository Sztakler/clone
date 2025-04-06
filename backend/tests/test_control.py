from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_control_robot_turn_on():
    response = client.post("/control", json={"action": "on"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "action": "on"}

def test_control_robot_turn_off():
    response = client.post("/control", json={"action": "off"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "action": "off"}

def test_control_robot_invalid_action():
    response = client.post("/control", json={"action": "invalid_action"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'enum', 'loc': ['body', 'action'], 'msg': "Input should be 'on', 'off', 'reset' or 'fan'", 'input': 'invalid_action', 'ctx': {'expected': "'on', 'off', 'reset' or 'fan'"}}]}

def test_fan_action_requires_fan_mode():
    response = client.post("/control", json={"action": "fan"})
    assert response.status_code == 422  # Unprocessable Entity
    assert "fan_mode is required" in response.json()["detail"]
