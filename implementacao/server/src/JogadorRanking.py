#!/usr/bin/env python
# -*- coding: utf-8 -*-

class JogadorRanking(object):
    def __init__(self, posicaoNoRanking, nome,
                 pontos, quantidadeDePartidas, quantidadeDeVitorias, quantidadeDestruido, eficiencia):
        self.posicaoNoRanking = posicaoNoRanking
        self.nome = nome
        self.pontos = pontos
        self.quantidadeDePartidas = quantidadeDePartidas
        self.quantidadeDeVitorias = quantidadeDeVitorias
        self.quantidadeDestruido = quantidadeDestruido
        self.eficiencia = eficiencia

    def __eq__(self, other):
        if isinstance(other, JogadorRanking):
            return self.posicaoNoRanking == other.posicaoNoRanking and \
                   self.nome == other.nome and \
                   self.pontos == other.pontos and \
                   self.quantidadeDePartidas == other.quantidadeDePartidas and \
                   self.quantidadeDeVitorias == other.quantidadeDeVitorias and \
                   self.quantidadeDestruido == other.quantidadeDestruido
        return NotImplemented
