#!/bin/bash

sed -e "s;PATH;$1;g" att.sql.base > att.sql
sqlite3 -cmd '.read att.sql'
