#! /bin/bash

# Start the redis queue worker for async task execution

# This runs the worker on periodic burst mode so that changes made to tasks
# during development will be applied when the worker executes them
echo "Starting rqworker ..."
while true; do
    python /app/manage.py rqworker --burst biodataservice
    sleep 10
done
