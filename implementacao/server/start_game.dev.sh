#!/bin/bash

echo "Executing migrations..."
ls -p migrations/database*.py | xargs -n 1 -I file python file war.db

echo "Starting server..."
PYTHONPATH=. python src/server.py
