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
    if row and row[0] == '4':
        print('Aplicando Patch database_update5...')
        cur.execute("DROP TABLE IF EXISTS RecuperacaoSenha")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS RecuperacaoSenha(email TEXT PRIMARY KEY, codigo TEXT, data DATETIME DEFAULT current_timestamp)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '5')")
        con.commit()
        print('Patch database_update5 aplicado com sucesso.')
    else:
        print('Patch database_update5 já foi aplicado anteriormente.')
