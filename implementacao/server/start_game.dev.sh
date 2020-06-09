#!/bin/bash

pip install gdown

if [ ! -f "memes.zip" ]; then
  gdown --id 12x46KaDlY5d1OzXJtEERGDoEaI6bPV-O
  mkdir -p webdir/imagens/memes/
  unzip -u memes.zip -d webdir/imagens/
  #rm memes.zip  # Please, remove manually.
fi

if [ ! -f "sons.zip" ]; then
  gdown --id 1b9W-7M-QltBvurp4cMXgWbvutJe-K7Uq
  mkdir -p webdir/sons/
  unzip -u sons.zip -d webdir/
  #rm sons.zip  # Please, remove manually.
fi

if [ ! -f "war.db" ]; then
	echo "Creating database..."
	python ../database_update0.py
	python ../database_update1.py
	python ../database_update2.py
	python ../database_update2.1.py
	python ../database_update3.py
	python ../database_update4.py
fi
echo "Starting server..."
PYTHONPATH=. python src/server.py && tail -F log/server.log