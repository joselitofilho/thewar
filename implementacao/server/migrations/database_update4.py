import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS GrupoUsuarios")
    cur.execute("CREATE TABLE GrupoUsuarios(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, nome TEXT)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '4')")
    con.commit()
