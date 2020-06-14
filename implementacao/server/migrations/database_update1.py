import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Usuarios")
    cur.execute("CREATE TABLE Usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, senha TEXT, email TEXT)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '1')")
    con.commit()
