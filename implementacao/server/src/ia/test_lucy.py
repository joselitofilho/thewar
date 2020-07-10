#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.desafios.desafios import *
from src.ia.ialucy import *
from src.jogador import *
from src.jogo import *
from src.pontuacao import *


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
    # print('grafo {}'.format(jogo.grafoTerritorios()))

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
    test_acao_mover()
