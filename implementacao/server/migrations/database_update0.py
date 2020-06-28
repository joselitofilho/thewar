import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    try:
        row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db'").fetchone()
        print('Patch database_update0 já foi aplicado anteriormente.')
    except:
        print('Aplicando Patch database_update0...')
        cur.execute("DROP TABLE IF EXISTS Versao")
        cur.execute(
            "CREATE TABLE Versao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sistema TEXT, versao TEXT, data DATETIME DEFAULT current_timestamp)")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '0')")
        con.commit()
        print('Patch database_update0 aplicado com sucesso.')
