#!/bin/bash

set -e

# Ensure Docker BuildX is available
if ! docker buildx version > /dev/null 2>&1; then
    echo "Docker BuildX is not available. Please install it first."
    exit 1
fi

# Create a BuildX builder if it doesn't exist
if ! docker buildx inspect mybuilder > /dev/null 2>&1; then
    echo "Creating a new BuildX builder..."
    docker buildx create --name mybuilder --use
fi

# Build the image locally
#multi platform
docker buildx build --platform linux/amd64 -t marearts-anpr-fastapi-amd64:latest .
# docker buildx build --platform linux/arm64 -t marearts-anpr-fastapi-arm64:latest .

echo "Build completed successfully!"