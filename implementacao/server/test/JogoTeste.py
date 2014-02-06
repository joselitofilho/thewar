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
    #   * Dado que Jogador1 tem 3 cartas territórios;
    #   * Dado que Jogador1 solicita fazer uma troca com as cartas:
    #     - [Argentina, Borneo, Coringa]
    # 
    # Critério: Efetuar troca com sucesso.
    def test_TrocaDeCartasComUmCoringaEDoisQuadrados(self):
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
        
    def tearDown(self):
        self.jogo.fecha()

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(JogoTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
