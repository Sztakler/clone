import './App.css';
import RobotState from './components/RobotState';
import RobotControls from './components/RobotControls';
import LogsMonitor from './components/LogsMonitor';

function App() {
  return (
    <div className="container">
      <div className="row">
        <div className="item">
          <RobotState />
        </div>
        <div className="item">
          <RobotControls />
        </div>
      </div>
    <div className="row">
      <div className="item">
        <LogsMonitor />
      </div>
    </div>
    </div>
  );
}

export default App;
