# -*- coding: utf-8 -*-

import sqlite3
import sys
import time

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY data DESC LIMIT 1").fetchone()
    if row and row[0] == '10':
        print('Aplicando Patch database_update11...')
        cur.execute("ALTER TABLE DesafiosEmAndamento ADD ordem INTEGER NOT NULL DEFAULT 0;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '11')")
        con.commit()
        print('Patch database_update11 aplicado com sucesso.')
    else:
        print('Patch database_update11 já foi aplicado anteriormente.')
