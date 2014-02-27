#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
from src.pontuacao import *

class PontuacaoTeste(unittest.TestCase):
   
    def setUp(self):
        try:
            os.remove('wartest.db')
        except:
            pass

        shutil.copyfile('wartest_base.db', 'wartest.db')

    def test_DeveRetornarORanking(self):
        # Preparação.
        quemDestruiuQuem = {
            '1': ['2', '3', '4']
        }
        pontuacao = Pontuacao('1', 
            ['1','2','3','4'], quemDestruiuQuem,
            'wartest.db')

        # Operação.
        pontosExtra = pontuacao.contabilizaPontosExtra()

        # Verificação.
        self.assertEqual(150, pontosExtra)

    def tearDown(self):
        os.remove('wartest.db')

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PontuacaoTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
