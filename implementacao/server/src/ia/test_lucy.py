#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from src.desafios.desafios import *
from src.ia.ialucy import *
from src.jogador import *
from src.jogo import *
from src.pontuacao import *


def test_acao_atacar():
    jogadoresDoJogo = {}
    cpus = {}

    for i in range(1):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in range(2):
        cpu = IALucy(str(i))
        cpus[cpu.usuario] = cpu
        jogadoresDoJogo[i + 1] = JogadorDoJogo(cpu.usuario, i + 1, False, TipoJogador.cpu)

    jogo = Jogo('TesteLucyAtacar', jogadoresDoJogo, cpus)
    jogo.faseI_Inicia()
    jogo.faseI_DefinirObjetivos()
    # jogo.iniciaTurnos()
    jogo.turno.tipoAcao = TipoAcaoTurno.mover
    jogo.posicaoJogadorDaVez = 1

    ################################################################################
    ################################################################################
    ################################################################################

    ### Oceania
    # Sumatra - 1 - Cpu2
    # Borneo - 2 - Humano
    # NovaGuine - 3 - Cpu2
    # Autralia - 8 - Cpu1

    for ttt in [CodigoTerritorio.Sumatra, CodigoTerritorio.Borneo, CodigoTerritorio.NovaGuine,
                CodigoTerritorio.Australia]:
        if ttt == CodigoTerritorio.Australia:
            terr = jogo.jogadores[1].seuTerritorio(ttt)
            if terr is not None:
                jogo.jogadores[1].removeTerritorio(ttt)
            else:
                terr = jogo.jogadores[0].seuTerritorio(ttt)
                if terr is not None:
                    jogo.jogadores[0].removeTerritorio(ttt)
                else:
                    terr = jogo.jogadores[2].seuTerritorio(ttt)
                    if terr is not None:
                        jogo.jogadores[2].removeTerritorio(ttt)

            terr.quantidadeDeTropas = 8
            jogo.jogadores[1].adicionaTerritorio(terr)

        if ttt == CodigoTerritorio.Sumatra or ttt == CodigoTerritorio.NovaGuine:
            terr = jogo.jogadores[2].seuTerritorio(ttt)
            if terr is not None:
                jogo.jogadores[2].removeTerritorio(ttt)
            else:
                terr = jogo.jogadores[0].seuTerritorio(ttt)
                if terr is not None:
                    jogo.jogadores[0].removeTerritorio(ttt)
                else:
                    terr = jogo.jogadores[1].seuTerritorio(ttt)
                    if terr is not None:
                        jogo.jogadores[1].removeTerritorio(ttt)

            if ttt == CodigoTerritorio.Sumatra:
                terr.quantidadeDeTropas = 1
            else:
                terr.quantidadeDeTropas = 3
            jogo.jogadores[2].adicionaTerritorio(terr)

        if ttt == CodigoTerritorio.Borneo:
            terr = jogo.jogadores[0].seuTerritorio(ttt)
            if terr is not None:
                jogo.jogadores[0].removeTerritorio(ttt)
            else:
                terr = jogo.jogadores[1].seuTerritorio(ttt)
                if terr is not None:
                    jogo.jogadores[1].removeTerritorio(ttt)
                else:
                    terr = jogo.jogadores[2].seuTerritorio(ttt)
                    if terr is not None:
                        jogo.jogadores[2].removeTerritorio(ttt)

            terr.quantidadeDeTropas = 2
            jogo.jogadores[0].adicionaTerritorio(terr)

    # print('Lucy0 {}'.format(jogo.jogadores[1].toJson()))
    # print('grafo {}'.format(jogo.grafoTerritorios(jogo.jogadores)))

    ################################################################################
    ################################################################################
    ################################################################################

    jogador = jogo.jogadores[1]
    usuario = jogador.usuario

    # meus_territorios = jogador.territorios
    # random.shuffle(meus_territorios)
    # territoriosInimigos = jogo.territoriosInimigos(usuario)
    # random.shuffle(territoriosInimigos)
    # for territorio in meus_territorios:
    #     if territorio.quantidadeDeTropas > 3:
    #         for inimigo in territoriosInimigos:
    #             if territorio.quantidadeDeTropas >= inimigo.quantidadeDeTropas + 2 and FronteiraTerritorio.TemFronteira(
    #                     inimigo.codigo, territorio.codigo):
    #                 print('{} ataca de {} em {}'.format(usuario, territorio.toJson(), inimigo.toJson()))
    #                 # jogo.ataca(usuario, [territorio.codigo], inimigo.codigo)
    #                 return False
    #
    # print('{} não atacou.'.format(usuario))
    # return True

    grafo = cpus[usuario].atualiza_grafo(usuario, jogador, jogo)
    meus_territorios_com_tropa = dict(
        filter(
            lambda elem: elem[1]['quantidade'] > 3 and elem[1]['usuario'] == usuario and elem[1]['bst'] != 0 and
                         elem[1]['bst'] != 1, grafo.items()))
    # print('{} meus_territorios_com_tropa {}.'.format(usuario, meus_territorios_com_tropa))

    if len(meus_territorios_com_tropa) > 0:
        codigo_territorios_inimigos = []
        for t in jogo.territoriosInimigos(usuario):
            codigo_territorios_inimigos.append(t.codigo)
        # print('codigoTerritoriosInimigos', codigo_territorios_inimigos)

        for territorio in meus_territorios_com_tropa:
            territorio_para = {}
            for territorio_fronteira in meus_territorios_com_tropa[territorio]['fronteiras']:
                diff_quantidade = meus_territorios_com_tropa[territorio]['quantidade'] - \
                                  grafo[territorio_fronteira]['quantidade']
                if territorio_fronteira in codigo_territorios_inimigos and diff_quantidade >= 2:
                    territorio_para[territorio_fronteira] = grafo[territorio_fronteira]
                    territorio_para[territorio_fronteira]['diff_quantidade'] = diff_quantidade
            territorio_para_ordenado = sorted(territorio_para.items(), key=lambda x: x[1]['diff_quantidade'] and x[1]['tipo'], reverse=True)
            # print(territorio_para_ordenado)
            if len(territorio_para_ordenado) > 0:
                territorio_inimigo = territorio_para_ordenado[0][0]
                print('{} ataca de {} em {}'.format(usuario, territorio, territorio_inimigo))
                jogo.ataca(usuario, [territorio], territorio_inimigo)
                return False

    # print('{} não atacou.'.format(usuario))
    return True


