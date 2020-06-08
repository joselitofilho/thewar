import sqlite3

class GrupoUsuariosDB(object):
    GRUPO_ADM = 'ADM'

    def __init__(self, baseDeDados='war.db'):
        self.baseDeDados = baseDeDados

    def verifica_usuario_adm(self, usuario):
        retorno = False

        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rowUsuario = c.execute('SELECT g.nome FROM GrupoUsuarios g JOIN Usuarios u ON u.id = g.idUsuario WHERE u.nome=?', [usuario]).fetchone()
        if rowUsuario:
            retorno = rowUsuario[0] == GrupoUsuariosDB.GRUPO_ADM
        conn.close()

        return retorno