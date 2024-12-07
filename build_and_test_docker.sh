#!/bin/bash

# Define variables
IMAGE_NAME="anomaly-detector-rca-app"
CONTAINER_NAME="anomaly-detector-rca_container"
DOCKERFILE_PATH="."
PORT_8000=8000
PORT_7860=7860
API_URL="http://localhost:$PORT_8000"

# Helper function to handle cleanup on exit
cleanup() {
  echo "Cleaning up resources..."
  docker stop $CONTAINER_NAME >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Helper function to exit on error
check_status() {
  if [ $1 -ne 0 ]; then
    echo "Error: $2"
    exit 1
  fi
}

# Step 1: Check and install dependencies
check_docker_installed() {
  echo "Checking Docker installation..."
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed. Attempting to install Docker..."
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update && sudo apt-get install -y docker.io
    elif command -v yum >/dev/null 2>&1; then
      sudo yum install -y docker
    else
      echo "Unsupported package manager. Please install Docker manually."
      exit 1
    fi
  fi
}

check_docker_running() {
  echo "Checking if Docker daemon is running..."
  if ! docker info >/dev/null 2>&1; then
    echo "Docker daemon is not running. Attempting to start it..."
    if command -v systemctl >/dev/null 2>&1; then
      sudo systemctl start docker || { echo "Failed to start Docker using systemctl."; exit 1; }
    elif command -v service >/dev/null 2>&1; then
      (sudo service docker stop && sudo service docker start ) || { echo "Failed to start Docker using service."; exit 1; }
    else
      echo "System does not use systemd or service. Attempting to start dockerd directly..."
      nohup sudo dockerd >/dev/null 2>&1 &
      sleep 5
    fi

    docker info >/dev/null 2>&1 || { echo "Docker daemon is still not running. Please resolve the issue and try again."; exit 1; }
  fi
}

fix_docker_socket_permissions() {
  echo "Checking Docker socket permissions..."
  if [ ! -w /var/run/docker.sock ]; then
    echo "Fixing permissions for Docker socket..."
    sudo chmod 666 /var/run/docker.sock || { echo "Failed to update permissions for Docker socket."; exit 1; }
  fi
}

# Step 2: Build Docker image
build_docker_image() {
  echo "Building Docker image..."
  docker build -t $IMAGE_NAME $DOCKERFILE_PATH
  check_status $? "Docker build failed."
}

# Step 3: Check port availability
check_ports() {
  echo "Checking port availability..."
  if lsof -i:$PORT_8000 -t >/dev/null 2>&1; then
    echo "Port $PORT_8000 is already in use. Please free the port and try again."
    exit 1
  fi

  if lsof -i:$PORT_7860 -t >/dev/null 2>&1; then
    echo "Port $PORT_7860 is already in use. Please free the port and try again."
    exit 1
  fi
}

# Step 4: Run Docker container
run_docker_container() {
  echo "Running Docker container..."
  docker run -d --rm --name $CONTAINER_NAME -p $PORT_8000:$PORT_8000 -p $PORT_7860:$PORT_7860 $IMAGE_NAME
  check_status $? "Failed to run the Docker container."
}

# Step 5: Test endpoints
test_endpoints() {
  echo "Testing FastAPI endpoints..."

  curl -X POST "$API_URL/predict" -H "Content-Type: application/json" -d '{"log": "Success"}'
  check_status $? "Test 1 (Predict Success) failed."

  curl -X POST "$API_URL/predict" -H "Content-Type: application/json" -d '{"log": "Failure"}'
  check_status $? "Test 2 (Predict Failure) failed."

  curl -X POST "$API_URL/root_cause_analysis" -H "Content-Type: application/json" -d '{"logs": ["openstack log with error", "app log entry", "Timeout occurred"]}'
  check_status $? "Test 3 (Root Cause Analysis) failed."

  echo "All tests passed."
}

 build_docker_compose() {
  local compose_file_path="${1:-docker-compose.yml}"  # Default to docker-compose.yml
  local project_name="${2}"  # Optional project name

  # Build the Docker Compose project
  docker compose -f "$compose_file_path" build ${project_name:+-p "$project_name"}
  # check_status $? "Failed to build Docker Compose project."
  check_status $? "Error building Docker Compose project."

}

check_wsl_and_exit() {
  if [[ -f /proc/sys/kernel/osrelease ]]; then
    if grep -iq "WSL" /proc/sys/kernel/osrelease; then
      echo "Error: This script is not intended to be run within WSL."
      exit 1
    fi
  fi
}

# Main function
main() {
  check_wsl_and_exit
  check_docker_installed
  check_docker_running
  fix_docker_socket_permissions
  check_ports
  build_docker_image
  build_docker_compose
  run_docker_container

  echo "Waiting for the services to start..."
  sleep 10
  test_endpoints
}

# Execute the main function
main
