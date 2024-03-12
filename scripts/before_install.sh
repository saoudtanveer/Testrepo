#!/bin/bash

# Define the name of the Docker container to be stopped and removed
CONTAINER_NAME="mystifying_rubin"

# Check if the container is running
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    # Stop the container
    docker stop "$CONTAINER_NAME"

    # Remove the container
    docker rm "$CONTAINER_NAME"

    echo "Container $CONTAINER_NAME stopped and removed."
else
    echo "Container $CONTAINER_NAME is not running."
fi
