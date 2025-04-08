import { useState, useEffect } from "react";
import axios from "axios";
import { FanMode, RobotAction, RobotControlCommand } from "../types/types";

import styles from "./RobotControls.module.css"

export default function RobotControls() {
  const [status, setStatus] = useState<string | null>(null);
  const [fanMode, setFanMode] = useState<FanMode>(FanMode.PROPORTIONAL);
  const [fanSpeed, setFanSpeed] = useState<number>(0);
  const [powerOn, setPowerOn] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    axios.get("http://localhost:8000/status")
      .then(res => setStatus(res.data.status))
      .catch(err => setError(err));
  }, []);

  const sendCommand = async (command: RobotControlCommand) => {
    try {
      const response = await axios.post("http://localhost:8000/control", command);
      console.log('Success:', response.data);
    } catch (err) {
      console.error("Error sending command:", err);
      setError("Error sending command");
    }
  }

  const handleTurnOn = () => {
    const command: RobotControlCommand = { action: RobotAction.ON };
    sendCommand(command);
  };

  const handleTurnOff = () => {
    const command: RobotControlCommand = { action: RobotAction.OFF };
    sendCommand(command);
  };
  const handleReset = () => {
    const command: RobotControlCommand = { action: RobotAction.RESET };
    sendCommand(command);
  };
  const handleSetFanMode = async () => {
    const command: RobotControlCommand = { action: RobotAction.FAN, fan_mode: fanMode };
    try{
      setLoading(true);
      sendCommand(command);
      console.log("Fan speed changed.")
    } catch (err) {
      console.error("Error changing fan speed: ", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSetFanSpeed = () => {
    const command: RobotControlCommand = {
      action: RobotAction.FAN_SPEED, fan_speed: fanSpeed
    };
    sendCommand(command);
  }

  return (
    <div className={styles.container}>
      <div>
        <h2>Robot Controls</h2>
        <div className={styles.controlButtons}>
          <button onClick={handleTurnOn}>Turn ON</button>
          <button onClick={handleTurnOff}>Turn OFF</button>
          <button onClick={handleReset}>Reset</button>
        </div>
      </div>

      <div className={styles.fanModeSelect}>
        <label>Fan Mode</label>
        <select
          value={fanMode}
          onChange={(e) => setFanMode(e.target.value as FanMode)}
        >
          <option value={FanMode.PROPORTIONAL}> Proportional</option>
          <option value={FanMode.STATIC}> Static</option>
        </select>
        <button onClick={handleSetFanMode}>Set Fan Mode</button>
      </div>

      <div>
        <label>Fan Speed:</label>
        <input type="range" min="0" max="100" value={fanSpeed} onChange={(e) => setFanSpeed(Number(e.target.value))}/>
        <span>{fanSpeed}%</span>
        <button onClick={handleSetFanSpeed} disabled={loading}>
          {loading ? "Changing..." : "Set Fan Speed"}
          </button>
        </div>
    </div >
  );

}
