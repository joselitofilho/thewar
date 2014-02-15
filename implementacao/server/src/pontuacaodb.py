#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class PontuacaoDB(object):

    def pontosDoUsuario(self, usuario):
        pontos = None
        conn = sqlite3.connect('war.db')
        c = conn.cursor()

        rowUsuarios = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if rowUsuarios:
            idUsuario = rowUsuarios[0]
            rowPontuacao = c.execute('SELECT pontos FROM Pontuacao WHERE idUsuario=?', [idUsuario]).fetchone()
            if rowPontuacao:
                pontos = rowPontuacao[0]

        conn.close()

        return pontos

    def atualizaPontosParaUsuario(self, usuario, pontos):
        conn = sqlite3.connect('war.db')
        c = conn.cursor()

        c.execute('UPDATE Pontuacao SET pontos=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);', [pontos, usuario])
        conn.commit()

        conn.close()

    def iniciaPontuacaoParaUsuario(self, usuario):
        conn = sqlite3.connect('war.db')
        c = conn.cursor()

        row = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if row:
            idUsuario = row[0]
            c.execute('INSERT INTO Pontuacao(idUsuario, pontos) VALUES (?, \'0\');', [idUsuario])
            conn.commit()

        conn.close()
