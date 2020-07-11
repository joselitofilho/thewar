# -*- coding: utf-8 -*-

import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY versao DESC LIMIT 1").fetchone()
    if row and row[0] == '9':
        print('Aplicando Patch database_update10...')
        cur.execute("ALTER TABLE DesafiosEmAndamento RENAME TO DesafiosEmAndamentoBkp;")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS DesafiosEmAndamento(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, infos TEXT DEFAULT '{}', apenasDoador BOOLEAN DEFAULT TRUE, iniciaEm DATETIME NOT NULL, terminaEm DATETIME NOT NULL);")
        cur.execute(
            "INSERT INTO DesafiosEmAndamento(idDesafio, nomeOrientador, infos, apenasDoador, iniciaEm, terminaEm) SELECT * FROM DesafiosEmAndamentoBkp;")
        cur.execute("DROP TABLE IF EXISTS DesafiosEmAndamentoBkp;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '10')")
        con.commit()
        print('Patch database_update10 aplicado com sucesso.')
    else:
        print('Patch database_update10 já foi aplicado anteriormente.')
