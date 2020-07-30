# -*- coding: utf-8 -*-

import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY data DESC LIMIT 1").fetchone()
    if row and row[0] == '12':
        print('Aplicando Patch database_update13...')
        cur.execute(
            "CREATE TABLE IF NOT EXISTS HistoricoJogos(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT NOT NULL, iniciou_em DATETIME DEFAULT current_timestamp, infos TEXT DEFAULT '{}');")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '13')")
        con.commit()
        print('Patch database_update13 aplicado com sucesso.')
    else:
        print('Patch database_update13 já foi aplicado anteriormente.')
