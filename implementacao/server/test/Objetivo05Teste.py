#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.objetivos import *

class Objetivo05Teste(unittest.TestCase):

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
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador1 eliminou o Jogador3.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador1EliminouOJogador3_EntaoJogador1VenceOJogo(self):
        # Preparacao.
        self.jogador1.jogadoresDestruidos = [2]
        
        # Operacao.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificacao.
        self.assertTrue(venceu)
    
    # Cenário:
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador3 não doi eliminado do jogo.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador3NaoFoiEliminadoDoJogo_EntaoJogador1NaoVenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificação.
        self.assertFalse(venceu)
        
    # Cenário:
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador3 foi eliminado mas não foi pelo Jogador1;
    #   * Jogador1 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador3FoiEliminadoMasNaoFoiPeloJogador1_DadoJogador1Tem2Territorios_EntaoJogador1NaoVenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_2)
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificação.
        self.assertFalse(venceu)
        
    # Cenário:
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador3 foi eliminado mas não foi pelo Jogador1;
    #   * Jogador1 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador3FoiEliminadoMasNaoFoiPeloJogador1_DadoJogador1Tem24Territorios_EntaoJogador1VenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_24)
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificação.
        self.assertTrue(venceu)
        
    # Cenário:
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador3 não está no jogo;
    #   * Jogador1 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoQueOJogador3NaoEstaNoJogo_DadoJogador1Tem2Territorios_EntaoJogador1NaoVenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_2)
        
        del self.jogadores[2]
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificação.
        self.assertFalse(venceu)

    # Cenário:
    #   * Jogador1 tem o objetivo 05;
    #   * Jogador3 não está no jogo;
    #   * Jogador1 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoQueOJogador3NaoEstaNoJogo_DadoJogador1Tem24Territorios_EntaoJogador1VenceOJogo(self):
        # Preparação.
        self.jogador1.jogadoresDestruidos = []
        self.jogador1.iniciaTerritorios(self.codigosTerritorios_24)
        
        del self.jogadores[2]
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador1, self.jogadores)
        
        # Verificação.
        self.assertTrue(venceu)
        
    # Cenário:
    #   * Jogador3 tem o objetivo 05;
    #   * Jogador3 tem 2 territorios.
    #
    # Critério: Não deve vencer o jogo.
    def test_DadoJogador3Tem2Territorios_EntaoJogador3NaoVenceOJogo(self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_2)
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador3, self.jogadores)
        
        # Verificação.
        self.assertFalse(venceu)
        
    # Cenário:
    #   * Jogador3 tem o objetivo 05;
    #   * Jogador3 tem 24 territorios.
    #
    # Critério: Deve vencer o jogo.
    def test_DadoJogador3Tem24Territorios_EntaoJogador3VenceOJogo(self):
        # Preparação.
        self.jogador3.jogadoresDestruidos = []
        self.jogador3.iniciaTerritorios(self.codigosTerritorios_24)
        
        # Operação.
        venceu = Objetivo05().completou(self.jogador3, self.jogadores)
        
        # Verificação.
        self.assertTrue(venceu)
