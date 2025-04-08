export interface RobotStateData {
  temperature: number;
  power: number;
  status: string;
  fan_speed: number;
  uptime: number;
}

export enum FanMode {
  STATIC = "static",
  PROPORTIONAL = "proportional"
}

export enum RobotAction {
  ON = "on",
  OFF = "off",
  RESET = "reset",
  FAN = "fan",
}

export interface RobotControlCommand {
  action: RobotAction;
  fan_mode?: FanMode;
}
