#!/usr/bin/env python

import unittest
from FronteiraTerritorioTeste import FronteiraTerritorioTeste 

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(FronteiraTerritorioTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
