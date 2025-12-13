#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code from repository..."
git pull origin main

# Rebuild and restart containers
echo "🔨 Rebuilding and restarting containers..."
docker compose down
docker compose build --no-cache
docker compose up -d

# Wait a moment for the container to start
sleep 2

# Check if container is running
if docker ps | grep -q nexhacksbot; then
    echo "✅ Deployment completed successfully"
    echo "📊 Container status:"
    docker ps | grep nexhacksbot
else
    echo "❌ Deployment failed - container is not running"
    exit 1
fi

