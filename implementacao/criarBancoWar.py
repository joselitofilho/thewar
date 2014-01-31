import sqlite3

con = sqlite3.connect('war_novo.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Usuarios")
    cur.execute("CREATE TABLE Usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, senha TEXT, email TEXT)")
    #cur.execute("INSERT INTO Usuarios(nome, senha, email) VALUES('Joselito', '1234', 'joselitofilhoo@gmail.com')")
    #cur.execute("INSERT INTO Usuarios(nome, senha, email) VALUES('visitante', 'visitante', 'jogowar@gmail.com')")
    con.commit()
