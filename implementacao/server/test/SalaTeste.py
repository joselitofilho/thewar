import unittest
from src.sala import *

class SalaTeste(unittest.TestCase):
    
    def setUp(self):
        pass

    def testDeveRetornarAsInformacoesDaSala_QuandoAdicionarNovoJogadorNaSala(self):
        sala = Sala("1")
        retorno = sala.adiciona("Joselito")
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEqual(retorno.sala, "1")
        self.assertEqual(retorno.estado, EstadoDaSala.sala_criada)
        self.assertEqual(retorno.extra["entrou_ou_saiu"], 1)

    def testDeveRetornarNone_QuandoAdicionarJogadorNumaSalaCheia(self):
        sala = Sala("1")
        sala.adiciona("J1")
        sala.adiciona("J2")
        sala.adiciona("J3")
        sala.adiciona("J4")
        sala.adiciona("J5")
        sala.adiciona("J6")

        # Adicionando jogador que nao deve ser aceito.
        retorno = sala.adiciona("J7")
        self.assertIsNone(retorno)

    def testDeveRetornarAsInformacoesDaSala_QuandoRemoverUmJogadorDaSalaQueEstaNaSala(self):
        sala = Sala("2")
        sala.adiciona("Joselito")

        # Remover jogador que ja existe.
        retorno = sala.remove("Joselito")
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEqual(retorno.sala, "2")
        self.assertEqual(retorno.estado, EstadoDaSala.sala_criada)
        self.assertEqual(retorno.extra["entrou_ou_saiu"], 0)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SalaTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
