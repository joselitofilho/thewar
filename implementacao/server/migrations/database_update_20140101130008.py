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
    if row and row[0] == '6':
        print('Aplicando Patch database_update7...')
        cur.execute("DROP TABLE IF EXISTS PontuacaoEventos")
        cur.execute(
            "CREATE TABLE PontuacaoEventos(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, pontos INTEGER DEFAULT 0, quantidadeDePartidas INTEGER DEFAULT 0, quantidadeDeVitorias DEFAULT 0, quantidadeDestruido INTEGER DEFAULT 0, atualizado DATETIME DEFAULT current_timestamp);")
        cur.execute(
            "CREATE TRIGGER IF NOT EXISTS tgIniciarPontuacaoEventos AFTER INSERT ON Usuarios BEGIN INSERT INTO PontuacaoEventos(idUsuario) VALUES (new.id); END;")
        cur.execute("INSERT INTO PontuacaoEventos(idUsuario) SELECT id FROM Usuarios;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '7')")
        con.commit()
        print('Patch database_update7 aplicado com sucesso.')
    else:
        print('Patch database_update7 já foi aplicado anteriormente.')
