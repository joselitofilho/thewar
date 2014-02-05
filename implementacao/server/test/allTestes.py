#!/usr/bin/env python

import unittest
from FronteiraTerritorioTeste import FronteiraTerritorioTeste
from Objetivo01Teste import Objetivo01Teste
from Objetivo02Teste import Objetivo02Teste
from Objetivo03Teste import Objetivo03Teste
from SalaTeste import SalaTeste 

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FronteiraTerritorioTeste))
    suite.addTest(unittest.makeSuite(Objetivo01Teste))
    suite.addTest(unittest.makeSuite(Objetivo02Teste))
    suite.addTest(unittest.makeSuite(Objetivo03Teste))
    suite.addTest(unittest.makeSuite(SalaTeste))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
