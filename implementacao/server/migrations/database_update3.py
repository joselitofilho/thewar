import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY versao DESC LIMIT 1").fetchone()
    if row and row[0] == '2.1':
        print('Aplicando Patch database_update3...')
        cur.execute("DROP TABLE IF EXISTS Doacoes")
        cur.execute(
            "CREATE TABLE Doacoes(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, valor REAL DEFAULT 0.0, data DATETIME DEFAULT current_timestamp)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '3')")
        con.commit()
        print('Patch database_update3 aplicado com sucesso.')
    else:
        print('Patch database_update3 já foi aplicado anteriormente.')
