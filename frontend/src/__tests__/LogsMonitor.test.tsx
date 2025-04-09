import { render, screen, waitFor } from '@testing-library/react';
import LogsMonitor from '../components/LogsMonitor';
import axios from 'axios';
import { act } from 'react';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('LogsMonitor Component', () => {
  it('should display logs after fetching data', async () => {
    const mockLogs = 'Log 1: Robot started\nLog 2: Robot running\nLog 3: Robot stopped';
    
    mockedAxios.get.mockResolvedValueOnce({ data: mockLogs });

    await act(async () => {
      render(<LogsMonitor />);
    });

    await waitFor(() => expect(screen.getByText(/Robot Logs/i)).toBeInTheDocument());
    expect(screen.getByText(/Log 1: Robot started/)).toBeInTheDocument();
    expect(screen.getByText(/Log 2: Robot running/)).toBeInTheDocument();
    expect(screen.getByText(/Log 3: Robot stopped/)).toBeInTheDocument();
  });

  it('should display an error message if fetching logs fails', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Network error'));

    await act(async () => {
      render(<LogsMonitor />);
    });

    await waitFor(() => expect(screen.getByText(/Error fetching robot logs/i)).toBeInTheDocument());
  });

  it('should update logs every second', async () => {
    const mockLogs1 = 'Log 1: Robot started';
    const mockLogs2 = 'Log 1: Robot started\nLog 2: Robot running';

    mockedAxios.get.mockResolvedValueOnce({ data: mockLogs1 });
    mockedAxios.get.mockResolvedValueOnce({ data: mockLogs2 });

    await act(async () => {
      render(<LogsMonitor />);
    });

    await waitFor(() => expect(screen.getByText(/Robot Logs/i)).toBeInTheDocument());
    expect(screen.getByText(/Log 1: Robot started/)).toBeInTheDocument();

    // Simulate the next fetch after 1 second
    mockedAxios.get.mockResolvedValueOnce({ data: mockLogs2 });
    await waitFor(() => expect(screen.getByText(/Log 2: Robot running/)).toBeInTheDocument());
  });
});

