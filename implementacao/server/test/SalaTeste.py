import unittest
from src.sala import *

class SalaTeste(unittest.TestCase):
    
    def setUp(self):
        pass

    def testAdicionarNovoJogadorNaSala(self):
        self.sala = Sala("1")
        mensagem = self.sala.adiciona("Joselito")
        self.assertIsNotNone(mensagem)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SalaTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
