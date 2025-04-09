import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axios from "axios";
import { FanMode, RobotStateData } from "../types/types";
import RobotControls from "../components/RobotControls";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("RobotControls", () => {
  const mockState: RobotStateData = {
    status: "running",
    uptime: 1234,
    fan_mode: FanMode.PROPORTIONAL,
    fan_speed: 30,
    temperature: 30,
    power: 16,
  }

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders and fetches state", async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: mockState });

    render(<RobotControls />);
    await waitFor(() => {
      expect(mockedAxios.get).toHaveBeenCalledWith("http://localhost:8000/state");
    });

    expect(screen.getByText(/Robot Controls/i)).toBeInTheDocument();
    expect(screen.getByText(/Reset/i)).toBeInTheDocument();
  });

  it("shows error if fetch fails", async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error("💥 fail"));

    render(<RobotControls />);
    await waitFor(() => {
      expect(screen.getByText(/Error fetching robot state/i)).toBeInTheDocument();
    });
  });

  it("calls sendCommand on power toggle", async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: mockState });
    mockedAxios.post.mockResolvedValueOnce({});

    render(<RobotControls />);
    await waitFor(() => screen.getByText(/Turn OFF/));

    const button = screen.getByText(/Turn OFF/);
    await userEvent.click(button);

    expect(mockedAxios.post).toHaveBeenCalledWith("http://localhost:8000/control", {
      action: "off",
    });
  });

  it("calls sendCommand on reset", async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: mockState });
    mockedAxios.post.mockResolvedValueOnce({});

    render(<RobotControls />);
    await waitFor(() => screen.getByText(/Reset/));

    const button = screen.getByText(/Reset/);
    await userEvent.click(button);

    expect(mockedAxios.post).toHaveBeenCalledWith("http://localhost:8000/control", {
      action: "reset",
    });
  });

  it("sets fan mode", async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: mockState });
    mockedAxios.post.mockResolvedValue({});

    render(<RobotControls />);
    await waitFor(() => screen.getByText(/Set mode/));

    const select = screen.getByRole("combobox");
    const button = screen.getByText(/Set mode/);

    await userEvent.selectOptions(select, FanMode.STATIC);
    await userEvent.click(button);

    expect(mockedAxios.post).toHaveBeenCalledWith("http://localhost:8000/control", {
      action: "fan",
      fan_mode: FanMode.STATIC,
    });
  });
  it("sets fan speed", async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: { ...mockState, fan_mode: FanMode.STATIC },
    });
    mockedAxios.post.mockResolvedValue({});

    render(<RobotControls />);
    await waitFor(() => screen.getByText(/Set speed/));

    const fanModeSelect = screen.getByLabelText(/Fan Mode/i);
    fireEvent.change(fanModeSelect, { target: { value: FanMode.STATIC } });

    const setModeBtn = screen.getByText(/Set mode/i);
    await userEvent.click(setModeBtn);

    const range = screen.getByRole("slider");
    const button = screen.getByText(/Set speed/);

    fireEvent.change(range, { target: { value: 80 } });
    await userEvent.click(button);

    await waitFor(() =>
      expect(mockedAxios.post).toHaveBeenCalledWith("http://localhost:8000/control", {
        action: "fan_speed",
        fan_speed: 80,
      })
    );
  });

});

