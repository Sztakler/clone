import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { RobotStateData } from './types/types';

import './App.css';


function App() {
  return (
    <div className="App">
      <RobotState />
    </div>
  );
}

function RobotState() {
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
    <div>
      <h1>Robot State</h1>
      <p>Status: {state?.status}</p>
      <p>Temperature: {state?.temperature}</p>
      <p>Fan speed: {state?.fan_speed}</p>
      <p>Power: {state?.power}</p>
      <p>Uptime: {state?.uptime}</p>
    </div>
  )
}

export default App;
