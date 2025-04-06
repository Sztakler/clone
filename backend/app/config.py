import argparse

def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="2137", type=int)
    parser.add_argument("--log-level", default="info")

    return parser.parse_args()

config = load_config()
