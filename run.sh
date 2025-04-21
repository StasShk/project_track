#!/bin/bash

IMAGE_NAME="project_trac"
CONTAINER_NAME="project_trac"

docker stop $CONTAINER_NAME 2>/dev/null && docker rm $CONTAINER_NAME 2>/dev/null

docker build -t $IMAGE_NAME .

docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME

echo "App running at http://localhost:5000"