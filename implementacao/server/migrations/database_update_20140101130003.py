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
    if row and row[0] == '2':
        print('Aplicando Patch database_update2_1...')
        cur.execute(
            "CREATE TRIGGER tgIniciarPontuacao AFTER INSERT ON Usuarios BEGIN INSERT INTO Pontuacao(idUsuario) VALUES (new.id); END;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '2.1')")
        con.commit()
        print('Patch database_update2_1 aplicado com sucesso.')
    else:
        print('Patch database_update2_1 já foi aplicado anteriormente.')
