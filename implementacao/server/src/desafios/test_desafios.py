#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.desafios.desafios import *
from src.ia.ialucy import *
from src.jogador import *
from src.jogo import *
from src.pontuacao import *


def test_desafio01():
    id_desafio = 1

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(1):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in range(3):
        cpu = IALucy(str(i))
        cpus[cpu.usuario] = cpu

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio02():
    id_desafio = 2

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(1):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in range(4):
        cpu = IALucy(str(i))
        cpus[cpu.usuario] = cpu

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio03():
    id_desafio = 3

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(1):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in range(5):
        cpu = IALucy(str(i))
        cpus[cpu.usuario] = cpu

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio04():
    id_desafio = 4

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in [1, 2]:
        jogadoresDoJogo[0].jogadoresDestruidos.append(i)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio05():
    id_desafio = 5

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in [1, 2, 3]:
        jogadoresDoJogo[0].jogadoresDestruidos.append(i)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio07():
    id_desafio = 7

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    territorios = list(CodigoTerritorio.Lista)
    for j in range(20):
        jogadoresDoJogo[0].territorios.append(territorios[j])

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio10():
    id_desafio = 10

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    territorio = Territorio(list(CodigoTerritorio.Lista)[0])
    territorio.quantidadeDeTropas = 60
    jogadoresDoJogo[0].territorios.append(territorio)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio14():
    id_desafio = 14

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for t in GrupoTerritorio.Dicionario[GrupoTerritorio.Asia]:
        jogadoresDoJogo[0].territorios.append(Territorio(t))
    for t in GrupoTerritorio.Dicionario[GrupoTerritorio.Europa]:
        jogadoresDoJogo[0].territorios.append(Territorio(t))

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio17():
    id_desafio = 17

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for t in GrupoTerritorio.Dicionario[GrupoTerritorio.Africa]:
        jogadoresDoJogo[0].territorios.append(Territorio(t))

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio22():
    id_desafio = 22

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    # jogadoresDoJogo[1].jogadoresDestruidos.append(0)  # Descomentar para simular que o jogador 0 foi destruído pelo jogador 1.

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = False
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio25():
    id_desafio = 25

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    jogo.turno.numero = 20
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio28():
    id_desafio = 28

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    territorio = Territorio(CodigoTerritorio.Moscou)
    territorio.quantidadeDeTropas = 100
    jogadoresDoJogo[0].territorios.append(territorio)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_desafio32():
    id_desafio = 32

    jogadoresDoJogo = {}
    cpus = {}

    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    territorio = Territorio(CodigoTerritorio.OrienteMedio)
    territorio.quantidadeDeTropas = 150
    jogadoresDoJogo[0].territorios.append(territorio)

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    desafio = FabricaDesafios().cria(id_desafio)
    print('Desafio {} completou? {}'.format(id_desafio,
                                            desafio.completou(jogo, usuario, venceu, quemDestruiuQuem)))


def test_contabiliza_pontos():
    jogadoresDoJogo = {}
    cpus = {}

    usuarios = []
    for i in range(6):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)
        usuarios.append('player' + str(i))

    jogo = Jogo('TesteDesafio', jogadoresDoJogo, cpus)
    usuario_vencedor = 'player0'
    jogo.jogadorVencedor = jogadoresDoJogo[0]
    venceu = True
    quemDestruiuQuem = jogo.quemDestruiuQuem(jogo.jogadores)

    print('Pontos obtidos {}'.format(Pontuacao(jogo, usuario_vencedor, usuarios, quemDestruiuQuem, cpus).contabilizaPontosDesafios(jogo, usuario_vencedor, venceu)))


if __name__ == '__main__':
    test_desafio01()
    test_desafio02()
    test_desafio03()
    test_desafio04()
    test_desafio05()
    # test_desafio06()
    test_desafio07()
    # test_desafio08()
    # test_desafio09()
    test_desafio10()
    # test_desafio11()
    # test_desafio12()
    # test_desafio13()
    test_desafio14()
    # test_desafio15()
    # test_desafio16()
    test_desafio17()
    # test_desafio18()
    # test_desafio19()
    # test_desafio20()
    # test_desafio21()
    test_desafio22()
    # test_desafio23()
    # test_desafio24()
    test_desafio25()
    # test_desafio26()
    # test_desafio27()
    test_desafio28()
    # test_desafio30()
    # test_desafio31()
    test_desafio32()

    test_contabiliza_pontos()
