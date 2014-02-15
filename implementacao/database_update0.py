import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Versao")
    cur.execute("CREATE TABLE Versao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sistema TEXT, versao TEXT, data DATETIME DEFAULT current_timestamp)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '0')")
    con.commit()
