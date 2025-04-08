import './App.css';
import RobotState from './components/RobotState';
import RobotControls from './components/RobotControls';
import LogsMonitor from './components/LogsMonitor';

function App() {
  return (
    <div className="container">
      <div className="item A">
        <RobotState />
      </div>
      <div className="item B">
        <RobotControls />
      </div>
      <div className="item C">
        <LogsMonitor />
      </div>
    </div>
  );
}

export default App;
