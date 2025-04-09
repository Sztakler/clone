import { render, screen, waitFor } from '@testing-library/react';
import RobotState from '../components/RobotState';
import axios from 'axios';
import { act } from 'react';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('RobotState Component', () => {
  it('should display robot state after data is fetched', async () => {
    const mockState = {
      status: 'online',
      temperature: 25,
      fan_mode: 'PROPORTIONAL',
      fan_speed: 50,
      power: 100,
      uptime: 3600,
    };

    mockedAxios.get.mockResolvedValueOnce({ data: mockState });

    await act(async () => {
      render(<RobotState />);
    })

    await waitFor(() => expect(screen.getByText(/online/i)).toBeInTheDocument());
    expect(screen.getByText(/25°C/i)).toBeInTheDocument();
    expect(screen.getByText(/PROPORTIONAL/i)).toBeInTheDocument();
    expect(screen.getByText(/50%/i)).toBeInTheDocument();
    expect(screen.getByText(/100W/i)).toBeInTheDocument();
    expect(screen.getByText(/3600s/i)).toBeInTheDocument();
  });

  it('should display error message if fetching data fails', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Network error'));
    await act(async () => {
      render(<RobotState />);
    })

    await waitFor(() => expect(screen.getByText(/Error fetching robot state/i)).toBeInTheDocument());
  });
});

