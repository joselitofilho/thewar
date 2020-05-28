#!/bin/bash
cd /app # Dentro do container docker deve ser a pasta /app, mas equivale a pasta implementação/server 
FILE="war.db"
if [ ! -f "$FILE" ]; then
	echo "Creating database..."
	python ../database_update0.py
	python ../database_update1.py
	python ../database_update2.py
	python ../database_update2.1.py
fi
echo "Starting server..."
python ./src/server.py &
tail -f ./log/server.log
