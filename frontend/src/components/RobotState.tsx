import { useState, useEffect } from "react";
import axios from "axios";
import { RobotStateData } from "../types/types";

import styles from "./RobotState.module.css"

export default function RobotState() {
  const [state, setState] = useState<RobotStateData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchState() {
    try {
      const response = await axios.get<RobotStateData>('http://localhost:8000/state');
      setState(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error fetching robot state');
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 100);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className={styles.container}>
      <h2>Robot State</h2>
      <ul>
        <li>
          <div>Status:</div>
          <div>{state?.status}</div>
        </li>
        <li>
          <div>Temperature:</div>
          <div>{state?.temperature}°C</div>
        </li>
        <li>
          <div>Fan speed:</div><div>{state?.fan_speed}%</div>
        </li>
        <li>
          <div>Power:</div>
          <div>{state?.power}W</div>
        </li>
        <li>
          <div>Uptime:</div>
          <div>{state?.uptime}s</div>
        </li>
      </ul>
    </div>
  )
}
