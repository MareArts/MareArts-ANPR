#!/bin/bash

set -e

# Auto-detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
    IMAGE_NAME="marearts-anpr-fastapi-amd64"
    ARCH_NAME="AMD64 (x86_64)"
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    IMAGE_NAME="marearts-anpr-fastapi-arm64"
    ARCH_NAME="ARM64 (aarch64)"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

CONTAINER_NAME="${IMAGE_NAME}"
PORT=8000

echo "Detected architecture: $ARCH_NAME"
echo "Using image: $IMAGE_NAME"

# Stop and remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping and removing existing container..."
    docker rm -f ${CONTAINER_NAME}
fi

# Run the container
echo "Starting the container..."
docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${IMAGE_NAME}:latest

echo "Container started successfully!"
echo "API is available at http://localhost:${PORT}"