#!/bin/bash

# Define the path to the directory containing the Dockerfile
DOCKERFILE_DIR="/home/ec2-user/chatbot-docker"

# Define the name for your Docker image
IMAGE_NAME="aidoctor3:Hafsa-chatbot3"

# Navigate to the directory containing the Dockerfile
cd "$DOCKERFILE_DIR" || exit

# Build the Docker image
docker build -t "$IMAGE_NAME" .

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image $IMAGE_NAME built successfully."
else
    echo "Failed to build Docker image $IMAGE_NAME."
fi
