#!/bin/bash

# Deployment script for Flowise Telegram Bot
# This script can be customized for your specific deployment environment

set -e

# Configuration
IMAGE_NAME="${IMAGE_NAME:-ghcr.io/your-username/flowise-telegram-bot}"
TAG="${TAG:-latest}"
ENVIRONMENT="${ENVIRONMENT:-production}"

echo "🚀 Deploying Flowise Telegram Bot to $ENVIRONMENT"
echo "📦 Image: $IMAGE_NAME:$TAG"

# Pull the latest image
echo "⬇️  Pulling latest image..."
docker pull $IMAGE_NAME:$TAG

# Stop existing container if running
if docker ps -q --filter "name=flowise-telegram-bot" | grep -q .; then
    echo "🛑 Stopping existing container..."
    docker stop flowise-telegram-bot
    docker rm flowise-telegram-bot
fi

# Run the new container
echo "▶️  Starting new container..."
docker run -d \
    --name flowise-telegram-bot \
    --restart unless-stopped \
    --env-file .env \
    --network host \
    $IMAGE_NAME:$TAG

# Wait for container to be healthy
echo "⏳ Waiting for container to be ready..."
sleep 10

# Check container status
if docker ps --filter "name=flowise-telegram-bot" --filter "status=running" | grep -q .; then
    echo "✅ Deployment successful! Bot is running."
    docker ps --filter "name=flowise-telegram-bot"
else
    echo "❌ Deployment failed! Container is not running."
    docker logs flowise-telegram-bot
    exit 1
fi
