import unittest
from src.sala import *

class SalaTeste(unittest.TestCase):
    
    def setUp(self):
        pass

    def testDeveRetornarAsInformacoesDaSala_QuandoAdicionarNovoJogadorNaSala(self):
        # Preparando.
        sala = Sala("1")

        # Acao.
        retorno = sala.adiciona("Joselito")

        # Verificacao.
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEqual(retorno.sala, "1")
        self.assertEqual(retorno.estado, EstadoDaSala.sala_criada)
        self.assertEqual(retorno.extra["entrou_ou_saiu"], 1)

    def testDeveRetornarNone_QuandoAdicionarJogadorNumaSalaCheia(self):
        # Preparando.
        sala = Sala("1")
        sala.adiciona("J1")
        sala.adiciona("J2")
        sala.adiciona("J3")
        sala.adiciona("J4")
        sala.adiciona("J5")
        sala.adiciona("J6")

        # Acao.
        retorno = sala.adiciona("J7")

        # Verificacao.
        self.assertIsNone(retorno)

    def testDeveRetornarNone_QuandoTentarAdicionarUmJogadorQueJaEstaNaSala(self):
        # Preparando.
        sala = Sala("1")
        sala.adiciona("Joselito")

        # Acao.
        retorno = sala.adiciona("Joselito")

        # Verificacao.
        self.assertIsNone(retorno)


    def testDeveRetornarAsInformacoesDaSala_QuandoRemoverUmJogadorDaSalaQueEstaNaSala(self):
        # Preparando.
        sala = Sala("2")
        sala.adiciona("Joselito")

        # Acao.
        retorno = sala.remove("Joselito")

        # Verificacao.
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEqual(retorno.sala, "2")
        self.assertEqual(retorno.estado, EstadoDaSala.sala_criada)
        self.assertEqual(retorno.extra["entrou_ou_saiu"], 0)

    def testDeveRetornarNone_QuandoRemoverUmJogadorDaSalaQueNaoEstaNaSala(self):
        # Preparando.
        sala = Sala("2")
        
        # Acao.
        retorno = sala.remove("Joselito")

        # Verificacao.
        self.assertIsNone(retorno)

    def testDeveRetornarQueOJogadorFoiAdicionadoNaSalaNaPosicaoUm_QuandoAlterarAPosicaoDeUmJogadorQueNaoEstaNaSala(self):
        # Preparando.
        sala = Sala("3")

        # Acao.
        retorno = sala.alteraPosicao("Joselito", 2)

        # Verificacao.
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEquals(retorno.jogadores[0].usuario, "Joselito")
        self.assertEquals(retorno.jogadores[0].posicao, 0)

    def testDeveRetornarQueOJogadorEstaNaNovaPosicao_QuandoAlterarAPosicao(self):
        # Preparando.
        sala = Sala("3")
        sala.adiciona("Joselito")

        # Acao.
        retorno = sala.alteraPosicao("Joselito", 3)

        # Verificacao.
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, AlteraPosicaoNaSala))
        self.assertEquals(retorno.sala, "3")
        self.assertEquals(retorno.jogadorDaSala.usuario, "Joselito")
        self.assertEquals(retorno.jogadorDaSala.posicao, 3)
        self.assertEquals(retorno.posicaoAntiga, 0)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SalaTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
