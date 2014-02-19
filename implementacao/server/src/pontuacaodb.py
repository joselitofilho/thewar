#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class PontuacaoDBO(object):
    def __init__(self):
        self.pontos = 0
        self.quantidadeDePartidas = 0
        self.quantidadeDeVitorias = 0
        self.quantidadeDestruido = 0

    def __eq__(self, other):
        if isinstance(other, PontuacaoDBO):
            return self.pontos == other.pontos and \
                    self.quantidadeDePartidas == other.quantidadeDePartidas and \
                    self.quantidadeDeVitorias == other.quantidadeDeVitorias and \
                    self.quantidadeDestruido == other.quantidadeDestruido
        return NotImplemented

class PontuacaoDB(object):

    def __init__(self, baseDeDados = 'war.db'):
        self.baseDeDados = baseDeDados

    def pontuacaoDBODoUsuario(self, usuario):
        retorno = None

        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rowUsuarios = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if rowUsuarios:
            idUsuario = rowUsuarios[0]
            rowPontuacao = c.execute('SELECT pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido FROM Pontuacao WHERE idUsuario=?', [idUsuario]).fetchone()
            if rowPontuacao:
                retorno = PontuacaoDBO()
                retorno.pontos = rowPontuacao[0]
                retorno.quantidadeDePartidas = rowPontuacao[1]
                retorno.quantidadeDeVitorias = rowPontuacao[2]
                retorno.quantidadeDestruido = rowPontuacao[3]

        conn.close()

        return retorno

    def pontosDoUsuario(self, usuario):
        pontos = None
        conn = sqlite3.connect(self.baseDeDados)
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
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        c.execute('UPDATE Pontuacao SET pontos=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);', [pontos, usuario])
        conn.commit()

        conn.close()

    def atualizaPontuacaoDBOParaUsuario(self, usuario, pontuacaoDBO):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        c.execute('UPDATE Pontuacao SET pontos=?, quantidadeDePartidas=?, quantidadeDeVitorias=?, quantidadeDestruido=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);', [pontuacaoDBO.pontos, pontuacaoDBO.quantidadeDePartidas, pontuacaoDBO.quantidadeDeVitorias, pontuacaoDBO.quantidadeDestruido, usuario])
        conn.commit()

        conn.close()

    def iniciaPontuacaoParaUsuario(self, usuario):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        row = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if row:
            idUsuario = row[0]
            c.execute('INSERT INTO Pontuacao(idUsuario) VALUES (?);', [idUsuario])
            conn.commit()

        conn.close()
