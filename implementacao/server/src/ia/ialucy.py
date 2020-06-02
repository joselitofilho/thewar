# -*- coding: utf-8 -*-
import sys
import random
import time

from src.mensagens import *
from src.tipoAcaoTurno import *

from .iainterface import IAInterface


class IALucy(IAInterface):
    def __init__(self, sufixo=''):
        self.usuario = 'Lucy' + sufixo
        self.jogador = None

    def usuario(self):
        return self.usuario

    def jogador_ref(self, value):
        self.jogador = value

    def processa_msg(self, jogo, msg):
        mensagem = Mensagem()
        mensagem.fromJson(msg)
        if mensagem.tipo == TipoMensagem.turno:
            params = mensagem.params
            if params['vezDoJogador']['usuario'] == self.usuario:
                if params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_globais:
                    self.turno_distribuir_tropas_globais(jogo, params)
                # elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
                #     jogo.finalizaTurnoPorTimeout()
                # elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
                #     jogo.finalizaTurnoPorTimeout()
                else:
                    jogo.finalizaTurnoPorTimeout()
                    time.sleep(1)

    def turno_distribuir_tropas_globais(self, jogo, params):
        # numero_do_turno = params['numeroDoTurno']
        # valor_da_troca = params['valorDaTroca']
        # info_jogadores = params['infoJogadores']
        quantidade_de_tropas = params['quantidadeDeTropas']

        # print '1'
        # print 'IALucy', self.usuario, 'turno_distribuir_tropas_globais'
        meus_territorios = self.jogador.territorios
        random.shuffle(meus_territorios)
        territorio = meus_territorios[0].codigo
        quantidade = quantidade_de_tropas
        # print '2', territorio, quantidade
        sys.stdout.flush()

        jogo.colocaTropaReq(self.usuario, territorio, quantidade)
        time.sleep(1)
        # print '3'
        jogo.finalizaTurno(self.usuario)

    def turno_distribuir_tropas_grupo_territorio(self, jogo, params):
        pass

    def turno_distribuir_topas_troca_de_cartas(self, jogo, params):
        pass

    def turno_troca_de_cartas(self, jogo, params):
        pass

    def turno_atacar(self, jogo, params):
        pass

    def turno_mover(self, jogo, params):
        pass
