# Robot Monitoring and Control App

A full-stack application for monitoring and controlling a robot using an HTTP-based API, built with FastAPI (backend) and React (frontend). WebSockets are also implemented in the backend for extensibility, though the frontend currently communicates via HTTP as per the spec.

---

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

## 🧠 Project Decisions

This section highlights important architectural and design decisions made during the development of the project.

- **Stateless Backend**: Logs and robot state are not stored in global variables or shared memory. Instead, a logging mechanism is used to persist logs, and robot state is managed through a dedicated `RobotService` class.
- **Logging over State**: Instead of holding logs in memory or the app state, Python’s built-in `logging` is used for simplicity and scalability.
- **WebSockets Ready**: Although the frontend uses HTTP polling (as specified), WebSocket support is fully implemented and ready for use in the backend.
- **Strict Modularity**: The backend is structured with clear separation between routers, services, and core logic. The frontend follows a component-based structure for clarity and maintainability.
- **CORS Configuration**: The backend is set up to handle cross-origin requests during local development using FastAPI’s middleware.


## 🚀 Setup

### 🔧 Local Development (without Docker)

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

---

### 🐳 Docker-Based Development

To run the application with Docker, you'll need to build and start the containers using Docker Compose.

1. Make sure you have Docker and Docker Compose installed.

2. Clone the repository:
    ```bash
    git clone https://github.com/Sztakler/clone
    ```

3. Navigate to the `backend` directory and build the container:
    ```bash
    cd backend
    docker-compose up --build
    ```
4. Navigate to the `frontend` directory and build the container:
    ```bash
    cd frontend
    docker-compose up --build
    ```

5. This will start both the backend and frontend containers. The application will be accessible at `http://localhost:3000`.

6. To shut down the container:
    ```bash
    docker-compose down
    ```

## 🧪 Testing

### Backend

Backend uses `pytest` for tests. To run them:

```bash
cd backend
pip install -r requirements.txt
pytest
````

### Frontend

Frontend uses 'jest' for tests. To run them:

```bash
cd frontend
npm install
npm test
```

## ⚡ WebSocket Support

WebSocket support is partially implemented in the backend and works for most use cases. It was initially developed to provide proper real-time updates, which would be more suitable for this kind of robot control app. However, the final implementation uses HTTP polling instead, as per the project specification requirements. 

## ⚙️ Configuration and Environment

- **Default Ports**:
  - **Backend**: runs on `5487`
  - **Frontend**: runs on `3000`
  - You can change them by editing the `.env` files in `backend/.env` and `frontend/.env` respectively.

- **.env Setup**:
  - Each part of the app can be configured with environment variables using a `.env` file.
  - Example `.env` file for the **backend** (`backend/.env`):
    ```env
    PORT=5487
    ENV=development
    ```
  - Example `.env` file for the **frontend** (`frontend/.env`):
    ```env
    REACT_APP_PORT=3000
    ```

  These values are automatically loaded by Docker Compose or can be used manually when running the app locally.

