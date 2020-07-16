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
    if row and row[0] == '3':
        print('Aplicando Patch database_update4...')
        cur.execute("DROP TABLE IF EXISTS GrupoUsuarios")
        cur.execute(
            "CREATE TABLE GrupoUsuarios(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, nome TEXT)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '4')")
        con.commit()
        print('Patch database_update4 aplicado com sucesso.')
    else:
        print('Patch database_update4 já foi aplicado anteriormente.')
