#!/bin/bash

IMAGE_NAME="project_trac"
CONTAINER_NAME="project_trac"

docker stop $CONTAINER_NAME 2>/dev/null && docker rm $CONTAINER_NAME 2>/dev/null

docker build -t $IMAGE_NAME .

docker run -d \
   -p 5000:5000 \
   --name $CONTAINER_NAME \
    --mount type=bind,source="$(pwd)/exercise.db",target=/app/exercise.db \
   $IMAGE_NAME

docker exec -it $CONTAINER_NAME python app/migrate.py

echo "App running at http://localhost:5000"