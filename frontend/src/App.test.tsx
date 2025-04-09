import { render, screen } from '@testing-library/react';
import App from './App';

// Mocking the components to avoid their internal logic running in this test
jest.mock('./components/RobotState', () => () => <div>Robot State</div>);
jest.mock('./components/RobotControls', () => () => <div>Robot Controls</div>);
jest.mock('./components/LogsMonitor', () => () => <div>Logs Monitor</div>);

describe('App Component', () => {
  it('should render RobotState component', () => {
    render(<App />);
    expect(screen.getByText(/Robot State/i)).toBeInTheDocument();
  });

  it('should render RobotControls component', () => {
    render(<App />);
    expect(screen.getByText(/Robot Controls/i)).toBeInTheDocument();
  });

  it('should render LogsMonitor component', () => {
    render(<App />);
    expect(screen.getByText(/Logs Monitor/i)).toBeInTheDocument();
  });

  it('should render the app without crashing', () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    render(<App />);
    consoleErrorSpy.mockRestore();
  });
});

