#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.desafios.desafios import *
from src.doacaodb import *
from src.pontuacaodb import *


class Pontuacao(object):
    def __init__(self, jogo, usuarioVencedor, usuarios, quemDestruiuQuem, cpus, baseDeDados='war.db'):
        self.jogo = jogo
        self.usuarioVencedor = usuarioVencedor
        self.usuarios = usuarios
        self.quemDestruiuQuem = quemDestruiuQuem
        self.baseDeDados = baseDeDados
        self.cpus = cpus
        # TODO: Pegar o id dos usuarios e guarda-lo.
        # self.idUsuarioVencedor
        # self.idsUsuarios

    def contabilizaPontuacaoDoVencedor(self):
        pontos = 0
        # TODO: Avaliar pontuação jogando contra a IA. Talvez pelo tipo dela...
        if len(self.cpus) == 0:
            qtdUsuarios = len(self.usuarios)
            if qtdUsuarios == 3:
                pontos = 200
            elif qtdUsuarios == 4:
                pontos = 300
            elif qtdUsuarios == 5:
                pontos = 500
            elif qtdUsuarios == 6:
                pontos = 800

        pontosExtra = self.contabilizaPontosPorDestruirOutroJogador(self.usuarioVencedor, self.cpus)
        pontosDesafios = self.contabilizaPontosDesafios(self.jogo, self.usuarioVencedor, True)
        pontosExtra += pontosDesafios

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
        pontuacaoDB.atualizaPontuacaoEventoParaUsuario(self.usuarioVencedor, True, False, pontosDesafios)

        return pontos

    def contabilizaPontuacaoDosQueNaoVenceram(self):
        # TODO: Fazer em uma transacao.
        pontuacaoDB = PontuacaoDB(self.baseDeDados)
        for usuario in self.usuarios:
            if usuario == self.usuarioVencedor:
                continue

            destruidoPorAlguem = self.usuarioFoiDestruidoPorAlguem(usuario)
            pontosExtra = self.contabilizaPontosPorDestruirOutroJogador(usuario, self.cpus)

            pontosDesafios = self.contabilizaPontosDesafios(self.jogo, usuario, False)
            pontosExtra += pontosDesafios

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
            pontuacaoDB.atualizaPontuacaoEventoParaUsuario(usuario, False, destruidoPorAlguem, pontosDesafios)

    def usuarioFoiDestruidoPorAlguem(self, usuario):
        for k, v in self.quemDestruiuQuem.items():
            if usuario in v:
                return True

        return False

    def contabilizaPontosPorDestruirOutroJogador(self, usuario, cpus):
        pontosExtra = 0
        for k, usuarios in self.quemDestruiuQuem.items():
            if k == usuario:
                pontosExtra = len(usuarios)
                for cpu in cpus:
                    if cpu in usuarios:
                        pontosExtra = max(pontosExtra - 1, 0)
                break
        return pontosExtra * 100

    def contabilizaPontosDesafios(self, jogo, usuario, venceu):
        pontos = 0

        doadores = DoacaoDB().nomes_doadores()
        desafios = Desafios()
        desafios_em_andamento = desafios.em_andamento(usuario)

        proximo_desafio_central = None
        for d in desafios_em_andamento:
            if d['apenas_doador'] == 0:
                if usuario in doadores:
                    if not d['concluido']:
                        proximo_desafio_central = d
                        break
                else:
                    if not d['concluido']:
                        proximo_desafio_central = d
                    break

        if proximo_desafio_central:
            desafio = FabricaDesafios().cria(d['desafio']['id'])
            # TODO: Retirar esse IF caso um dia as cpus participem de um evento.
            if usuario not in jogo.cpus.keys():
                if desafio.completou(jogo, usuario, venceu, self.quemDestruiuQuem):
                    desafios.conclui_desafio(d, usuario)
                    pontos += d['desafio']['xp']

        for d in desafios_em_andamento:
            if d['apenas_doador'] == 1 and usuario in doadores:
                if not d['concluido']:
                    desafio = FabricaDesafios().cria(d['desafio']['id'])
                    # TODO: Retirar esse IF caso um dia as cpus participem de um evento.
                    if usuario not in jogo.cpus.keys():
                        if desafio.completou(jogo, usuario, venceu, self.quemDestruiuQuem):
                            desafios.conclui_desafio(d, usuario)
                            pontos += d['desafio']['xp']
        return pontos
