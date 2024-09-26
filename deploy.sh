#!/bin/bash

# Pull the latest code from the repository
git pull origin main

# Build and run the application
docker-compose down
docker-compose pull
docker-compose up -d --build

# Cleanup unused Docker images and volumes
docker system prune -f
