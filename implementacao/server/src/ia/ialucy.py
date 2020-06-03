# -*- coding: utf-8 -*-
import random

from src.mensagens import *
from src.territorio import *
from src.timeout import *
from src.tipoAcaoTurno import *
from src.carta import *

from .iainterface import IAInterface


class IALucy(IAInterface):
    def __init__(self, sufixo=''):
        self.usuario = 'Lucy' + sufixo
        self.jogador = None

        self.jogando = False
        self.atacando = False

        self.timeout = None
        self.timeout_coloca_tropa = None
        self.timeout_coloca_tropa_grupo_territorio = None
        self.timeout_trocar_cartas = None
        self.timeout_ataca = None
        self.timeout_move_apos_conquistar_territorio = None
        self.timeout_finaliza_turno = None

    def usuario(self):
        return self.usuario

    def jogador_ref(self, value):
        self.jogador = value

    def processa_msg(self, jogo, msg):
        mensagem = Mensagem()
        mensagem.fromJson(msg)
        if mensagem.tipo == TipoMensagem.turno and not self.jogando:
            params = mensagem.params
            if params['vezDoJogador']['usuario'] == self.usuario:
                self.jogando = True
                self.processa_msg_turno(self.usuario, self.jogador, jogo, params)
        elif mensagem.tipo == TipoMensagem.atacar and self.atacando:
            params = mensagem.params
            if params['jogadorAtaque']['usuario'] == self.usuario:
                self.processa_msg_atacar(self.usuario, self.jogador, jogo, params)

    def processa_msg_turno(self, usuario, jogador, jogo, params):
        if params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_globais or params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            self.turno_distribuir_tropas_globais(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            self.turno_distribuir_tropas_grupo_territorio(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.trocar_cartas:
            self.turno_trocar_cartas(usuario, jogador, jogo, params)
        elif params['tipoAcao'] == TipoAcaoTurno.atacar:
            self.turno_atacar(usuario, jogador, jogo)
        elif params['tipoAcao'] == TipoAcaoTurno.mover:
            self.timeout = Timeout(1, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
            self.timeout.start()

    def turno_distribuir_tropas_globais(self, usuario, jogador, jogo, params):
        self.timeout_coloca_tropa = Timeout(2, self.coloca_tropa,
                                            {'usuario': usuario, 'jogador': jogador, 'jogo': jogo, 'params': params})
        self.timeout_coloca_tropa.start()

    def coloca_tropa(self, usuario, jogador, jogo, params):
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

        self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
        self.timeout_finaliza_turno.start()

    def turno_distribuir_tropas_grupo_territorio(self, usuario, jogador, jogo, params):
        self.timeout_coloca_tropa_grupo_territorio = Timeout(2, self.coloca_tropa_grupo_territorio,
                                            {'usuario': usuario, 'jogador': jogador, 'jogo': jogo, 'params': params})
        self.timeout_coloca_tropa_grupo_territorio.start()

    def coloca_tropa_grupo_territorio(self, usuario, jogador, jogo, params):
        grupo_territorio = params['grupoTerritorio']
        quantidade_de_tropas = params['quantidadeDeTropas']

        meus_grupos_territorio = GrupoTerritorio.FronteirasContinentes[grupo_territorio]
        random.shuffle(meus_grupos_territorio)
        territorio = meus_grupos_territorio[0]

        jogo.colocaTropaReq(usuario, territorio, quantidade_de_tropas)

        self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
        self.timeout_finaliza_turno.start()

    def turno_distribuir_tropas_troca_de_cartas(self, usuario, jogador, jogo, params):
        pass

    def turno_trocar_cartas(self, usuario, jogador, jogo, params):
        self.timeout_trocar_cartas = Timeout(2, self.trocar_cartas,
                                             {'usuario': usuario, 'jogador': jogador, 'jogo': jogo, 'params': params})
        self.timeout_trocar_cartas.start()

    def trocar_cartas(self, usuario, jogador, jogo, params):
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
                self.jogando = False
                jogo.trocaCartasTerritorio(usuario, cartas_para_troca)
                return

        self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
        self.timeout_finaliza_turno.start()


    def processa_msg_atacar(self, usuario, jogador, jogo, params):
        conquistou_territorio = params['conquistouTerritorio']

        if conquistou_territorio:
            quantidade = min(params['territoriosDoAtaque'][0]['quantidadeDeTropas'] - 1, 1)
            self.timeout_move_apos_conquistar_territorio = Timeout(2, self.move_apos_conquistar_territorio,
                                                                   {'usuario': usuario, 'jogador': jogador,
                                                                    'jogo': jogo, 'quantidade': quantidade})
            self.timeout_move_apos_conquistar_territorio.start()
        else:
            self.turno_atacar(usuario, jogador, jogo)

    def turno_atacar(self, usuario, jogador, jogo):
        self.atacando = True
        self.timeout_ataca = Timeout(2, self.ataca, {'usuario': usuario, 'jogador': jogador, 'jogo': jogo})
        self.timeout_ataca.start()

    def ataca(self, usuario, jogador, jogo):
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
                        return

        self.atacando = False
        self.timeout_finaliza_turno = Timeout(0.5, self.finaliza_turno, {'jogo': jogo, 'usuario': usuario})
        self.timeout_finaliza_turno.start()

    def move_apos_conquistar_territorio(self, usuario, jogador, jogo, quantidade):
        jogo.moveAposConquistarTerritorio(usuario, quantidade)

        self.turno_atacar(usuario, jogador, jogo)

    def turno_mover(self, jogo, params):
        pass

    def finaliza_turno(self, jogo, usuario):
        self.atacando = False
        self.jogando = False
        jogo.finalizaTurno(usuario)
