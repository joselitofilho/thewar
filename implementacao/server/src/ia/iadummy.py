# -*- coding: utf-8 -*-
import random
import sys
import time

from src.carta import *
from src.mensagens import *
from src.territorio import *
from src.tipoAcaoTurno import *

from .iainterface import IAInterface


class IADummy(IAInterface):
    def __init__(self, sufixo=''):
        super(IADummy, self).__init__('Dmy' + sufixo)

    def acao_coloca_tropa(self, usuario, jogador, jogo, params):
        quantidade_de_tropas = params['quantidadeDeTropas']
        terrs = jogador.territorios
        random.shuffle(terrs)
        jogo.colocaTropaReq(usuario, terrs[0].codigo, quantidade_de_tropas)

        return True

    def acao_coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        grupo_territorio = params['grupoTerritorio']
        quantidade_de_tropas = params['quantidadeDeTropas']

        random.shuffle(jogador.territorios)
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
        return True

    def acao_move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        # quantidade = min(params['territoriosDoAtaque'][0]['quantidadeDeTropas'] - 1, 1)
        # NOTE: Por enquanto não vai mover ao atacar.
        quantidade = 0
        jogo.moveAposConquistarTerritorio(usuario, quantidade)

    def acao_move(self, usuario, jogador, jogo):
        return True
