import sqlite3

con = sqlite3.connect('war.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TRIGGER tgIniciarPontuacao AFTER INSERT ON Usuarios BEGIN INSERT INTO Pontuacao(idUsuario) VALUES (new.id); END;")
    cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '2.1')")
    con.commit()
