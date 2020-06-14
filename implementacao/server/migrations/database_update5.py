import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS RecuperacaoSenha")
    cur.execute("CREATE TABLE IF NOT EXISTS RecuperacaoSenha(email TEXT PRIMARY KEY, codigo TEXT, data DATETIME DEFAULT current_timestamp)")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '5')")
    con.commit()
