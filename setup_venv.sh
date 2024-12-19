#!/bin/bash

VENV_NAME="capstone-grp1"
VENV_STATE_FILE=".venv_state"  # This file will track the existence of the venv

# Function to create and activate virtual environment
create_and_activate_venv() {
    # Check if the virtual environment state file exists
    if [ ! -f "$VENV_STATE_FILE" ]; then
        echo "Virtual environment state not found. Creating the virtual environment..."
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "$VENV_NAME" ]; then
            python3 -m venv $VENV_NAME
            echo "Virtual environment '$VENV_NAME' created."
        fi
        
        # Mark the virtual environment as created by creating the state file
        touch $VENV_STATE_FILE
        echo "Virtual environment state file created."
    else
        echo "Virtual environment already created. Using it..."
    fi

    # Show the activation command for the user
    if [ -f "$VENV_NAME/bin/activate" ]; then
        # For Linux/macOS
        source $VENV_NAME/bin/activate
    elif [ -f "$VENV_NAME\\Scripts\\activate.bat" ]; then
        # For Windows (assuming you are using a command prompt or PowerShell)
        $VENV_NAME\\Scripts\\activate.bat
    fi
}

# Function to check if venv is activated
check_venv_activated() {
    which python3
    # Check if the VIRTUAL_ENV environment variable is set
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Virtual environment is NOT activated."
        return 1  # Return non-zero if venv is not activated
    else
        echo "Virtual environment is activated: $VIRTUAL_ENV"
        return 0  # Return 0 if venv is activated
    fi
}

# Check if python3.8-venv is installed
if ! dpkg-query -l | grep -q python3.8-venv; then
    echo "Package python3.8-venv is not installed. Installing..."
    sudo apt update && sudo apt install -y python3.8-venv
else
    echo "Package python3.8-venv is already installed."
fi
