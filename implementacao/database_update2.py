import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Pontuacao")
    cur.execute("CREATE TABLE Pontuacao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, pontos INTEGER)")
    con.commit()
