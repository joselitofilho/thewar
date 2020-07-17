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
    if row and row[0] == '11':
        print('Aplicando Patch database_update12...')
        cur.execute(
            "CREATE TABLE IF NOT EXISTS DesafiosConcluidosNova(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER NOT NULL, idDesafioEmAndamento INTEGER NOT NULL, idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, data DATETIME DEFAULT current_timestamp);")
        cur.execute(
            """
            INSERT INTO DesafiosConcluidosNova(id, idUsuario, idDesafioEmAndamento, idDesafio, nomeOrientador, data) 
                 SELECT id, idUsuario, 0, idDesafio, nomeOrientador, data
                   FROM DesafiosConcluidos;
            """)
        cur.execute("DROP TABLE DesafiosConcluidos;")
        cur.execute("ALTER TABLE DesafiosConcluidosNova RENAME TO DesafiosConcluidos;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '12')")
        con.commit()
        print('Patch database_update12 aplicado com sucesso.')
    else:
        print('Patch database_update12 já foi aplicado anteriormente.')
