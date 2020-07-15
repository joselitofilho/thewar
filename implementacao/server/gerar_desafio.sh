#!/bin/bash

echo "`date` $0 gerando desafios..."
PYTHONPATH=. python crons/cron_desafio.py
echo "`date` $0 fim."