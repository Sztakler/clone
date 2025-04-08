import { useState, useEffect } from "react";
import axios from "axios";
import { RobotStateData } from "../types/types";

import "./RobotState.css"

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
    <div className="container">
      <h1>Robot State</h1>
      <ul>
      <li>Status: {state?.status}</li>
      <li>Temperature: {state?.temperature}°C</li>
      <li>Fan speed: {state?.fan_speed}%</li>
      <li>Power: {state?.power}W</li>
      <li>Uptime: {state?.uptime}s</li>
      </ul>
    </div>
  )
}
