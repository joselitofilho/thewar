#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
from src.pontuacaodb import *

class PontuacaoDBTeste(unittest.TestCase):
   
    def setUp(self):
        try:
            os.remove('wartest.db')
        except:
            pass

        shutil.copyfile('wartest_base.db', 'wartest.db')

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

    def test_DeveAtualizarPontuacaoDBODoUsuario(self):
        # Preparação.
        novaPontuacaoDBO = PontuacaoDBO()
        novaPontuacaoDBO.pontos = 9999;
        novaPontuacaoDBO.quantidadeDePartidas = 99
        novaPontuacaoDBO.quantidadeDeVitorias = 111
        novaPontuacaoDBO.quantidadeDestruido = 0

        # Operação.
        pontuacaoDB = PontuacaoDB('wartest.db')
        pontuacaoDBO = pontuacaoDB.atualizaPontuacaoDBOParaUsuario("Joselito", novaPontuacaoDBO)
        pontuacaoDBOAtualizada = pontuacaoDB.pontuacaoDBODoUsuario("Joselito")

        # Verificação.
        self.assertEqual(novaPontuacaoDBO, pontuacaoDBOAtualizada)

    def tearDown(self):
        os.remove('wartest.db')

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PontuacaoDBTeste)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
