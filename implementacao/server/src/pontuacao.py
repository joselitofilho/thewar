#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pontuacaodb import *

class Pontuacao(object):
    def __init__(self, usuarioVencedor, usuarios):
        self.usuarioVencedor = usuarioVencedor
        self.usuarios = usuarios
        # TODO: Pegar o id dos usuarios e guarda-lo.
        #self.idUsuarioVencedor
        #self.idsUsuarios

    def contabiliza(self):
        pontos = 0
        qtdUsuarios = len(self.usuarios)
        if qtdUsuarios == 3:
            pontos = 100
        elif qtdUsuarios == 4:
            pontos = 200
        elif qtdUsuarios == 5:
            pontos = 300
        elif qtdUsuarios == 6:
            pontos = 500

        pontuacaoDB = PontuacaoDB()
        pontosAtual = pontuacaoDB.pontosDoUsuario(self.usuarioVencedor)
        if pontosAtual == None:
            pontuacaoDB.iniciaPontuacaoParaUsuario(self.usuarioVencedor)
            pontosAtualizados = pontos
        else:
            pontosAtualizados = pontosAtual + pontos
        
        print pontosAtualizados
        pontuacaoDB.atualizaPontosParaUsuario(
            self.usuarioVencedor, pontosAtualizados)

        return pontos
