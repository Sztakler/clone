import { useEffect, useState } from "react";
import axios from "axios";

export default function LogsMonitor() {
  const [logs, setLogs] = useState<string>("");

  useEffect(() => {
    const fetchLogs = async () => {
      const response = await axios.get("http://localhost:8000/logs");
      setLogs(response.data);
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 1000); // co sekundę

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="logs">
      <h2>Robot Logs</h2>
      <pre>{logs}</pre>
    </div>
  );
}

