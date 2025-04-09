import argparse
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    parser = argparse.ArgumentParser(description="Robot Service Configuration")

    parser.add_argument("--host", default=os.getenv("HOST", "localhost"), help="Host for the server")
    parser.add_argument("--port", default=int(os.getenv("PORT", 5487)), type=int, help="Port for the server")
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "info"), help="Log level for the application")
    parser.add_argument("--refresh-rate", default=int(os.getenv("REFRESH_RATE", 10)), type=int, help="Frequency of state updates in Hz (default 10Hz)")
    return parser.parse_args()

config = load_config()

print(f"Server will run on {config.host}:{config.port} with log level {config.log_level}, refresh rate {config.refresh_rate}Hz")

