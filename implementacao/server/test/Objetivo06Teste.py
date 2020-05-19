#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from src.objetivos import *


class Objetivo06Teste(unittest.TestCase):

    def setUp(self):
        self.jogador1 = JogadorDoJogo("J1", 0, False)
        self.jogador2 = JogadorDoJogo("J2", 1, False)
        self.jogador3 = JogadorDoJogo("J3", 2, False)
        self.jogador4 = JogadorDoJogo("J4", 3, False)
        self.jogador5 = JogadorDoJogo("J5", 4, False)
        self.jogador6 = JogadorDoJogo("J6", 5, False)

        self.jogadores = {
            0: self.jogador1,
            1: self.jogador2,
            2: self.jogador3,
            3: self.jogador4,
            4: self.jogador5,
            5: self.jogador6
        }

        self.codigosTerritorios_2 = [
            CodigoTerritorio.Brasil,
            CodigoTerritorio.Argentina
        ]
        self.codigosTerritorios_24 = [
            CodigoTerritorio.AfricaDoSul, CodigoTerritorio.Argentina, CodigoTerritorio.Alaska, CodigoTerritorio.Aral,
            CodigoTerritorio.Alemanha, CodigoTerritorio.Argelia, CodigoTerritorio.Australia, CodigoTerritorio.Borneo,
            CodigoTerritorio.California, CodigoTerritorio.Chile, CodigoTerritorio.China, CodigoTerritorio.Colombia,
            CodigoTerritorio.Congo, CodigoTerritorio.Dudinka, CodigoTerritorio.Egito, CodigoTerritorio.Groelandia,
            CodigoTerritorio.India, CodigoTerritorio.Inglaterra, CodigoTerritorio.Japao, CodigoTerritorio.Labrador,
            CodigoTerritorio.Islandia, CodigoTerritorio.Mexico, CodigoTerritorio.Moscou, CodigoTerritorio.Omsk
        ]

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador3 eliminou o Jogador1.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador3EliminouOJogador1_EntaoJogador3VenceOJogo(self):
        # Preparacao.
        self.jogador3.jogadoresDestruidos = [0]

        # Operacao.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificacao.
        self.assertTrue(venceu)

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador1 não doi eliminado do jogo.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador1NaoFoiEliminadoDoJogo_EntaoJogador3NaoVenceOJogo(self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []

        # Operação.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificação.
        self.assertFalse(venceu)

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador1 foi eliminado mas não foi pelo Jogador3;
    #   * Jogador3 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador1FoiEliminadoMasNaoFoiPeloJogador3_DadoJogador3Tem2Territorios_EntaoJogador3NaoVenceOJogo(
            self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_2)

        # Operação.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificação.
        self.assertFalse(venceu)

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador1 foi eliminado mas não foi pelo Jogador3;
    #   * Jogador3 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador1FoiEliminadoMasNaoFoiPeloJogador3_DadoJogador3Tem24Territorios_EntaoJogador3VenceOJogo(
            self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_24)

        # Operação.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificação.
        self.assertTrue(venceu)

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador1 não está no jogo;
    #   * Jogador3 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador1NaoEstaNoJogo_DadoJogador3Tem2Territorios_EntaoJogador3NaoVenceOJogo(self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_2)

        del self.jogadores[0]

        # Operação.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificação.
        self.assertFalse(venceu)

    # Cenário:
    #   * Jogador3 tem o objetivo 06;
    #   * Jogador1 não está no jogo;
    #   * Jogador3 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador1NaoEstaNoJogo_DadoJogador3Tem24Territorios_EntaoJogador3VenceOJogo(self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_24)

        del self.jogadores[0]

        # Operação.
        venceu = Objetivo06().completou(self.jogador3, self.jogadores)

        # Verificação.
        self.assertTrue(venceu)

    # Cenário:
    #   * Jogador1 tem o objetivo 06;
    #   * Jogador1 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoJogador1Tem2Territorios_EntaoJogador1NaoVenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_2)

        # Operação.
        venceu = Objetivo06().completou(self.jogador1, self.jogadores)

        # Verificação.
        self.assertFalse(venceu)

    # Cenário:
    #   * Jogador1 tem o objetivo 06;
    #   * Jogador1 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoJogador1Tem24Territorios_EntaoJogador1VenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_24)

        # Operação.
        venceu = Objetivo06().completou(self.jogador1, self.jogadores)

        # Verificação.
        self.assertTrue(venceu)
