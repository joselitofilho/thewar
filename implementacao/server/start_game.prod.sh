#!/bin/bash

cd /app # Dentro do container docker deve ser a pasta /app, mas equivale a pasta implementação/server 

gdown --id 12x46KaDlY5d1OzXJtEERGDoEaI6bPV-O
mkdir -p webdir/imagens/memes/
unzip -u memes.zip -d webdir/imagens/
rm memes.zip

gdown --id 1b9W-7M-QltBvurp4cMXgWbvutJe-K7Uq
mkdir -p webdir/sons/
unzip -u sons.zip -d webdir/
rm sons.zip

gdown --id 1DLO1aRCZFgJZeGQoVnlQZpZLVuPHiZ4F
mkdir -p webdir/videos/
unzip -u videos.zip -d webdir/
rm videos.zip

gdown --id 1fDOrGiP1gqAUehyAOhZgRMwHyeVgiu81
mv premiacao.png webdir/imagens/lobby/banners/

gdown --id 15Y7Zrp9s4FiQuKgMiN-lxTad7xyEhh0l
mv premio.png webdir/imagens/lobby/banners/

echo "Executing migrations..."
ls -p migrations/database*.py | xargs -n 1 -I file python file war.db

echo "Starting server..."
PYTHONPATH=. python ./src/server.py >> ./log/server.log && tail -F ./log/server.log

