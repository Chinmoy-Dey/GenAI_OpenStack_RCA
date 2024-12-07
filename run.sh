#!/bin/bash

# Configurable parameters
UVICORN_HOST="0.0.0.0"
UVICORN_PORT=8000
UVICORN_CMD="uvicorn ui.api:app --reload --host $UVICORN_HOST --port $UVICORN_PORT"
PYTHON_SCRIPT="python3 ui/app.py"
REQUIREMENTS_FILE="requirements.txt"
LOG_FILE="service_startup.log"

# Function to log messages
log_message() {
    local message=$1
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" | tee -a "$LOG_FILE"
}

# Function to check if a command is available
is_command_installed() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python and Docker if not installed
install_prerequisites() {
    log_message "Checking for prerequisites..."
    
    # Check and install Python
    if ! is_command_installed python3; then
        log_message "Python3 is not installed. Installing Python3..."
        sudo apt update -y && sudo apt install -y python3 python3-pip
        if [ $? -ne 0 ]; then
            log_message "Failed to install Python3. Exiting."
            exit 1
        fi
        log_message "Python3 installed successfully."
    else
        log_message "Python3 is already installed."
    fi

    # Check and install Docker
    if ! is_command_installed docker; then
        log_message "Docker is not installed. Installing Docker..."
        sudo apt update -y && sudo apt install -y docker.io
        if [ $? -ne 0 ]; then
            log_message "Failed to install Docker. Exiting."
            exit 1
        fi
        sudo systemctl start docker && sudo systemctl enable docker
        log_message "Docker installed and started successfully."
    else
        log_message "Docker is already installed."
    fi

    # Install dependencies from requirements.txt
    if [ -f "$REQUIREMENTS_FILE" ]; then
        log_message "Installing dependencies from $REQUIREMENTS_FILE..."
        python3 -m pip install --upgrade pip
        python3 -m pip install -r "$REQUIREMENTS_FILE"
        if [ $? -ne 0 ]; then
            log_message "Failed to install dependencies from $REQUIREMENTS_FILE. Exiting."
            exit 1
        fi
        log_message "Dependencies installed successfully."
    else
        log_message "$REQUIREMENTS_FILE not found. Skipping dependency installation."
    fi
}

# Function to check if a port is in use
is_port_in_use() {
    lsof -i:$1 -t >/dev/null 2>&1
}

# Function to terminate process using a port
terminate_port() {
    local port=$1
    log_message "Checking if port $port is in use..."
    if is_port_in_use $port; then
        log_message "Port $port is in use. Attempting to terminate the process..."
        lsof -i:$port -t | xargs kill -9 >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            log_message "Successfully terminated the process using port $port."
        else
            log_message "Failed to terminate the process on port $port. Exiting."
            exit 1
        fi
    else
        log_message "Port $port is not in use."
    fi
}

# Exit handler to clean up
cleanup() {
    log_message "Script is exiting. Cleaning up..."
    terminate_port $UVICORN_PORT
    log_message "Cleanup completed."
}
trap cleanup EXIT

# Check and install prerequisites
install_prerequisites

# Check and handle port conflict for Uvicorn
terminate_port $UVICORN_PORT

# Start Uvicorn
log_message "Starting Uvicorn on $UVICORN_HOST:$UVICORN_PORT..."
$UVICORN_CMD &
UVICORN_PID=$!
if [ $? -ne 0 ]; then
    log_message "Failed to start Uvicorn. Exiting."
    exit 1
fi
log_message "Uvicorn started with PID $UVICORN_PID."

# Start Python script
log_message "Starting Python script..."
$PYTHON_SCRIPT &
PYTHON_PID=$!
if [ $? -ne 0 ]; then
    log_message "Failed to start Python script. Exiting."
    kill -9 $UVICORN_PID
    exit 1
fi
log_message "Python script started with PID $PYTHON_PID."

# Wait for child processes to terminate
wait $UVICORN_PID
UVICORN_EXIT_CODE=$?
log_message "Uvicorn exited with code $UVICORN_EXIT_CODE."

wait $PYTHON_PID
PYTHON_EXIT_CODE=$?
log_message "Python script exited with code $PYTHON_EXIT_CODE."

log_message "Both Uvicorn and Python script have terminated."
