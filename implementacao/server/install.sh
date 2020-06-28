#!/bin/bash

cd modules-extras/pysha3-0.3/ && python3 setup.py install

echo "0 1 * * * /bin/bash /opt/app/gerar_desafio.sh >> /dev/null" | crontab
