#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.jogo import *

class JogoTeste(unittest.TestCase):
    
    def iniciaJogadoresDoJogo(self):
        self.jogadores = {}
        self.jogadores[0] = JogadorDoJogo(
            "J1",
            0,
            True)
        self.jogadores[1] = JogadorDoJogo(
            "J2",
            1,
            False)
        self.jogadores[2] = JogadorDoJogo(
            "J3",
            2,
            False)
            
        return self.jogadores
        
    def fakeClientes(self):
        fakeClientes = {}
        fakeClientes[0] = "FakeClienteSocket1"
        fakeClientes[1] = "FakeClienteSocket2"
        fakeClientes[2] = "FakeClienteSocket3"
        return fakeClientes
    
    def setUp(self):
        self.iniciaJogadoresDoJogo()
        # TODO: Estou fazendo os clientes fakes apenas para a refatoracao. 
        # Ele deve ser retirando dessa classe quando terminado.
        self.jogo = Jogo("1", self.jogadores, self.fakeClientes())
        
    def testQuandoUmJogoEhIniciado_DeveRetornarOJogadorQueComecaOJogo(self):
        # TODO: Implementar
        pass

    def test_DeveRetornarAPosicaoDoProximoJogador1_QuandoForAVezDoJogadorDePosicao0_ESeTodosOsJogadoresEstiveremNoJogo(self):
        self.jogo.cabecaDaFila = 0
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = ["Argentina"]
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(1, self.jogo.posicaoJogadorDaVez)
        
    def test_DeveRetornarAPosicaoDoProximoJogador0_QuandoForAVezDoJogadorDePosicao2_ESeTodosOsJogadoresEstiveremNoJogo(self):
        self.jogo.cabecaDaFila = 2
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = ["Argentina"]
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(0, self.jogo.posicaoJogadorDaVez)
        
    def test_DeveRetornarAPosicaoDoProximoJogador2_QuandoForAVezDoJogadorDePosicao0_EOJogador1NaoTerMaisTerritorios(self):
        self.jogo.cabecaDaFila = 0
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = []
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(2, self.jogo.posicaoJogadorDaVez)

    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Argentina, Borneo, Coringa];
    #   * Dado que Jogador1 tem as cartas [Argentina, Borneo, Coringa].
    # 
    # Critério: Realiza a troca.
    def test_DeveRealizarTroca_QuandoTrocaDeCartasComUmCoringaEDoisQuadrados(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Argentina, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CartasTerritorio.Coringa, CartaForma.Todas, CartaCor.Todas)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Argentina,CodigoTerritorio.Borneo,CartasTerritorio.Coringa
        ])
        
        # Verificação.
        self.assertTrue(trocou)
    
    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Argentina, Borneo, Coringa]
    #   * Dado que Jogador1 tem as cartas [Brasil, Borneo, Coringa].
    # 
    # Critério: Não realiza a troca.
    def test_DadoQueAsCartasVinheramDiferentesDaQueOJogadorTem_EntaoNaoSeRealizaATroca(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Brasil, CartaForma.Bola, CartaCor.Azul),
            CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CartasTerritorio.Coringa, CartaForma.Todas, CartaCor.Todas)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Argentina,CodigoTerritorio.Borneo,CartasTerritorio.Coringa
        ])
        
        # Verificação.
        self.assertFalse(trocou)
    
    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Brasil, Borneo, Coringa]
    #   * Dado que Jogador1 tem as cartas [Brasil, Borneo, Coringa].
    # 
    # Critério: Realiza a troca.
    def test_DeveRealizarTroca_QuandoTrocaDe2CartasDeFormasDiferentesE1Coringa(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Brasil, CartaForma.Bola, CartaCor.Azul),
            CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CartasTerritorio.Coringa, CartaForma.Todas, CartaCor.Todas)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Brasil,CodigoTerritorio.Borneo,CartasTerritorio.Coringa
        ])
        
        # Verificação.
        self.assertTrue(trocou)
        
    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Brasil, Borneo, NovaYork]
    #   * Dado que Jogador1 tem as cartas [Brasil, Borneo, NovaYork].
    # 
    # Critério: Realiza a troca.
    def test_DeveRealizarTroca_QuandoTrocaDe3CartasDeFormasDiferentes(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Brasil, CartaForma.Bola, CartaCor.Azul),
            CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CodigoTerritorio.NovaYork, CartaForma.Triangulo, CartaCor.Vermelha)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Brasil,CodigoTerritorio.Borneo,CodigoTerritorio.NovaYork
        ])
        
        # Verificação.
        self.assertTrue(trocou)
        
    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Argentina, Borneo, California]
    #   * Dado que Jogador1 tem as cartas [Argentina, Borneo, California].
    # 
    # Critério: Realiza a troca.
    def test_DeveRealizarTroca_QuandoTrocaDe3CartasDeFormasIguais(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Argentina, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CodigoTerritorio.California, CartaForma.Quadrado, CartaCor.Amarela)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Argentina,CodigoTerritorio.Borneo,CodigoTerritorio.California
        ])
        
        # Verificação.
        self.assertTrue(trocou)
        
    # Cenário:
    #   * Dado que está no turno de trocar cartas;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Mexico, Mongolia, Omsk]
    #   * Dado que Jogador1 tem as cartas [Mexico, Mongolia, Omsk].
    # 
    # Critério: Não realiza a troca.
    def test_NaoDeveRealizarTroca_Quando2FormasQuadradoE1FromaTriangulo(self):
        # Preparação.
        self.jogo.posicaoJogadorDaVez = 0
        self.jogo.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
        self.jogo.jogadores[0].cartasTerritorio = [
            CartaTerritorio(CodigoTerritorio.Mexico, CartaForma.Quadrado, CartaCor.Amarela),
            CartaTerritorio(CodigoTerritorio.Mongolia, CartaForma.Bola, CartaCor.Azul),
            CartaTerritorio(CodigoTerritorio.Omsk, CartaForma.Quadrado, CartaCor.Amarela)
        ]
        
        # Operação.
        trocou = self.jogo.trocaCartasTerritorio("J1",
        [
            CodigoTerritorio.Mexico,CodigoTerritorio.Mongolia,CodigoTerritorio.Omsk
        ])
        
        # Verificação.
        self.assertFalse(trocou)

    #def test_DadoJogadorJ2_DeveGanhar3Pontos_QuandoVencerUmaPartidadeDe3Jogadores(self):
    #    pontos = self.jogo.contabilizaPontosParaOVencedor()

    #    self.assertEqual(3, pontos)
        
    def tearDown(self):
        self.jogo.fecha()

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(JogoTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