def test_acao_mover():
    jogadoresDoJogo = {}
    cpus = {}

    for i in range(1):
        jogadoresDoJogo[i] = JogadorDoJogo('player' + str(i), i, True if i == 0 else False, TipoJogador.humano)

    for i in range(2):
        cpu = IALucy(str(i))
        cpus[cpu.usuario] = cpu
        jogadoresDoJogo[i + 1] = JogadorDoJogo(cpu.usuario, i + 1, False, TipoJogador.cpu)

    jogo = Jogo('TesteLucyMover', jogadoresDoJogo, cpus)
    jogo.faseI_Inicia()
    jogo.faseI_DefinirObjetivos()
    # jogo.iniciaTurnos()
    jogo.turno.tipoAcao = TipoAcaoTurno.mover
    jogo.posicaoJogadorDaVez = 1

    ################################################################################
    ################################################################################
    ################################################################################

    ### Asia
    # India - 1
    # Vietna - 1
    ### Oceania
    # Sumatra - 1
    # Borneo - 1
    # NovaGuine - 1
    # Autralia - 5

    for ttt in [CodigoTerritorio.India, CodigoTerritorio.Vietna, CodigoTerritorio.Sumatra, CodigoTerritorio.Borneo,
                CodigoTerritorio.NovaGuine, CodigoTerritorio.Australia]:
        terr = jogo.jogadores[1].seuTerritorio(ttt)
        if ttt == CodigoTerritorio.Australia and terr is not None:
            # print('jog', jogo.jogadores[1].usuario, 'terr', terr.codigo)
            jogo.jogadores[1].removeTerritorio(ttt)
            terr.quantidadeDeTropas = 5
            jogo.jogadores[1].adicionaTerritorio(terr)

        terr = jogo.jogadores[0].seuTerritorio(ttt)
        if terr is not None:
            # print('jog', jogo.jogadores[0].usuario, 'terr', terr.codigo)
            jogo.jogadores[0].removeTerritorio(ttt)
            if ttt == CodigoTerritorio.Australia:
                terr.quantidadeDeTropas = 5
            jogo.jogadores[1].adicionaTerritorio(terr)

        terr = jogo.jogadores[2].seuTerritorio(ttt)
        if terr is not None:
            # print('jog', jogo.jogadores[2].usuario, 'terr', terr.codigo)
            jogo.jogadores[2].removeTerritorio(ttt)
            if ttt == CodigoTerritorio.Australia:
                terr.quantidadeDeTropas = 5
            jogo.jogadores[1].adicionaTerritorio(terr)

    # print('Lucy0 {}'.format(jogo.jogadores[1].toJson()))
    # print('grafo {}'.format(jogo.grafoTerritorios(jogo.jogadores)))

    ################################################################################
    ################################################################################
    ################################################################################

    jogador = jogo.jogadores[1]
    usuario = jogador.usuario
    visitados = []
    while True:
        grafo = cpus[usuario].atualiza_grafo(usuario, jogador, jogo)
        # print('---> Lucy0 {}'.format(jogo.jogadores[1].toJson()))
        territorios_com_bst_0 = dict(
            filter(
                lambda elem: elem[1]['quantidade'] > 1 and elem[1]['usuario'] == usuario and elem[1]['bst'] == 0 and
                             elem[1]['codigo'] not in visitados, grafo.items()))
        print('territorios_com_bst_0', len(territorios_com_bst_0), territorios_com_bst_0)

        if len(territorios_com_bst_0) > 0:
            do_territorio = next(iter(territorios_com_bst_0))
            territorio_de = grafo[do_territorio]
            territorio_para = {}
            so_tem_fronteira_com_bst_0 = True
            for t in territorio_de['fronteiras']:
                if grafo[t]['usuario'] == usuario and t not in visitados:
                    territorio_para[t] = grafo[t]
                    # print('De {} tem fronteira com {}'.format(territorio_de['codigo'], territorio_para[t]))
                    if grafo[t]['bst'] != 0:
                        so_tem_fronteira_com_bst_0 = False

            print('territorio_para', len(territorio_para))
            if len(territorio_para) > 0:
                if so_tem_fronteira_com_bst_0:
                    visitados.append(do_territorio)
                for tp in territorio_para.values():
                    print('BSR ::', tp)

                territorio_para_ordenado = sorted(territorio_para.items(), key=lambda x: x[1]['nbsr'], reverse=True)
                para_o_territorio = territorio_para_ordenado[0][0]

                quantidade = max(territorio_de['quantidade'] - 1, 1)
                print('MOVE :::: {} de {} para {} quantidade {}'.format(usuario, do_territorio, para_o_territorio,
                                                                        quantidade))
                print('grafo para o territorio {}'.format(grafo[para_o_territorio]))
                jogo.move(usuario, do_territorio, para_o_territorio, quantidade)
                # self.wait_short_time()
        else:
            break


if __name__ == '__main__':
    test_acao_atacar()
    # test_acao_mover()
