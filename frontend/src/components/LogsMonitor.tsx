import { useEffect, useState } from "react";
import axios from "axios";

import styles from "./LogsMonitor.module.css"

const apiUrl = process.env.REACT_APP_API_URL;

export default function LogsMonitor() {
  const [logs, setLogs] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await axios.get(`${apiUrl}/logs`);
        setLogs(response.data);
      }
      catch (err: any) {
        setError("Error fetching robot logs")
      }

    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 1000); // co sekundę

    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (<div>{error}</div>)
  }

  return (
    <div className={styles.logs}>
      <h2>Robot Logs</h2>
      <pre>{logs}</pre>
    </div>
  );
}

