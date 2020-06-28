# -*- coding: utf-8 -*-

import threading
import time

try:
    import queue
except ImportError:
    import Queue as queue

from src.carta import *
from src.mensagens import *
from src.territorio import *
from src.timeout import *
from src.tipoAcaoTurno import *


class IAInterface(threading.Thread):
    def __init__(self, usuario):
        threading.Thread.__init__(self)
        self.loop = False

        self.mensagem = None
        self.usuario = usuario
        self.jogador = None
        self.jogo = None
        self.grafo_territorios = None

        self.queue_msgs = queue.Queue()

    def __del__(self):
        self.para()

    def acao_coloca_tropa(self, usuario, jogador, jogo, params):
        raise NotImplementedError()

    def acao_coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        raise NotImplementedError()

    def acao_trocar_cartas(self, usuario, jogador, jogo, params):
        raise NotImplementedError()

    def acao_ataca(self, usuario, jogador, jogo):
        raise NotImplementedError()

    def acao_move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        raise NotImplementedError()

    def acao_move(self, usuario, jogador, jogo):
        raise NotImplementedError()

    def usuario(self):
        return self.usuario

    def jogador_ref(self, value):
        self.jogador = value

    def wait_short_time(self):
        time.sleep(0.5)

    def wait_mid_time(self):
        time.sleep(1)

    def wait_long_time(self):
        time.sleep(2)

    def run(self):
        self.loop = True
        while self.loop:
            msg = self.queue_msgs.get()
            if msg:
                self.mensagem = Mensagem()
                self.mensagem.fromJson(msg)
                if self.mensagem.tipo == TipoMensagem.turno:
                    params = self.mensagem.params
                    if params['vezDoJogador']['usuario'] == self.usuario:
                        self.processa_msg_turno(self.usuario, self.jogador, self.jogo, params)
                elif self.mensagem.tipo == TipoMensagem.atacar:
                    params = self.mensagem.params
                    if params['jogadorAtaque']['usuario'] == self.usuario:
                        self.processa_msg_atacar(self.usuario, self.jogador, self.jogo, params)
                elif self.mensagem.tipo == TipoMensagem.mover:
                    params = self.mensagem.params
                    if params['jogador'] == self.usuario:
                        pass
                elif self.mensagem.tipo == TipoMensagem.erro:
                    print('ERROR MSG ', self.usuario)

            self.wait_short_time()

    def para(self):
        self.loop = False

    def processa_msg(self, jogo, msg):
        self.queue_msgs.put(msg)
        self.jogo = jogo

    def processa_msg_turno(self, usuario, jogador, jogo, params):
        if params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_globais:
            self.turno_distribuir_tropas_globais(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            self.turno_distribuir_tropas_grupo_territorio(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            self.turno_distribuir_tropas_troca_de_cartas(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.trocar_cartas:
            self.turno_trocar_cartas(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.atacar:
            self.turno_atacar(usuario, jogador, jogo)
        elif params['tipoAcao'] == TipoAcaoTurno.mover:
            self.turno_mover(usuario, jogador, jogo)

    def turno_distribuir_tropas_globais(self, usuario, jogador, jogo, params):
        self.wait_mid_time()
        self.coloca_tropa(usuario, jogador, jogo, params)

    def coloca_tropa(self, usuario, jogador, jogo, params):
        if self.acao_coloca_tropa(usuario, jogador, jogo, params):
            self.wait_short_time()
            self.finaliza_turno(usuario, jogo)

    def turno_distribuir_tropas_grupo_territorio(self, usuario, jogador, jogo, params):
        self.wait_mid_time()
        self.coloca_tropa_grupo_territorio(usuario, jogador, jogo, params)

    def coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        if self.acao_coloca_tropa_grupo_territorio(usuario, jogador, jogo, params):
            self.wait_short_time()
            self.finaliza_turno(usuario, jogo)

    def turno_distribuir_tropas_troca_de_cartas(self, usuario, jogador, jogo, params):
        self.wait_mid_time()
        self.coloca_tropa(usuario, jogador, jogo, params)

    def turno_trocar_cartas(self, usuario, jogador, jogo, params):
        self.wait_mid_time()
        self.trocar_cartas(usuario, jogador, jogo, params)

    def trocar_cartas(self, usuario, jogador, jogo, params):
        if self.acao_trocar_cartas(usuario, jogador, jogo, params):
            self.wait_short_time()
            self.finaliza_turno(usuario, jogo)

    def processa_msg_atacar(self, usuario, jogador, jogo, params):
        conquistou_territorio = params['conquistouTerritorio']

        if conquistou_territorio:
            self.wait_short_time()
            self.move_apos_conquistar_territorio(usuario, jogador, jogo, params)
        else:
            self.turno_atacar(usuario, jogador, jogo)

    def turno_atacar(self, usuario, jogador, jogo):
        self.wait_mid_time()
        self.ataca(usuario, jogador, jogo)

    def ataca(self, usuario, jogador, jogo):
        if self.acao_ataca(usuario, jogador, jogo):
            self.wait_short_time()
            self.finaliza_turno(usuario, jogo)

    def move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        self.acao_move_apos_conquistar_territorio(usuario, jogador, jogo, params)

    def turno_mover(self, usuario, jogador, jogo):
        self.wait_mid_time()
        self.move(usuario, jogador, jogo)

    def move(self, usuario, jogador, jogo):
        if self.acao_move(usuario, jogador, jogo):
            self.wait_short_time()
            self.finaliza_turno(usuario, jogo)

    def finaliza_turno(self, usuario, jogo):
        jogo.finalizaTurno(usuario)

    def situacao_territorios(self, usuario, jogador, jogo):
        meus_territorios = jogador.territorios
        territorios_inimigos = jogo.territoriosInimigos(usuario)

        densidade_por_grupos = jogador.densidadeTodosGruposTerritorio()

        codigos_meus_territorios = []
        for terr in meus_territorios:
            codigos_meus_territorios.append(terr.codigo)
        meus_territorios_por_grupo = []
        for grupo in GrupoTerritorio.Dicionario:
            meus_territorios_por_grupo[grupo] = jogador.territoriosPorGrupo(GrupoTerritorio.Dicionario[grupo],
                                                                            codigos_meus_territorios)

        # FronteiraTerritorio.Fronteiras[territorio.codigo]
        # GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.CONTINENTE]

        return {
            'meus_territorios': meus_territorios,
            'territorios_inimigos': territorios_inimigos,
            'densidade_por_grupos': densidade_por_grupos,
            'meus_territorios_por_grupo': meus_territorios_por_grupo
        }

    def atualiza_grafo(self, usuario, jogador, jogo):
        self.grafo_territorios = jogo.grafoTerritorios()

        bst = self.bst(usuario, jogador)
        # print('BST', usuario, bst)
        bsr = self.bsr(usuario, jogador)
        # print('BSR', usuario, bsr)
        nbsr = self.nbsr(usuario, jogador, bsr)
        # print('NBSR', usuario, nbsr)

        for t in self.grafo_territorios:
            if t in bst:
                self.grafo_territorios[t]['bst'] = bst[t]
            if t in bsr:
                self.grafo_territorios[t]['bsr'] = bsr[t]
            if t in nbsr:
                self.grafo_territorios[t]['nbsr'] = nbsr[t]

        return self.grafo_territorios

    def bst(self, usuario, jogador):
        res = {}
        meus_territorios = jogador.territorios
        for territorio in meus_territorios:
            bst = 0.0
            for adjacente in self.grafo_territorios[territorio.codigo]['fronteiras']:
                if self.grafo_territorios[adjacente]['usuario'] != usuario:
                    bst = bst + self.grafo_territorios[adjacente]['quantidade']
            res[territorio.codigo] = bst

        return res

    def bsr(self, usuario, jogador):
        res = {}
        meus_territorios = jogador.territorios
        for territorio in meus_territorios:
            bst = 0.0
            for adjacente in self.grafo_territorios[territorio.codigo]['fronteiras']:
                if self.grafo_territorios[adjacente]['usuario'] != usuario:
                    bst = bst + self.grafo_territorios[adjacente]['quantidade']
            res[territorio.codigo] = bst / self.grafo_territorios[territorio.codigo]['quantidade']

        return res

    def nbsr(self, usuario, jogador, bsr):
        res = {}
        meus_territorios = jogador.territorios
        for territorio in meus_territorios:
            sum = bsr[territorio.codigo]
            for adjacente in self.grafo_territorios[territorio.codigo]['fronteiras']:
                if self.grafo_territorios[adjacente]['usuario'] == usuario:
                    sum = sum + bsr[adjacente]
            res[territorio.codigo] = 0 if sum == 0 else bsr[territorio.codigo] / sum

        return res
