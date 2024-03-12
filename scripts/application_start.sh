#!/bin/bash

# Define the name for your Docker container
CONTAINER_NAME="mystifying_rubin"

# Define the name of the Docker image
IMAGE_NAME="aidoctor3:Hafsa-chatbot3"

# Define any additional options you want to pass to `docker run`
# For example, you can specify ports, volumes, environment variables, etc.
# Add them to the following OPTIONS variable
OPTIONS="-d -p 3012:3012" # Example: run in detached mode, map port 8080 on host to port 80 in container

# Run the Docker container
docker run $OPTIONS --name "$CONTAINER_NAME" "$IMAGE_NAME"

# Check if the container is running
if [ $(docker ps -q -f name="$CONTAINER_NAME") ]; then
    echo "Container $CONTAINER_NAME is running."
else
    echo "Failed to start container $CONTAINER_NAME."
fi
