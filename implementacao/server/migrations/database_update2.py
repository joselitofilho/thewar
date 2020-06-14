import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Pontuacao")
    cur.execute("CREATE TABLE Pontuacao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, pontos INTEGER DEFAULT 0, quantidadeDePartidas INTEGER DEFAULT 0, quantidadeDeVitorias DEFAULT 0, quantidadeDestruido INTEGER DEFAULT 0, atualizado DATETIME DEFAULT current_timestamp)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '2')")
    con.commit()
