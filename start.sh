#!/bin/bash

# Bring down any existing containers for the mdmodels-demo project
docker compose -p md-models-demo down

# Start up the services
docker compose up --build -d