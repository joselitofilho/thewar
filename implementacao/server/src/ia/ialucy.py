# -*- coding: utf-8 -*-
import random

from src.mensagens import *
from src.territorio import *
from src.timeout import *
from src.tipoAcaoTurno import *
from src.carta import *

from .iainterface import IAInterface


class IALucy(IAInterface, object):
    def __init__(self, sufixo=''):
        super(IALucy, self).__init__('Lucy' + sufixo)

    def acao_coloca_tropa(self, usuario, jogador, jogo, params):
        quantidade_de_tropas = params['quantidadeDeTropas']
        densidades = jogador.densidadeTodosGruposTerritorio()
        grupo = None
        for densidade in densidades:
            grupo = densidade[0]
            if densidade[1] < 100.0:
                grupo = densidade[0]
                break
        listaGrupo = GrupoTerritorio.Dicionario[grupo]
        codigosTerritorios = []
        for terr in jogador.territorios:
            codigosTerritorios.append(terr.codigo)
        meus_territorios = jogador.territoriosPorGrupo(listaGrupo, codigosTerritorios)

        random.shuffle(meus_territorios)
        territorio = meus_territorios[0]

        jogo.colocaTropaReq(usuario, territorio, quantidade_de_tropas)

        return True

    def acao_coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        grupo_territorio = params['grupoTerritorio']
        quantidade_de_tropas = params['quantidadeDeTropas']

        meus_grupos_territorio = GrupoTerritorio.FronteirasContinentes[grupo_territorio]
        random.shuffle(meus_grupos_territorio)
        territorio = meus_grupos_territorio[0]

        jogo.colocaTropaReq(usuario, territorio, quantidade_de_tropas)

        return True

    def acao_trocar_cartas(self, usuario, jogador, jogo, params):
        minhas_cartas = jogador.cartasTerritorio
        if len(minhas_cartas) >= 3:
            cartasTriangulo = []
            cartasQuadrado = []
            cartasBola = []
            cartasCoringa = []
            for carta in minhas_cartas:
                if carta.codigoTerritorio == CartaForma.Todas:
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
                while(len(cartas_para_troca) < 3):
                    if len(cartasTriangulo) > 0:
                        cartas_para_troca.append(cartasTriangulo.pop(0).codigoTerritorio)
                    elif len(cartasQuadrado) > 0:
                        cartas_para_troca.append(cartasQuadrado.pop(0).codigoTerritorio)
                    elif len(cartasBola) > 0:
                        cartas_para_troca.append(cartasBola.pop(0).codigoTerritorio)
                    elif len(cartasCoringa) > 0:
                        cartas_para_troca.append(cartasCoringa.pop(0).codigoTerritorio)

            if len(cartas_para_troca) == 3:
                jogo.trocaCartasTerritorio(usuario, cartas_para_troca)
                return False

        return True

    def acao_ataca(self, usuario, jogador, jogo):
        meus_territorios = jogador.territorios
        random.shuffle(meus_territorios)
        territoriosInimigos = jogo.territoriosInimigos(usuario)
        random.shuffle(territoriosInimigos)
        for territorio in meus_territorios:
            if territorio.quantidadeDeTropas > 3:
                for inimigo in territoriosInimigos:
                    if territorio.quantidadeDeTropas >= inimigo.quantidadeDeTropas + 3 and FronteiraTerritorio.TemFronteira(
                            inimigo.codigo, territorio.codigo):
                        jogo.ataca(usuario, [territorio.codigo], inimigo.codigo)
                        return False

        return True

    def acao_move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        quantidade = min(params['territoriosDoAtaque'][0]['quantidadeDeTropas'] - 1, 1)
        jogo.moveAposConquistarTerritorio(usuario, quantidade)

        return True

    def acao_move(self, usuario, jogador, jogo):
        return True