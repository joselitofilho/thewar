import unittest
from src.sala import *

class SalaTeste(unittest.TestCase):
    
    def setUp(self):
        pass

    def testAdicionarNovoJogadorNaSala(self):
        self.sala = Sala("1")
        retorno = self.sala.adiciona("Joselito")
        self.assertIsNotNone(retorno)
        self.assertTrue(isinstance(retorno, InfoSala))
        self.assertEqual(retorno.sala, "1")
        self.assertEqual(retorno.estado, EstadoDaSala.sala_criada)
        self.assertEqual(retorno.extra["entrou_ou_saiu"], 1)

    def testNaoAdicionarJogadorQuandoASalaEstiverCheia(self):
        self.sala = Sala("1")
        self.sala.adiciona("J1")
        self.sala.adiciona("J2")
        self.sala.adiciona("J3")
        self.sala.adiciona("J4")
        self.sala.adiciona("J5")
        self.sala.adiciona("J6")

        # Adicionando jogador que nao deve ser aceito.
        retorno = self.sala.adiciona("J7")
        self.assertIsNone(retorno)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SalaTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
