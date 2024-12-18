#!/bin/bash

# Stop containers and remove volumes
docker-compose down -v

# Rebuild and start containers
docker-compose up --build