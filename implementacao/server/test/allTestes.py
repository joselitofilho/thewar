#!/usr/bin/env python

import unittest
from FronteiraTerritorioTeste import FronteiraTerritorioTeste 
from SalaTeste import SalaTeste 

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FronteiraTerritorioTeste))
    suite.addTest(unittest.makeSuite(SalaTeste))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
