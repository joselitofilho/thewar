# -*- coding: utf-8 -*-
import random
import sys
import traceback

from src.carta import *
from src.mensagens import *
from src.territorio import *
from src.tipoAcaoTurno import *

from .iainterface import IAInterface


class IALucy(IAInterface):
    def __init__(self, sufixo=''):
        super(IALucy, self).__init__('Lucy' + sufixo)

    def acao_coloca_tropa(self, usuario, jogador, jogo, params):
        try:
            grafo = self.atualiza_grafo(usuario, jogador, jogo)

            quantidade_de_tropas = params['quantidadeDeTropas']
            densidades = jogador.densidadeTodosGruposTerritorio()
            grupo_maior_densidade = densidades[0][0]
            for densidade in densidades:
                if 0.0 < densidade[1] and densidade[1] < 100.0:
                    grupo_maior_densidade = densidade[0]
                    break
            lista_grupo_maior_densidade = GrupoTerritorio.Dicionario[grupo_maior_densidade]
            codigosTerritorios = []
            for terr in jogador.territorios:
                codigosTerritorios.append(terr.codigo)
            meus_territorios_por_grupo_maior_densidade = jogador.territoriosPorGrupo(lista_grupo_maior_densidade,
                                                                                     codigosTerritorios)

            meus_territorios = []
            for terr in jogo.territoriosInimigos(usuario):
                if terr.codigo in lista_grupo_maior_densidade:
                    for adj in grafo[terr.codigo]['fronteiras']:
                        if grafo[adj]['grupo'] == grupo_maior_densidade and grafo[adj]['usuario'] == usuario:
                            meus_territorios.append(grafo[adj]['codigo'])

            if len(meus_territorios) == 0:
                for terr in jogador.territorios:
                    if terr.codigo in meus_territorios_por_grupo_maior_densidade:
                        meus_territorios.append(terr.codigo)

            meu_territorio_escolhido = grafo[meus_territorios[0]]
            for terr in meus_territorios:
                grafo_terr = grafo[terr]
                if grafo_terr['bsr'] == meu_territorio_escolhido['bsr']:
                    qtd_adjacentes_no_grupo_1 = 0
                    for adj in grafo_terr['fronteiras']:
                        if grafo[adj]['grupo'] == grafo_terr['grupo']:
                            qtd_adjacentes_no_grupo_1 += 1
                    qtd_adjacentes_no_grupo_2 = 0
                    for adj in meu_territorio_escolhido['fronteiras']:
                        if meu_territorio_escolhido['grupo'] == grafo[adj]['grupo']:
                            qtd_adjacentes_no_grupo_2 += 1
                    if qtd_adjacentes_no_grupo_1 > qtd_adjacentes_no_grupo_2:
                        meu_territorio_escolhido = grafo_terr
                elif meu_territorio_escolhido['nbsr'] < grafo[terr]['nbsr']:
                    meu_territorio_escolhido = grafo_terr

            if meu_territorio_escolhido:
                territorio_codigo = meu_territorio_escolhido['codigo']
            else:
                territorio_codigo = meus_territorios_por_grupo_maior_densidade[0]

            jogo.colocaTropaReq(usuario, territorio_codigo, quantidade_de_tropas)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("acao_coloca_tropa :: Unexpected exception:", sys.exc_info()[0], flush=True)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            print('grafo {}'.format(jogo.grafoTerritorios(jogo.jogadores)), flush=True)

            terrs = jogador.territorios
            random.shuffle(terrs)
            jogo.colocaTropaReq(usuario, terrs[0].codigo, quantidade_de_tropas)

        return True

    def acao_coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        grupo_territorio = params['grupoTerritorio']
        quantidade_de_tropas = params['quantidadeDeTropas']

        meus_territorios_com_fronteira = GrupoTerritorio.FronteirasContinentes[grupo_territorio]

        meus_territorios = []
        for terr in jogador.territorios:
            if terr.codigo in meus_territorios_com_fronteira:
                meus_territorios.append(terr)

        territorios_inimigos = jogo.territoriosInimigos(usuario)
        territorio_inimigo = None
        meu_territorio_escolhido = None
        for terr in meus_territorios:
            for terr_inimigo in territorios_inimigos:
                if FronteiraTerritorio.TemFronteira(terr.codigo, terr_inimigo.codigo):
                    if territorio_inimigo:
                        if terr_inimigo.quantidadeDeTropas >= territorio_inimigo.quantidadeDeTropas:
                            territorio_inimigo = terr_inimigo
                            meu_territorio_escolhido = terr
                    else:
                        territorio_inimigo = terr_inimigo
                        meu_territorio_escolhido = terr

        if meu_territorio_escolhido:
            territorio_codigo = meu_territorio_escolhido.codigo
        else:
            random.shuffle(meus_territorios)
            territorio_codigo = meus_territorios[0].codigo
        jogo.colocaTropaReq(usuario, territorio_codigo, quantidade_de_tropas)

        return True

    def acao_trocar_cartas(self, usuario, jogador, jogo, params):
        minhas_cartas = jogador.cartasTerritorio
        if len(minhas_cartas) >= 3:
            cartasTriangulo = []
            cartasQuadrado = []
            cartasBola = []
            cartasCoringa = []
            for carta in minhas_cartas:
                if carta.forma == CartaForma.Todas:
                    cartasCoringa.append(carta)
                elif carta.forma == CartaForma.Bola:
                    cartasBola.append(carta)
                elif carta.forma == CartaForma.Quadrado:
                    cartasQuadrado.append(carta)
                elif carta.forma == CartaForma.Triangulo:
                    cartasTriangulo.append(carta)

            cartas_para_troca = []
            if len(cartasTriangulo) >= 3:
                cartas_para_troca = [cartasTriangulo[0].codigoTerritorio,
                                     cartasTriangulo[1].codigoTerritorio,
                                     cartasTriangulo[2].codigoTerritorio]
            elif len(cartasQuadrado) >= 3:
                cartas_para_troca = [cartasQuadrado[0].codigoTerritorio,
                                     cartasQuadrado[1].codigoTerritorio,
                                     cartasQuadrado[2].codigoTerritorio]
            elif len(cartasBola) >= 3:
                cartas_para_troca = [cartasBola[0].codigoTerritorio,
                                     cartasBola[1].codigoTerritorio,
                                     cartasBola[2].codigoTerritorio]
            elif len(cartasTriangulo) > 0 and len(cartasQuadrado) > 0 and len(cartasBola) > 0:
                cartas_para_troca = [cartasTriangulo[0].codigoTerritorio,
                                     cartasQuadrado[0].codigoTerritorio,
                                     cartasBola[0].codigoTerritorio]
            elif len(cartasCoringa) > 0:
                cartas_para_troca.append(cartasCoringa.pop(0).codigoTerritorio)
                while len(cartas_para_troca) < 3:
                    if len(cartasTriangulo) > 0:
                        cartas_para_troca.append(cartasTriangulo.pop(0).codigoTerritorio)
                    elif len(cartasQuadrado) > 0:
                        cartas_para_troca.append(cartasQuadrado.pop(0).codigoTerritorio)
                    elif len(cartasBola) > 0:
                        cartas_para_troca.append(cartasBola.pop(0).codigoTerritorio)
                    elif len(cartasCoringa) > 0:
                        cartas_para_troca.append(cartasCoringa.pop(0).codigoTerritorio)

            if len(cartas_para_troca) >= 3:
                jogo.trocaCartasTerritorio(usuario, cartas_para_troca)
                return False

        return True

    def acao_ataca(self, usuario, jogador, jogo):
        # meus_territorios = jogador.territorios
        # random.shuffle(meus_territorios)
        # territoriosInimigos = jogo.territoriosInimigos(usuario)
        # random.shuffle(territoriosInimigos)
        # for territorio in meus_territorios:
        #     if territorio.quantidadeDeTropas > 3:
        #         for inimigo in territoriosInimigos:
        #             if territorio.quantidadeDeTropas >= inimigo.quantidadeDeTropas + 2 and FronteiraTerritorio.TemFronteira(
        #                     inimigo.codigo, territorio.codigo):
        #                 jogo.ataca(usuario, [territorio.codigo], inimigo.codigo)
        #                 return False
        #
        # return True

        try:
            grafo = self.atualiza_grafo(usuario, jogador, jogo)
            # TODO: Usar variável para saber se houve conquista de território.
            meus_territorios_com_tropa = dict(
                filter(
                    # lambda elem: elem[1]['quantidade'] > 3 and elem[1]['usuario'] == usuario and elem[1]['bst'] != 0,
                    # lambda elem: elem[1]['quantidade'] > 3 and elem[1]['usuario'] == usuario and elem[1]['nbsr'] < 0.5,
                    # lambda elem: elem[1]['quantidade'] > 3 and elem[1]['usuario'] == usuario and (
                    #             elem[1]['quantidade'] >= elem[1]['bst'] * 0.3),
                    lambda elem: elem[1]['quantidade'] > 3 and elem[1]['usuario'] == usuario,
                    grafo.items()))

            if len(meus_territorios_com_tropa) > 0:
                codigo_territorios_inimigos = []
                for t in jogo.territoriosInimigos(usuario):
                    codigo_territorios_inimigos.append(t.codigo)

                for territorio in meus_territorios_com_tropa:
                    territorio_para = {}
                    for territorio_fronteira in meus_territorios_com_tropa[territorio]['fronteiras']:
                        diff_quantidade = meus_territorios_com_tropa[territorio]['quantidade'] - \
                                          grafo[territorio_fronteira]['quantidade']
                        if territorio_fronteira in codigo_territorios_inimigos and diff_quantidade >= 2:
                            territorio_para[territorio_fronteira] = grafo[territorio_fronteira]
                            territorio_para[territorio_fronteira]['diff_quantidade'] = diff_quantidade
                            territorio_para[territorio_fronteira]['mesmo_grupo'] = '1' if grafo[territorio_fronteira][
                                                                                              'grupo'] == \
                                                                                          meus_territorios_com_tropa[
                                                                                              territorio][
                                                                                              'grupo'] else '0'

                    territorio_para_ordenado = sorted(territorio_para.items(),
                                                      key=lambda x: x[1]['mesmo_grupo'] and x[1]['diff_quantidade'],
                                                      reverse=True)
                    if len(territorio_para_ordenado) > 0:
                        territorio_inimigo = territorio_para_ordenado[0][0]
                        jogo.ataca(usuario, [territorio], territorio_inimigo)
                        return False
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("acao_coloca_tropa :: Unexpected exception:", sys.exc_info()[0], flush=True)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            print('grafo {}'.format(jogo.grafoTerritorios(jogo.jogadores)), flush=True)

        return True

    def acao_move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        quantidade = 0
        grafo = self.atualiza_grafo(usuario, jogador, jogo)
        territorio_ataque = grafo[params['territoriosDoAtaque'][0]['codigo']]
        if territorio_ataque['bst'] == 0:
            quantidade = min(params['territoriosDoAtaque'][0]['quantidadeDeTropas'] - 1, 2)

        jogo.moveAposConquistarTerritorio(usuario, quantidade)

    def acao_move(self, usuario, jogador, jogo):
        visitados = []
        qtd_nao_moveu = 0
        while True:
            try:
                grafo = self.atualiza_grafo(usuario, jogador, jogo)

                territorios_com_bst_0 = dict(
                    filter(lambda elem: elem[1]['quantidade'] > 1 and elem[1]['usuario'] == usuario and elem[1][
                        'bst'] == 0 and elem[1]['codigo'] not in visitados, grafo.items()))

                if len(territorios_com_bst_0) > 0:
                    do_territorio = next(iter(territorios_com_bst_0))
                    territorio_de = grafo[do_territorio]
                    territorio_para = {}
                    so_tem_fronteira_com_bst_0 = True
                    for t in territorio_de['fronteiras']:
                        if grafo[t]['usuario'] == usuario and t not in visitados:
                            territorio_para[t] = grafo[t]
                            if grafo[t]['bst'] != 0:
                                so_tem_fronteira_com_bst_0 = False

                    if len(territorio_para) > 0:
                        if so_tem_fronteira_com_bst_0:
                            visitados.append(do_territorio)

                        territorio_para_ordenado = sorted(territorio_para.items(), key=lambda x: x[1]['nbsr'],
                                                          reverse=True)
                        para_o_territorio = territorio_para_ordenado[0][0]

                        quantidade = max(territorio_de['quantidade'] - 1, 1)
                        jogo.move(usuario, do_territorio, para_o_territorio, quantidade)
                        qtd_nao_moveu = 0
                        self.wait_short_time()

                else:
                    break
            except:
                print("acao_move :: Unexpected exception:", sys.exc_info()[0], flush=True)
                print('grafo {}'.format(jogo.grafoTerritorios(jogo.jogadores)), flush=True)
                break

            qtd_nao_moveu += 1
            if qtd_nao_moveu >= 3:
                break
            self.wait_short_time()

        return True
