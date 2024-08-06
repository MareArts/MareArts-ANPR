#!/bin/bash

set -e

CONTAINER_NAME="marearts-anpr-fastapi-amd64"
PORT=8000

# Stop and remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping and removing existing container..."
    docker rm -f ${CONTAINER_NAME}
fi

# Run the container
echo "Starting the container..."
    docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${CONTAINER_NAME}:latest


echo "Container started successfully!"
echo "API is available at http://localhost:${PORT}"
