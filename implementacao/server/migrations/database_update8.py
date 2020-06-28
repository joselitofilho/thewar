import sqlite3
import sys

wardb = 'war.db'
if len(sys.argv) > 1:
    wardb = sys.argv[1]

con = sqlite3.connect(wardb)
with con:
    cur = con.cursor()
    row = cur.execute("SELECT versao FROM Versao WHERE sistema = 'db' ORDER BY versao DESC LIMIT 1").fetchone()
    if row and row[0] == '7':
        print('Aplicando Patch database_update8...')
        cur.execute("DROP TABLE IF EXISTS Configuracoes")
        cur.execute(
            "CREATE TABLE Configuracoes(chave TEXT PRIMARY KEY NOT NULL, valor TEXT DEFAULT '', extra TEXT DEFAULT '{}')")
        cur.execute("DROP TABLE IF EXISTS HistoricoDoacoes")
        cur.execute("INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('meta_doacao', '300')")
        cur.execute(
            "CREATE TABLE HistoricoDoacoes(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idUsuario INTEGER, valor REAL DEFAULT 0.0, data DATETIME DEFAULT current_timestamp)")
        cur.execute(
            "CREATE TRIGGER IF NOT EXISTS tgNovaDoacao AFTER INSERT ON Doacoes BEGIN INSERT INTO HistoricoDoacoes(id, idUsuario, valor, data) VALUES (new.id, new.idUsuario, new.valor, new.data); END;")
        cur.execute("INSERT INTO Versao(sistema, versao) VALUES ('db', '8')")
        con.commit()
        print('Patch database_update8 aplicado com sucesso.')
    else:
        print('Patch database_update8 já foi aplicado anteriormente.')
