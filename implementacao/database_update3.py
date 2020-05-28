import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Doacoes")
    cur.execute("CREATE TABLE Doacoes(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, valor REAL DEFAULT 0.0, data DATETIME DEFAULT current_timestamp)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '3')")
    con.commit()
