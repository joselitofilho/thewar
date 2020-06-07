# -*- coding: utf-8 -*-

from src.carta import *
from src.mensagens import *
from src.territorio import *
from src.timeout import *
from src.tipoAcaoTurno import *


class IAInterface(object):
    def __init__(self, usuario):
        self.usuario = usuario
        self.jogador = None

        self.timeout = None
        self.timeout_coloca_tropa = None
        self.timeout_coloca_tropa_grupo_territorio = None
        self.timeout_trocar_cartas = None
        self.timeout_ataca = None
        self.timeout_move_apos_conquistar_territorio = None
        self.timeout_finaliza_turno = None

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

    def processa_msg(self, jogo, msg):
        mensagem = Mensagem()
        mensagem.fromJson(msg)
        if mensagem.tipo == TipoMensagem.turno:
            params = mensagem.params
            if params['vezDoJogador']['usuario'] == self.usuario:
                self.processa_msg_turno(self.usuario, self.jogador, jogo, params)
        elif mensagem.tipo == TipoMensagem.atacar:
            params = mensagem.params
            if params['jogadorAtaque']['usuario'] == self.usuario:
                self.processa_msg_atacar(self.usuario, self.jogador, jogo, params)

    def processa_msg_turno(self, usuario, jogador, jogo, params):
        if params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_globais or params[
            'tipoAcao'] == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            self.turno_distribuir_tropas_globais(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            self.turno_distribuir_tropas_grupo_territorio(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.trocar_cartas:
            self.turno_trocar_cartas(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.atacar:
            self.turno_atacar(usuario, jogador, jogo)
        elif params['tipoAcao'] == TipoAcaoTurno.mover:
            self.turno_mover(usuario, jogador, jogo)

    def turno_distribuir_tropas_globais(self, usuario, jogador, jogo, params):
        self.timeout_coloca_tropa = Timeout(2, self.coloca_tropa,
                                            {'usuario': usuario, 'jogador': jogador, 'jogo': jogo, 'params': params})
        self.timeout_coloca_tropa.start()

    def coloca_tropa(self, usuario, jogador, jogo, params):
        if self.acao_coloca_tropa(usuario, jogador, jogo, params):
            self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout_finaliza_turno.start()

    def turno_distribuir_tropas_grupo_territorio(self, usuario, jogador, jogo, params):
        self.timeout_coloca_tropa_grupo_territorio = Timeout(2, self.coloca_tropa_grupo_territorio,
                                                             {'usuario': usuario, 'jogador': jogador, 'jogo': jogo,
                                                              'params': params})
        self.timeout_coloca_tropa_grupo_territorio.start()

    def coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        if self.acao_coloca_tropa_grupo_territorio(usuario, jogador, jogo, params):
            self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout_finaliza_turno.start()

    def turno_distribuir_tropas_troca_de_cartas(self, usuario, jogador, jogo, params):
        pass

    def turno_trocar_cartas(self, usuario, jogador, jogo, params):
        self.timeout_trocar_cartas = Timeout(2, self.trocar_cartas,
                                             {'usuario': usuario, 'jogador': jogador, 'jogo': jogo, 'params': params})
        self.timeout_trocar_cartas.start()

    def trocar_cartas(self, usuario, jogador, jogo, params):
        if self.acao_trocar_cartas(usuario, jogador, jogo, params):
            self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout_finaliza_turno.start()

    def processa_msg_atacar(self, usuario, jogador, jogo, params):
        conquistou_territorio = params['conquistouTerritorio']

        if conquistou_territorio:
            self.timeout_move_apos_conquistar_territorio = Timeout(2, self.move_apos_conquistar_territorio,
                                                                   {'usuario': usuario, 'jogador': jogador,
                                                                    'jogo': jogo, 'params': params})
            self.timeout_move_apos_conquistar_territorio.start()
        else:
            self.turno_atacar(usuario, jogador, jogo)

    def turno_atacar(self, usuario, jogador, jogo):
        self.timeout_ataca = Timeout(2, self.ataca, {'usuario': usuario, 'jogador': jogador, 'jogo': jogo})
        self.timeout_ataca.start()

    def ataca(self, usuario, jogador, jogo):
        if self.acao_ataca(usuario, jogador, jogo):
            self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout_finaliza_turno.start()

    def move_apos_conquistar_territorio(self, usuario, jogador, jogo, params):
        if self.acao_move_apos_conquistar_territorio(usuario, jogador, jogo, params):
            self.turno_atacar(usuario, jogador, jogo)

    def turno_mover(self, usuario, jogador, jogo):
        self.timeout_move = Timeout(2, self.move, {'usuario': usuario, 'jogador': jogador, 'jogo': jogo})
        self.timeout_move.start()

    def move(self, usuario, jogador, jogo):
        if self.acao_move(usuario, jogador, jogo):
            self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout_finaliza_turno.start()

    def finaliza_turno(self, jogo, usuario):
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
