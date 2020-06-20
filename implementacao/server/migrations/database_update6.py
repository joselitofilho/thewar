import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS DesafiosEmAndamento")
    cur.execute("CREATE TABLE IF NOT EXISTS DesafiosEmAndamento(idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, infos TEXT DEFAULT '{}', apenasDoador BOOLEAN DEFAULT TRUE, iniciaEm DATETIME DEFAULT current_timestamp)")
    cur.execute("DROP TABLE IF EXISTS DesafiosConcluidos")
    cur.execute("CREATE TABLE IF NOT EXISTS DesafiosConcluidos(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER NOT NULL, idDesafio INTEGER NOT NULL, nomeOrientador TEXT NOT NULL, data DATETIME DEFAULT current_timestamp)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '6')")
    con.commit()
