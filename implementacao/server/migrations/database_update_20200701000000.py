# -*- coding: utf-8 -*-

import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY data DESC LIMIT 1;").fetchone()
    if row and row[0] == '8':
        print('Aplicando Patch database_update9...')
        cur.execute("DROP TABLE IF EXISTS Eventos;")
        cur.execute(
            "CREATE TABLE Eventos(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, iniciaEm DATETIME NOT NULL, terminaEm DATETIME NOT NULL);")
        cur.execute("INSERT INTO Eventos VALUES (0, 'Teste', datetime('2020-06-25 23:00:00'), datetime('2020-07-01 22:59:59'));")
        cur.execute(
            "ALTER TABLE PontuacaoEventos ADD idEvento INTEGER NOT NULL DEFAULT 0;")
        cur.execute("INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('id_evento_atual', 0);")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '9');")
        con.commit()
        print('Patch database_update9 aplicado com sucesso.')
    else:
        print('Patch database_update9 já foi aplicado anteriormente.')
