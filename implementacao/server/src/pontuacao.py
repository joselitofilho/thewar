#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pontuacaodb import *


class Pontuacao(object):
    def __init__(self, usuarioVencedor, usuarios, quemDestruiuQuem, baseDeDados='war.db'):
        self.usuarioVencedor = usuarioVencedor
        self.usuarios = usuarios
        self.quemDestruiuQuem = quemDestruiuQuem
        self.baseDeDados = baseDeDados
        # TODO: Pegar o id dos usuarios e guarda-lo.
        # self.idUsuarioVencedor
        # self.idsUsuarios

    def contabilizaPontuacaoDoVencedor(self):
        pontos = 0
        qtdUsuarios = len(self.usuarios)
        if qtdUsuarios == 3:
            pontos = 200
        elif qtdUsuarios == 4:
            pontos = 300
        elif qtdUsuarios == 5:
            pontos = 500
        elif qtdUsuarios == 6:
            pontos = 800

        pontosExtra = self.contabilizaPontosExtra(self.usuarioVencedor)
        pontos += pontosExtra

        pontuacaoDB = PontuacaoDB(self.baseDeDados)
        pontuacaoDBOAtual = pontuacaoDB.pontuacaoDBODoUsuario(self.usuarioVencedor)
        novaPontuacaoDBO = PontuacaoDBO()
        if pontuacaoDBOAtual == None:
            pontuacaoDB.iniciaPontuacaoParaUsuario(self.usuarioVencedor)
            novaPontuacaoDBO.pontos = pontos
            novaPontuacaoDBO.quantidadeDePartidas = 1
            novaPontuacaoDBO.quantidadeDeVitorias = 1
            novaPontuacaoDBO.quantidadeDestruido = 0
        else:
            novaPontuacaoDBO.pontos = pontuacaoDBOAtual.pontos + pontos
            novaPontuacaoDBO.quantidadeDePartidas = pontuacaoDBOAtual.quantidadeDePartidas + 1
            novaPontuacaoDBO.quantidadeDeVitorias = pontuacaoDBOAtual.quantidadeDeVitorias + 1
            novaPontuacaoDBO.quantidadeDestruido = pontuacaoDBOAtual.quantidadeDestruido

        pontuacaoDB.atualizaPontuacaoDBOParaUsuario(self.usuarioVencedor, novaPontuacaoDBO)

        return pontos

    def contabilizaPontuacaoDosQueNaoVenceram(self):
        # TODO: Fazer em uma transacao.
        pontuacaoDB = PontuacaoDB(self.baseDeDados)
        for usuario in self.usuarios:
            if usuario == self.usuarioVencedor:
                continue

            destruidoPorAlguem = self.usuarioFoiDestruidoPorAlguem(usuario)
            pontosExtra = self.contabilizaPontosExtra(usuario)

            pontuacaoDBOAtual = pontuacaoDB.pontuacaoDBODoUsuario(usuario)
            novaPontuacaoDBO = PontuacaoDBO()
            if pontuacaoDBOAtual == None:
                pontuacaoDB.iniciaPontuacaoParaUsuario(usuario)
                novaPontuacaoDBO.pontos = 0 + pontosExtra
                novaPontuacaoDBO.quantidadeDePartidas = 1
                novaPontuacaoDBO.quantidadeDeVitorias = 0
                if destruidoPorAlguem:
                    novaPontuacaoDBO.quantidadeDestruido = 1
                else:
                    novaPontuacaoDBO.quantidadeDestruido = 0
            else:
                novaPontuacaoDBO.pontos = pontuacaoDBOAtual.pontos + pontosExtra
                novaPontuacaoDBO.quantidadeDePartidas = pontuacaoDBOAtual.quantidadeDePartidas + 1
                novaPontuacaoDBO.quantidadeDeVitorias = pontuacaoDBOAtual.quantidadeDeVitorias
                if destruidoPorAlguem:
                    novaPontuacaoDBO.quantidadeDestruido = pontuacaoDBOAtual.quantidadeDestruido + 1
                else:
                    novaPontuacaoDBO.quantidadeDestruido = pontuacaoDBOAtual.quantidadeDestruido

            pontuacaoDB.atualizaPontuacaoDBOParaUsuario(usuario, novaPontuacaoDBO)

    def usuarioFoiDestruidoPorAlguem(self, usuario):
        for k, v in self.quemDestruiuQuem.iteritems():
            if usuario in v:
                return True

        return False

    def contabilizaPontosExtra(self, usuario):
        pontosExtra = 0
        for k, v in self.quemDestruiuQuem.iteritems():
            if k == usuario:
                pontosExtra = len(v)
                break
        return pontosExtra * 100
