import { useState, useEffect } from "react";
import axios, { CanceledError } from "axios";
import { FanMode, RobotAction, RobotControlCommand, RobotStateData } from "../types/types";

import styles from "./RobotControls.module.css"
import RobotState from "./RobotState";

export default function RobotControls() {
  const [state, setState] = useState<RobotStateData | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [fanMode, setFanMode] = useState<FanMode>(FanMode.PROPORTIONAL);
  const [fanSpeed, setFanSpeed] = useState<number>(0);
  const [powerOn, setPowerOn] = useState<boolean>(true);
  const [controlError, setControlError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [disabledSetSpeed, setDisabledSetSpeed] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchState() {
    try {
      const response = await axios.get<RobotStateData>('http://localhost:8000/state');
      setState(response.data);
      setLoading(false);
      if (response.data.status === "offline")
        setPowerOn(false);
    } catch (err) {
      setError('Error fetching robot state');
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchState();
  }, []);

  const sendCommand = async (command: RobotControlCommand) => {
    try {
      const response = await axios.post("http://localhost:8000/control", command);
      console.log('Success:', response.data);
    } catch (err: any) {
      console.error("Error sending command:", err);
      setControlError("Error sending command " + err.message);
    }
  }

  const handleTogglePower = () => {
    const command: RobotControlCommand = {
      action: powerOn ? RobotAction.OFF : RobotAction.ON
    }
    setPowerOn(!powerOn);
    sendCommand(command);
  }

  const handleReset = () => {
    const command: RobotControlCommand = { action: RobotAction.RESET };
    sendCommand(command);
  };

  const handleSetFanMode = async () => {
    const command: RobotControlCommand = { action: RobotAction.FAN, fan_mode: fanMode };
    try {
      setLoading(true);
      sendCommand(command);
      console.log("Fan speed changed.")
    } catch (err: any) {
      setControlError("Error changing fan speed")
      console.error("Error changing fan speed: ", err.message);
    } finally {
      if (command.fan_mode === FanMode.STATIC)
        setDisabledSetSpeed(false);
      else
        setDisabledSetSpeed(true)
      setLoading(false);
    }
  };

  const handleSetFanSpeed = () => {
    const command: RobotControlCommand = {
      action: RobotAction.FAN_SPEED, fan_speed: fanSpeed
    };
    sendCommand(command);
  }

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className={styles.container}>
      <div>
        <h2>Robot Controls</h2>
        <div className={styles.controlButtons}>
          <button onClick={handleTogglePower}>
            {powerOn ? "Turn OFF" : "Turn ON"}
          </button>
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
        <button onClick={handleSetFanMode}>Set mode</button>
      </div>

      <div>
        <label>Fan Speed:</label>
        <input type="range" min="0" max="100" value={fanSpeed} onChange={(e) => setFanSpeed(Number(e.target.value))} />
        <span>{fanSpeed}%</span>
        <button onClick={handleSetFanSpeed} disabled={disabledSetSpeed}>
          Set speed
        </button>
      </div>

    </div >
  );

}
