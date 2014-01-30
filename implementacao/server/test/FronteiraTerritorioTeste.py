import unittest
from src.territorio import *

class FronteiraTerritorioTeste(unittest.TestCase):
    
    def testBrasilTemFronteiraComChile(self):
        self.assertTrue(FronteiraTerritorio.TemFronteira(CodigoTerritorio.Brasil, 
            CodigoTerritorio.Chile))

    def testBrasilNaoTemFronteiraComMexico(self):
        self.assertFalse(FronteiraTerritorio.TemFronteira(CodigoTerritorio.Brasil, 
            CodigoTerritorio.Mexico))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(FronteiraTerritorioTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
