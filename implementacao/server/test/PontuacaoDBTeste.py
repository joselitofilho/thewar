#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.pontuacaodb import *

class PontuacaoDBTeste(unittest.TestCase):
    
    def test_DeveRetornarAPontuacaoDBODoUsuario(self):
        # Preparação.
        pontuacaoDBOEsperado = PontuacaoDBO()
        pontuacaoDBOEsperado.pontos = 500
        pontuacaoDBOEsperado.quantidadeDePartidas = 3
        pontuacaoDBOEsperado.quantidadeDeVitorias = 2
        pontuacaoDBOEsperado.quantidadeDerrotas = 0
        
        # Operação.
        pontuacaoDB = PontuacaoDB('wartest.db')
        pontuacaoDBO = pontuacaoDB.pontuacaoDBODoUsuario("Joselito")
        
        # Verificação.
        self.assertEqual(pontuacaoDBOEsperado, pontuacaoDBO)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PontuacaoDBTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
