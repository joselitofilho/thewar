import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY versao DESC LIMIT 1").fetchone()
    if row and row[0] == '0':
        print('Aplicando Patch database_update1...')
        cur.execute("DROP TABLE IF EXISTS Usuarios")
        cur.execute(
            "CREATE TABLE Usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT, senha TEXT, email TEXT)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '1')")
        con.commit()
        print('Patch database_update1 aplicado com sucesso.')
    else:
        print('Patch database_update1 já foi aplicado anteriormente.')
