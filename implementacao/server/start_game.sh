#!/bin/bash

FILE="war.db"
if [ ! -f "$FILE" ]; then
	echo "Creating database..."
	python ../database_update0.py
	python ../database_update1.py
	python ../database_update2.py
	python ../database_update2.1.py
	python ../database_update3.py
fi
echo "Starting server..."
PYTHONPATH=. python src/server.py
