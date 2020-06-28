import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY versao DESC LIMIT 1").fetchone()
    if row and row[0] == '1':
        print('Aplicando Patch database_update2...')
        cur.execute("DROP TABLE IF EXISTS Pontuacao")
        cur.execute(
            "CREATE TABLE Pontuacao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, pontos INTEGER DEFAULT 0, quantidadeDePartidas INTEGER DEFAULT 0, quantidadeDeVitorias DEFAULT 0, quantidadeDestruido INTEGER DEFAULT 0, atualizado DATETIME DEFAULT current_timestamp)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '2')")
        con.commit()
        print('Patch database_update2 aplicado com sucesso.')
    else:
        print('Patch database_update2 já foi aplicado anteriormente.')
