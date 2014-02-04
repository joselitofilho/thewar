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
        self.jogo = Jogo(self.jogadores)
        # TODO: Estou fazendo os clientes fakes apenas para a refatoracao. 
        # Ele deve ser retirando dessa classe quando terminado.
        self.jogo.clientes = self.fakeClientes()
        
        
    def testQuandoUmJogoEhIniciado_DeveRetornarOJogadorQueComecaOJogo(self):
        retorno = self.jogo.defineQuemComecaOJogo()
    
        self.assertIsNotNone(retorno)
        
    #def testQuandoUmJogoEhIniciado_DeveRetornarOsTerritoriosDeCadaJogador(self):
    #    self.jogo.cabecaDaFila = 2
    #    self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
    #    self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
    #    retorno = self.jogo.distribuiTerritoriosEntreOsJogadores()
    
    #    self.assertIsNotNone(retorno)
    #    self.assertEqual(3, len(retorno))
    
    def testDeveRetornarAPosicaoDoProximoJogador1_QuandoForAVezDoJogadorDePosicao0_ESeTodosOsJogadoresEstiveremNoJogo(self):
        self.jogo.cabecaDaFila = 0
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = ["Argentina"]
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(1, self.jogo.posicaoJogadorDaVez)
        
    def testDeveRetornarAPosicaoDoProximoJogador0_QuandoForAVezDoJogadorDePosicao2_ESeTodosOsJogadoresEstiveremNoJogo(self):
        self.jogo.cabecaDaFila = 2
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = ["Argentina"]
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(0, self.jogo.posicaoJogadorDaVez)
        
    def testDeveRetornarAPosicaoDoProximoJogador2_QuandoForAVezDoJogadorDePosicao0_EOJogador1NaoTerMaisTerritorios(self):
        self.jogo.cabecaDaFila = 0
        self.jogo.indiceOrdemJogadores = self.jogo.cabecaDaFila
        self.jogo.posicaoJogadorDaVez = self.jogo.ordemJogadores[self.jogo.cabecaDaFila]
        self.jogo.jogadores[0].territorios = ["Brasil"]
        self.jogo.jogadores[1].territorios = []
        self.jogo.jogadores[2].territorios = ["Chile"]
        self.jogo.passaParaProximoJogador()
        
        self.assertEqual(2, self.jogo.posicaoJogadorDaVez)
