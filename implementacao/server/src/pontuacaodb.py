#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from src.JogadorRanking import *


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

    def __init__(self, baseDeDados='war.db'):
        self.baseDeDados = baseDeDados

    def pontuacaoDBODoUsuario(self, usuario):
        retorno = None

        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rowUsuarios = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if rowUsuarios:
            idUsuario = rowUsuarios[0]
            rowPontuacao = c.execute(
                'SELECT pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido FROM Pontuacao WHERE idUsuario=?',
                [idUsuario]).fetchone()
            if rowPontuacao:
                retorno = PontuacaoDBO()
                retorno.pontos = rowPontuacao[0]
                retorno.quantidadeDePartidas = rowPontuacao[1]
                retorno.quantidadeDeVitorias = rowPontuacao[2]
                retorno.quantidadeDestruido = rowPontuacao[3]

        conn.close()

        return retorno

    def iniciaPontuacaoParaUsuario(self, usuario):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        row = c.execute('SELECT id FROM Usuarios WHERE nome=?', [usuario]).fetchone()
        if row:
            idUsuario = row[0]
            c.execute('INSERT INTO Pontuacao(idUsuario) VALUES (?);', [idUsuario])
            conn.commit()

        conn.close()

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

        c.execute('UPDATE Pontuacao SET pontos=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);',
                  [pontos, usuario])
        conn.commit()

        conn.close()

    def atualizaPontuacaoDBOParaUsuario(self, usuario, pontuacaoDBO):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        c.execute(
            'UPDATE Pontuacao SET pontos=?, quantidadeDePartidas=?, quantidadeDeVitorias=?, quantidadeDestruido=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);',
            [pontuacaoDBO.pontos, pontuacaoDBO.quantidadeDePartidas, pontuacaoDBO.quantidadeDeVitorias,
             pontuacaoDBO.quantidadeDestruido, usuario])
        conn.commit()

        conn.close()

    def atualizaPontuacaoEventoParaUsuario(self, usuario, venceu, destruido_por_alguem, pontos):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        rowPontuacao = c.execute(
            'SELECT pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido FROM PontuacaoEventos WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);',
            [usuario]).fetchone()

        pontuacao = pontos
        quantidadeDePartidas = 1
        quantidadeDeVitorias = 1 if venceu else 0
        quantidadeDestruido = 1 if destruido_por_alguem else 0
        if rowPontuacao:
            pontuacao += rowPontuacao[0]
            quantidadeDePartidas += rowPontuacao[1]
            quantidadeDeVitorias += rowPontuacao[2]
            quantidadeDestruido += rowPontuacao[3]

            c.execute(
                'UPDATE PontuacaoEventos SET pontos=?, quantidadeDePartidas=?, quantidadeDeVitorias=?, quantidadeDestruido=? WHERE idUsuario IN (SELECT id FROM Usuarios WHERE nome=?);',
                [pontuacao, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido, usuario])

        conn.commit()
        conn.close()

    def ranking_geral(self):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rowPontuacoes = c.execute(
            'SELECT nome, pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido FROM Pontuacao p INNER JOIN Usuarios u ON u.id = p.idUsuario ORDER BY pontos+quantidadeDePartidas+quantidadeDeVitorias+quantidadeDestruido DESC').fetchall()

        ranking = []
        if rowPontuacoes:
            posicaoRanking = 1
            for row in rowPontuacoes:
                eficiencia = 0
                try:
                    eficiencia = int((float(row[3]) / float(row[2])) * 100)
                except:
                    pass
                jogadorRanking = JogadorRanking(posicaoRanking,
                                                row[0], row[1], row[2], row[3], row[4], eficiencia)
                ranking.append(jogadorRanking)
                posicaoRanking += 1

        conn.close()

        return ranking

    def ranking_evento(self):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rowPontuacoes = c.execute(
            'SELECT nome, pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido FROM PontuacaoEventos p INNER JOIN Usuarios u ON u.id = p.idUsuario ORDER BY pontos+quantidadeDePartidas+quantidadeDeVitorias+quantidadeDestruido DESC').fetchall()

        ranking = []
        if rowPontuacoes:
            posicaoRanking = 1
            for row in rowPontuacoes:
                eficiencia = 0
                try:
                    eficiencia = int((float(row[3]) / float(row[2])) * 100)
                except:
                    pass
                jogadorRanking = JogadorRanking(posicaoRanking,
                                                row[0], row[1], row[2], row[3], row[4], eficiencia)
                ranking.append(jogadorRanking)
                posicaoRanking += 1

        conn.close()

        return ranking
