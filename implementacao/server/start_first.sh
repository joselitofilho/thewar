#!/bin/bash

python ../database_update0.py
python ../database_update1.py
python ../database_update2.py
python ../database_update2.1.py

python src/server.py
