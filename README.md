# Robot Monitoring and Control App

This project is designed to monitor and control a robot through a web interface. The backend is built with FastAPI, while the frontend uses React. WebSockets are implemented but not used by the application, as the specification required using HTTP for communication.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup](#setup)
  - [Running Without Docker](#running-without-docker)
  - [Running With Docker](#running-with-docker)
- [Testing](#testing)
- [Project Design Decisions](#project-design-decisions)
- [Notes](#notes)

## Project Overview

The goal of this project is to create a simple, functional interface to control and monitor the state of a robot. The backend provides an API to retrieve the robot's state and logs, control the fan speed, and toggle the robot's power. The frontend displays this data and allows the user to interact with the robot.

## Setup

### Running Without Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/Sztakler/clone
    ```
2. Set up a virtual environment for the backend:
    - Install `venv` if you don't have it:
        ```bash
        python3 -m pip install --user virtualenv
        ```
    - Create and activate a virtual environment:
        ```bash
        python3 -m venv venv
        source venv/bin/activate  # On Windows use: venv\Scripts\activate
        ```

3. Install the backend dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4. Start the backend server:
    ```bash
    python app/main.py
    ```
    - Server can be configured using CLI options:
      ```txt
      -h, --help            show this help message and exit
      --host HOST           Host for the server
      --port PORT           Port for the server
      --log-level LOG_LEVEL
                            Log level for the application
      --refresh-rate REFRESH_RATE
                            Frequency of state updates in Hz (default 10Hz)
      ````
    - Example:
    ```bash
    python app/main.py --refresh-rate=10
    ```

5. Install the frontend dependencies:
    ```bash
    cd frontend
    npm install
    ```

6. Start the frontend development server:
    ```bash
    npm start
    ```


Now you can access the application in your browser at `http://localhost:3000`.

### Running With Docker

To run the application with Docker, you'll need to build and start the containers using Docker Compose.

1. Make sure you have Docker and Docker Compose installed.

2. Clone the repository:
    ```bash
    git clone https://github.com/Sztakler/clone
    ```

3. Navigate to the project root and build the containers:
    ```bash
    docker-compose up --build
    ```

4. This will start both the backend and frontend containers. The application will be accessible at `http://localhost:3000`.

5. To shut down the containers:
    ```bash
    docker-compose down
    ```

## Testing

To run tests for the backend, you can use `pytest`. Install the testing dependencies and run:

```bash
cd backend
pip install -r requirements.txt
pytest

