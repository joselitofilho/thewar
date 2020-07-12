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
    if row and row[0] == '5':
        print('Aplicando Patch database_update6...')
        cur.execute("DROP TABLE IF EXISTS DesafiosEmAndamento")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS DesafiosEmAndamento(idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, infos TEXT DEFAULT '{}', apenasDoador BOOLEAN DEFAULT TRUE, iniciaEm DATETIME NOT NULL, terminaEm DATETIME NOT NULL)")
        cur.execute("DROP TABLE IF EXISTS DesafiosConcluidos")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS DesafiosConcluidos(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER NOT NULL, idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, data DATETIME DEFAULT current_timestamp)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '6')")
        con.commit()
        print('Patch database_update6 aplicado com sucesso.')
    else:
        print('Patch database_update6 já foi aplicado anteriormente.')
