#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import logging
import random
import time

from src.carta import *
from src.chat.chat import *
from src.grupousuariosdb import *
from src.historicojogo import *
from src.jsonserializer import *
from src.mensagens import *
from src.objetivos import *
from src.pontuacao import *
from src.territorio import *
from src.tipoAcaoTurno import *
from src.turno import *


class Jogo(object):
    def __init__(self, nome, jogadores, cpus, clientes=None, gerenciador=None):
        random.seed()
        self.iniciou_em = int(time.time() * 1000)
        self.terminou_em = None
        self.TAG = 'jogo_{}_{}'.format(nome, self.iniciou_em)

        self.gerenciador = gerenciador

        self.nome = nome
        self.turno = Turno()

        self.clientes = clientes
        self.jogadores = jogadores
        self.cpus = cpus

        self.olheiros = {}

        self.qtd_turnos_sem_jogadores_humanos = 0
        self.quemJaJogou = 0

        self.jogadorQueComecou = -1

        self.ordemJogadores = list(self.jogadores.keys())
        random.shuffle(self.ordemJogadores)

        self.quantidade_troca_por_jogador = {}
        for k, v in self.jogadores.items():
            self.quantidade_troca_por_jogador[v.usuario] = 0

        # Indice que aponta para a fila da ordem dos jogador.
        self.indiceOrdemJogadores = None
        # Posicao do jogador que esta jogando no momento.
        self.posicaoJogadorDaVez = None
        # Cabeca da fila que auxiliara a decisao do proximo jogador que ira jogar.
        self.cabecaDaFila = None

        self.cartasTerritorioDoBaralho = []
        self.cartasTerritorioDescartadas = []

        self.jogadorDaVezConquistouTerritorio = False

        self.numeroDaTroca = 1

        self.obrigatorioPassarAVez = False

        self.contabilizouPontos = False

        self.jogadorVencedor = None

        self.pontuacaoPelaVitoria = 0

        self.estaAtacando = False

        self.chat = Chat()

        self.pontuacao_jogadores = {}

    def prepara_para_comecar(self):
        # Distribui os territorios e define quem comeca.
        jogoFaseIMsg = self.faseI_Inicia()
        self.enviaMsgParaTodos(TipoMensagem.jogo_fase_I, jogoFaseIMsg)

        # Envia a carta objetivo para cada jogador individualmente.
        cartasObjetivos = self.faseI_DefinirObjetivos()
        for i in range(len(self.jogadores)):
            posicaoJogador = self.ordemJogadores[i]
            self.enviaMsgParaJogador(TipoMensagem.carta_objetivo, CartaObjetivo(cartasObjetivos[i]),
                                     self.jogadores[posicaoJogador])

        logging.info("{} jogadores {}".format(self.TAG, json.dumps(self.jogadores, cls=SerializerEncoder)))

    def faseI_Inicia(self):
        self.jogadorQueComecou = self.faseI_DefinirQuemComeca()
        territoriosDosJogadores = self.faseI_DistribuirTerritorios()
        logging.info(
            '{} {} ID jogo: {} - sockets: {} - maquina: {}'.format(
                self.TAG, datetime.datetime.now(), self.nome, 0 if self.clientes is None else len(self.clientes),
                len(self.cpus)))
        return JogoFaseI(self.jogadorQueComecou, territoriosDosJogadores)

    def faseI_DefinirQuemComeca(self):
        numeroAleatorio = random.randint(0, len(self.jogadores) - 1)
        self.cabecaDaFila = numeroAleatorio
        self.indiceOrdemJogadores = self.cabecaDaFila
        self.posicaoJogadorDaVez = self.ordemJogadores[self.cabecaDaFila]

        return self.posicaoJogadorDaVez

    def faseI_DistribuirTerritorios(self):
        territorios = list(CodigoTerritorio.Lista)
        random.shuffle(territorios)

        listaTerritoriosPorJogador = []
        incremento = []

        # Calculando incremento.
        quantidadeDeJogadores = len(self.jogadores)
        if quantidadeDeJogadores == 4:
            incremento.append(10)
            incremento.append(10)
            incremento.append(11)
            incremento.append(11)
        elif quantidadeDeJogadores == 5:
            incremento.append(8)
            incremento.append(8)
            incremento.append(8)
            incremento.append(9)
            incremento.append(9)
        else:
            for i in range(quantidadeDeJogadores):
                incremento.append(42 // quantidadeDeJogadores)
        inicio = 0
        fim = 0
        for i in range(quantidadeDeJogadores):
            fim = fim + incremento[i]

            territoriosJogador_i = []
            for j in range(inicio, fim):
                territoriosJogador_i.append(territorios[j])

            self.jogadores[self.posicaoJogadorDaVez].iniciaTerritorios(territoriosJogador_i)
            listaTerritoriosPorJogador.append(
                TerritoriosPorJogador(self.posicaoJogadorDaVez, self.jogadores[self.posicaoJogadorDaVez].territorios))

            inicio = inicio + incremento[i]
            self.passaParaProximoJogador(False)

        return listaTerritoriosPorJogador

    def faseI_DefinirObjetivos(self):
        objetivos = list(range(0, 13))
        random.shuffle(objetivos)

        objetivoPorJogadores = []
        for i in range(len(self.jogadores)):
            posicaoJogador = self.ordemJogadores[i]
            self.jogadores[posicaoJogador].objetivo = objetivos[i]
            objetivoPorJogadores.append(objetivos[i])

        return objetivoPorJogadores

    def iniciaTurnos(self):
        self.cartasTerritorioDoBaralho = list(CartasTerritorio.Todas())
        random.shuffle(self.cartasTerritorioDoBaralho)
        self.cartasTerritorioDescartadas = []

        self.numeroDaTroca = 1

        self.qtd_turnos_sem_jogadores_humanos = 0

        self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
        acaoDoTurno = self.criaAcaoDoTurno(self.turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

    def criaAcaoDoTurno(self, turno):
        # Qual o turno que esta: 1, 2, 3, ...
        numeroDoTurno = turno.numero
        # Quem esta jogando: posicao do jogador...
        jogadorDaVez = self.posicaoJogadorDaVez
        # Qual a acao que ele deve fazer...
        tipoAcaoDoTurno = turno.tipoAcao

        tempoRestante = turno.tempoRestante
        valorDaTroca = self.calculaQuantidadeDeTropasDaTroca(self.numeroDaTroca)

        jogador = self.jogadores[jogadorDaVez]
        infoJogadorDaVez = {
            "usuario": jogador.usuario,
            "posicao": jogador.posicao
        }

        infoJogadores = []
        #  Monta a lista das informações dos jogadores
        for j in self.jogadores.values():
            infoJogadores.append({
                "usuario": j.usuario,
                "posicao": j.posicao,
                "tipo": j.tipo,
                "total_territorios": len(j.territorios),
                "total_cartas_territorio": len(j.cartasTerritorio),
                "esta_na_sala": j.posicao in self.clientes.keys() if j.tipo == TipoJogador.humano else True
            })

        jogadorQueComecou = self.jogadorQueComecou
        ordemJogadores = self.ordemJogadores

        acao = None
        # Preencher os dados da acao
        if tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_globais:
            if turno.quantidadeDeTropas == 0:
                qtd = len(jogador.territorios) // 2
                if qtd > 3:
                    turno.quantidadeDeTropas = qtd
                else:
                    turno.quantidadeDeTropas = 3
            territoriosDosJogadores = self.listaDeTerritoriosDosJogadores()
            acao = AcaoDistribuirTropasGlobais(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante,
                                               valorDaTroca, turno.quantidadeDeTropas, territoriosDosJogadores,
                                               infoJogadores, jogadorQueComecou, ordemJogadores)
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            turno.grupoTerritorioAtual = None
            for grupo in turno.gruposTerritorio:
                turno.grupoTerritorioAtual = grupo
                break
            if turno.quantidadeDeTropas == 0:
                turno.quantidadeDeTropas = GrupoTerritorio.BonusPorGrupo[turno.grupoTerritorioAtual]
            acao = AcaoDistribuirTropasGrupoTerritorio(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante,
                                                       valorDaTroca, turno.quantidadeDeTropas,
                                                       turno.grupoTerritorioAtual, infoJogadores, jogadorQueComecou,
                                                       ordemJogadores)
        elif tipoAcaoDoTurno == TipoAcaoTurno.trocar_cartas:
            acao = AcaoTrocarCartas(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca,
                                    (len(jogador.cartasTerritorio) >= 5), infoJogadores, jogadorQueComecou,
                                    ordemJogadores)
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            acao = AcaoDistribuirTropasTrocaDeCartas(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante,
                                                     valorDaTroca, turno.quantidadeDeTropas, infoJogadores,
                                                     jogadorQueComecou, ordemJogadores)
        elif tipoAcaoDoTurno == TipoAcaoTurno.jogo_terminou:
            ganhador = {
                "usuario": jogador.usuario,
                "pontos": self.pontuacaoPelaVitoria
            }

            acao = AcaoJogoTerminou(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca,
                                    jogador.objetivo, ganhador, infoJogadores, jogadorQueComecou, ordemJogadores)
        else:
            acao = AcaoTurno(tipoAcaoDoTurno, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca,
                             infoJogadores, jogadorQueComecou, ordemJogadores)
        return acao

    def todosJogaram(self):
        return self.quemJaJogou > len(self.ordemJogadores) - 1

    def passaParaProximoJogador(self, comVerificacaoExtra=True):
        # Verifica se o jogador ainda esta no jogo. Caso nao esteja, pula a vez dele.
        ok = False

        if comVerificacaoExtra:
            self.quemJaJogou += 1
        self.indiceOrdemJogadores = (self.indiceOrdemJogadores + 1) % len(self.ordemJogadores)
        self.posicaoJogadorDaVez = self.ordemJogadores[self.indiceOrdemJogadores]
        self.jogadorDaVezConquistouTerritorio = False

        jogador = self.jogadores[self.posicaoJogadorDaVez]
        jogadorEstaOn = True
        if jogador.tipo == TipoJogador.humano:
            # Verifica se o jogador esta logado na sala e nao foi destruido.
            # TODO: Se o jogador não estiver na sala, usar um BOT no lugar.
            jogadorEstaOn = True if self.clientes is None else self.posicaoJogadorDaVez in self.clientes.keys()

        if jogadorEstaOn:
            if not comVerificacaoExtra:
                ok = True
            elif len(jogador.territorios) > 0:
                ok = True

        if not ok:
            return self.passaParaProximoJogador(comVerificacaoExtra)
        return ok

    def finalizaTurno_1(self):
        if self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais and self.turno.quantidadeDeTropas == 0:
            jogador = self.jogadores[self.posicaoJogadorDaVez]
            if len(jogador.gruposTerritorio()) > 0:
                self.turno.gruposTerritorio = list(jogador.gruposTerritorio())
                self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            else:
                if not self.temUmVencedor():
                    self.passaParaProximoJogador()

                    if self.todosJogaram():
                        self.quemJaJogou = 0
                        self.turno.numero = 2
                        self.turno.tipoAcao = TipoAcaoTurno.atacar

                        if len(self.cpus) > 0 and not self.temJogadorOnLine():
                            self.qtd_turnos_sem_jogadores_humanos += 1
                        if self.qtd_turnos_sem_jogadores_humanos > 3:
                            return self.gerenciador.jogoTerminou(self.nome)
                    else:
                        self.turno.numero = 1
                        self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

                    self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                    acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                    self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

            if self.temUmVencedor() and self.gerenciador is not None:
                self.jogoTerminou()

        elif self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio and self.turno.quantidadeDeTropas == 0:
            try:
                self.turno.gruposTerritorio.pop(0)
            except:
                logging.error("{} Nao tem grupo territorio para remover.".format(self.TAG))

            if len(self.turno.gruposTerritorio) == 0:
                if self.temUmVencedor():
                    self.turno.tipoAcao = TipoAcaoTurno.jogo_terminou
                else:
                    self.passaParaProximoJogador()

                    if self.todosJogaram():
                        self.quemJaJogou = 0
                        self.turno.numero = 2
                        self.turno.tipoAcao = TipoAcaoTurno.atacar

                        if len(self.cpus) > 0 and not self.temJogadorOnLine():
                            self.qtd_turnos_sem_jogadores_humanos += 1
                        if self.qtd_turnos_sem_jogadores_humanos > 3:
                            return self.gerenciador.jogoTerminou(self.nome)
                    else:
                        self.turno.numero = 1
                        self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

            if self.temUmVencedor() and self.gerenciador != None:
                self.jogoTerminou()

    def finalizaTurno_2(self):
        # turno = self.turno

        if self.turno.tipoAcao == TipoAcaoTurno.atacar:
            self.turno.numero = 2
            self.turno.tipoAcao = TipoAcaoTurno.mover
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

        elif self.turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            if self.turno.tropasParaMoverAposAtaque < 3:
                self.finalizaTurno_moverAposConquistarTerritorio()

        elif self.turno.tipoAcao == TipoAcaoTurno.mover:
            if self.temUmVencedor():
                self.turno.tipoAcao = TipoAcaoTurno.jogo_terminou
            else:
                self.enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio()

                self.passaParaProximoJogador()

                if self.todosJogaram():
                    self.quemJaJogou = 0
                    self.turno.numero = 3
                    self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

                    if len(self.cpus) > 0 and not self.temJogadorOnLine():
                        self.qtd_turnos_sem_jogadores_humanos += 1
                    if self.qtd_turnos_sem_jogadores_humanos > 3:
                        return self.gerenciador.jogoTerminou(self.nome)
                else:
                    self.turno.numero = 2
                    self.turno.tipoAcao = TipoAcaoTurno.atacar

            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

            if self.temUmVencedor() and self.gerenciador != None:
                self.jogoTerminou()

    def finalizaTurno_I(self):
        # turno = self.turno
        erro = True
        jogador = self.jogadores[self.posicaoJogadorDaVez]

        if self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais:
            if self.turno.quantidadeDeTropas == 0:
                if len(jogador.gruposTerritorio()) > 0:
                    self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
                    self.turno.gruposTerritorio = list(jogador.gruposTerritorio())
                elif len(jogador.cartasTerritorio) > 2:
                    self.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    self.turno.tipoAcao = TipoAcaoTurno.atacar

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            if self.turno.quantidadeDeTropas == 0:
                try:
                    self.turno.gruposTerritorio.pop(0)
                except Exception:
                    logging.error("{} Nao tem grupo territorio para remover.".format(self.TAG))

                if len(self.turno.gruposTerritorio) == 0:
                    if len(jogador.cartasTerritorio) > 2:
                        self.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                    else:
                        self.turno.tipoAcao = TipoAcaoTurno.atacar

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            if self.turno.quantidadeDeTropas == 0:
                if len(jogador.cartasTerritorio) > 2:
                    self.turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    self.turno.tipoAcao = TipoAcaoTurno.atacar

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif self.turno.tipoAcao == TipoAcaoTurno.trocar_cartas:
            if len(jogador.cartasTerritorio) < 5 or self.obrigatorioPassarAVez:
                if self.obrigatorioPassarAVez:
                    self.turno.tipoAcao = TipoAcaoTurno.mover
                else:
                    self.turno.tipoAcao = TipoAcaoTurno.atacar

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False
                self.obrigatorioPassarAVez = False

        elif self.turno.tipoAcao == TipoAcaoTurno.atacar:
            self.turno.tipoAcao = TipoAcaoTurno.mover
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            erro = False

        elif self.turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            if self.turno.tropasParaMoverAposAtaque < 3:
                self.finalizaTurno_moverAposConquistarTerritorio()
                erro = False

        elif self.turno.tipoAcao == TipoAcaoTurno.mover:
            if self.temUmVencedor():
                self.turno.tipoAcao = TipoAcaoTurno.jogo_terminou
            else:
                self.enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio()

                self.passaParaProximoJogador()
                self.turno.trocouCartas = False

                if self.todosJogaram():
                    self.quemJaJogou = 0
                    self.turno.numero += 1

                    if len(self.cpus) > 0 and not self.temJogadorOnLine():
                        self.qtd_turnos_sem_jogadores_humanos += 1
                    if self.qtd_turnos_sem_jogadores_humanos > 3:
                        return self.gerenciador.jogoTerminou(self.nome)
                self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

            erro = False
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

            if self.temUmVencedor() and self.gerenciador != None:
                self.jogoTerminou()

        if erro:
            self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)

    def finalizaTurno(self, usuario):
        posicaoJogador = -1
        for k, v in self.jogadores.items():
            if v.usuario == usuario:
                posicaoJogador = k

        if posicaoJogador == self.posicaoJogadorDaVez:
            if self.turno.numero == 1:
                self.finalizaTurno_1()
            elif self.turno.numero == 2:
                self.finalizaTurno_2()
            else:
                self.finalizaTurno_I()

    def finalizaTurnoPorTimeout(self):
        self.turno.reiniciaVariaveisExtras()
        if self.turno.tipoAcao == TipoAcaoTurno.trocar_cartas:
            self.obrigatorioPassarAVez = True
        else:
            self.obrigatorioPassarAVez = False

        if self.turno.numero == 1:
            self.finalizaTurno_1()
        elif self.turno.numero == 2:
            self.finalizaTurno_2()
        else:
            self.finalizaTurno_I()

    def finalizaTurno_moverAposConquistarTerritorio(self):
        self.turno.reiniciaVariaveisExtrasMoverAposConquistar()
        self.turno.tipoAcao = TipoAcaoTurno.atacar
        acaoDoTurno = self.criaAcaoDoTurno(self.turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

    def posicaoDoUsuario(self, usuario):
        posicaoJogador = -1
        for k, v in self.jogadores.items():
            if v.usuario == usuario:
                posicaoJogador = k
                break
        return posicaoJogador

    def colocaTropaReq(self, usuario, codigoTerritorio, quantidade):
        # turno = self.turno
        jogador = self.jogadores[self.posicaoJogadorDaVez]

        erro = True
        if jogador.usuario == usuario:
            if self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais or \
                    self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
                if quantidade <= self.turno.quantidadeDeTropas and jogador.temTerritorio(codigoTerritorio):
                    self.turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = self.turno.quantidadeDeTropas

                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa,
                                           ColocarTropa(self.jogadores[self.posicaoJogadorDaVez].usuario,
                                                        quantidade,
                                                        territorio,
                                                        quantidadeTotalRestante))
                    erro = False
            elif self.turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
                if quantidade <= self.turno.quantidadeDeTropas and \
                        jogador.temTerritorio(codigoTerritorio) and \
                        codigoTerritorio in GrupoTerritorio.Dicionario[self.turno.grupoTerritorioAtual]:
                    self.turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = self.turno.quantidadeDeTropas

                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa,
                                           ColocarTropa(self.jogadores[self.posicaoJogadorDaVez].usuario,
                                                        quantidade,
                                                        territorio,
                                                        quantidadeTotalRestante))
                    erro = False

    def colocaTropaNaTrocaDeCartasTerritorios(self, posicaoJogador, cartasParaTroca):
        territoriosBeneficiados = []
        jogador = self.jogadores[posicaoJogador]

        # Verifica se o jogador tem os territorios das cartas, se tiver, adiciona duas tropas nele.
        for carta in cartasParaTroca:
            if jogador.temTerritorio(carta.codigoTerritorio):
                territorio = jogador.adicionaTropasNoTerritorio(carta.codigoTerritorio, 2)
                territoriosBeneficiados.append(territorio);

        self.enviaMsgParaTodos(TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios,
                               ColocarTropaNaTrocaDeCartasTerritorios(self.jogadores[posicaoJogador].usuario,
                                                                      territoriosBeneficiados))

    def ataca(self, usuario, dosTerritorios, paraOTerritorio):
        # turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]

        if jogador.usuario == usuario:
            if self.turno.tipoAcao == TipoAcaoTurno.atacar:
                if not self.estaAtacando and jogador.temOsTerritorios(dosTerritorios) and not jogador.temTerritorio(
                        paraOTerritorio):
                    self.estaAtacando = True
                    temErro = False

                    # Recuperando territorio da defesa.
                    #   - Identifica o jogador que esta sendo atacado;
                    #   - Identifica o territorio que esta sendo atacado;
                    #   - Pega a quantidade de tropas desse territorio.
                    for k, v in self.jogadores.items():
                        if v.temTerritorio(paraOTerritorio):
                            jogadorDefesa = v
                            territorioDaDefesa = jogadorDefesa.seuTerritorio(paraOTerritorio)
                            quantidadeDadosDefesa = territorioDaDefesa.quantidadeDeTropas
                            if quantidadeDadosDefesa > 3:
                                quantidadeDadosDefesa = 3
                            break

                    if quantidadeDadosDefesa > 0:
                        # Sortear os dados da defesa.
                        dadosDefesa = []
                        for t in range(0, quantidadeDadosDefesa):
                            valorDado = self.jogarDado()
                            dadosDefesa.append(valorDado)
                        dadosDefesa = sorted(dadosDefesa, reverse=True)

                        # Recuperando territorios do ataque.
                        territoriosDoAtaque = []
                        quantidadeDadosAtaque = 0
                        for t in dosTerritorios:
                            territorioObj = jogador.seuTerritorio(t)
                            if (territorioObj.quantidadeDeTropas > 1 and
                                    FronteiraTerritorio.TemFronteira(
                                        territorioDaDefesa.codigo, territorioObj.codigo)):
                                territoriosDoAtaque.append(territorioObj)

                                if territorioObj.quantidadeDeTropas > 3:
                                    quantidadeDadosAtaque += territorioObj.quantidadeDeTropas
                                elif territorioObj.quantidadeDeTropas > 1:
                                    quantidadeDadosAtaque += territorioObj.quantidadeDeTropas - 1
                                else:
                                    temErro = True
                            else:
                                temErro = True
                                break

                        if not temErro:
                            if quantidadeDadosAtaque > 3:
                                quantidadeDadosAtaque = 3

                            # Sortear os dados do ataque.
                            dadosAtaque = []
                            for i in range(0, quantidadeDadosAtaque):
                                valorDado = self.jogarDado()
                                dadosAtaque.append(valorDado)
                            dadosAtaque = sorted(dadosAtaque, reverse=True)

                            conquistouTerritorio = False

                            # Efetuar ataque e descontar as tropas dos territorios envolvidos nele.
                            for i in range(len(dadosAtaque)):
                                if i < len(dadosDefesa):
                                    if dadosAtaque[i] > dadosDefesa[i]:
                                        # Ataque venceu.
                                        territorioDaDefesa = jogadorDefesa.removeTropasNoTerritorio(
                                            territorioDaDefesa.codigo, 1)

                                        # Verifica se o territorio foi conquistado.
                                        if territorioDaDefesa.quantidadeDeTropas == 0:
                                            # jogadorDefesa.territorios.remove(territorioDaDefesa)
                                            # jogador.territorios.append(territorioDaDefesa)

                                            # # Movendo uma tropa para o territorio conquistado.
                                            # territorioDaDefesa = jogador.adicionaTropasNoTerritorio(
                                            #     territorioDaDefesa.codigo, 1)

                                            jogadorDefesa.removeTerritorio(territorioDaDefesa.codigo)
                                            territorioDaDefesa.quantidadeDeTropas = 1
                                            jogador.adicionaTerritorio(territorioDaDefesa)

                                            for t in territoriosDoAtaque:
                                                if t.quantidadeDeTropas > 1:
                                                    jogador.removeTropasNoTerritorio(t.codigo, 1)
                                                    break
                                            ######

                                            conquistouTerritorio = True

                                            # Verifica se o jogador destruiu o outro. Caso positivo, as cartas dos territorios
                                            # do jogador derrotado vai para o jogador que o destruiu.
                                            if len(jogadorDefesa.territorios) == 0:
                                                jogador.jogadoresDestruidos.append(jogadorDefesa.posicao)
                                                jogador.cartasTerritorio.extend(jogadorDefesa.cartasTerritorio)

                                                # Envia as cartas atualizadas para o cliente.
                                                self.enviaMsgParaJogador(TipoMensagem.cartas_territorio,
                                                                         jogador.cartasTerritorio,
                                                                         jogador)

                                                # Envia para todos que o jogador foi destruido.
                                                self.enviaMsgParaTodos(TipoMensagem.jogador_destruido,
                                                                       JogadorDestruido(jogadorDefesa))

                                            self.jogadorDaVezConquistouTerritorio = True
                                            self.turno.tropasParaMoverAposAtaque = 0
                                            self.turno.territoriosDoAtaqueDaConquista = []
                                            for t in territoriosDoAtaque:
                                                if t.quantidadeDeTropas > 1:
                                                    self.turno.territoriosDoAtaqueDaConquista.append(t.codigo)
                                                    self.turno.tropasParaMoverAposAtaque += t.quantidadeDeTropas - 1
                                                    if self.turno.tropasParaMoverAposAtaque > 2:
                                                        self.turno.tropasParaMoverAposAtaque = 2
                                            self.turno.territorioConquistado = territorioDaDefesa.codigo

                                            if self.turno.tropasParaMoverAposAtaque > 0:
                                                self.turno.tipoAcao = TipoAcaoTurno.mover_apos_conquistar_territorio
                                            break

                                    else:
                                        # Defesa venceu.
                                        self.defesaVenceu(i, territoriosDoAtaque, jogador)

                            self.enviaMsgParaTodos(TipoMensagem.atacar,
                                                   Atacar(
                                                       {
                                                           "posicao": posicaoJogador,
                                                           "usuario": self.jogadores[posicaoJogador].usuario
                                                       },
                                                       {
                                                           "posicao": jogadorDefesa.posicao,
                                                           "usuario": jogadorDefesa.usuario
                                                       },
                                                       dadosDefesa, dadosAtaque,
                                                       territorioDaDefesa, territoriosDoAtaque,
                                                       conquistouTerritorio))
                    else:
                        temErro = True

                    if temErro:
                        self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)

                    self.estaAtacando = False

    def defesaVenceu(self, i, territoriosDoAtaque, jogador):
        pos = i
        while pos >= 0:
            if pos < len(territoriosDoAtaque) and territoriosDoAtaque[pos].quantidadeDeTropas > 1:
                territoriosDoAtaque[pos] = jogador.removeTropasNoTerritorio(
                    territoriosDoAtaque[pos].codigo,
                    1)
                break
            pos -= 1

    def move(self, usuario, doTerritorio, paraOTerritorio, quantidade):
        # turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]

        if jogador.usuario == usuario:
            if self.turno.tipoAcao == TipoAcaoTurno.mover:
                if jogador.temTerritorio(doTerritorio) and jogador.temTerritorio(paraOTerritorio) and \
                        FronteiraTerritorio.TemFronteira(doTerritorio, paraOTerritorio):
                    doTerritorioObj = jogador.seuTerritorio(doTerritorio)
                    paraOTerritorioObj = jogador.seuTerritorio(paraOTerritorio)
                    if doTerritorioObj.quantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.codigo, quantidade)

                        self.enviaMsgParaTodos(TipoMensagem.mover,
                                               Mover(self.jogadores[posicaoJogador].usuario,
                                                     doTerritorioObj, paraOTerritorioObj,
                                                     quantidade))
                    else:
                        self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)
                else:
                    self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)

            elif self.turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
                if jogador.temTerritorio(doTerritorio) and \
                        jogador.temTerritorio(paraOTerritorio) and \
                        self.turno.territorioConquistado == paraOTerritorio and \
                        doTerritorio in self.turno.territoriosDoAtaqueDaConquista and \
                        self.turno.tropasParaMoverAposAtaque > 0:

                    doTerritorioObj = jogador.seuTerritorio(doTerritorio)
                    paraOTerritorioObj = jogador.seuTerritorio(paraOTerritorio)

                    if doTerritorioObj.quantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.codigo, quantidade)

                        self.turno.tropasParaMoverAposAtaque -= quantidade
                        self.enviaMsgParaTodos(TipoMensagem.mover,
                                               Mover(self.jogadores[posicaoJogador].usuario,
                                                     doTerritorioObj, paraOTerritorioObj,
                                                     quantidade))
                    else:
                        self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)
                else:
                    self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)
            self.jogadores[posicaoJogador] = jogador

    def moveAposConquistarTerritorio(self, usuario, quantidade):
        # turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]

        if jogador.usuario == usuario and self.turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            paraOTerritorio = self.turno.territorioConquistado
            for codigo in self.turno.territoriosDoAtaqueDaConquista:
                terr = jogador.seuTerritorio(codigo)
                if quantidade > 0:
                    doTerritorio = terr.codigo
                    qtdTropasQuePodemSerMovidas = terr.quantidadeDeTropas - 1
                    if quantidade > qtdTropasQuePodemSerMovidas:
                        self.move(usuario, doTerritorio, paraOTerritorio, qtdTropasQuePodemSerMovidas)
                        quantidade -= qtdTropasQuePodemSerMovidas
                    else:
                        self.move(usuario, doTerritorio, paraOTerritorio, quantidade)
                        break

            self.finalizaTurno_moverAposConquistarTerritorio()

    def trocaCartasTerritorio(self, usuario, cartasTerritorio):
        # turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]

        if self.turno.tipoAcao == TipoAcaoTurno.trocar_cartas and \
                jogador.usuario == usuario and \
                len(cartasTerritorio) == 3:

            cartasParaTroca = []
            for carta in jogador.cartasTerritorio:
                if carta.codigoTerritorio in cartasTerritorio:
                    cartasParaTroca.append(carta)
                    cartasTerritorio.remove(carta.codigoTerritorio)

            if len(cartasParaTroca) < 3:
                self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)
            else:
                # Se chegou aqui, eh porque o jogador tem as cartas dos territorios.

                # Verifica se a troca pode ser feita.
                #   - 3 formas iguais
                #   - 3 formas diferentes

                podeTrocar = False
                if cartasParaTroca[0].codigoTerritorio == CartasTerritorio.Coringa or \
                        cartasParaTroca[1].codigoTerritorio == CartasTerritorio.Coringa or \
                        cartasParaTroca[2].codigoTerritorio == CartasTerritorio.Coringa:
                    podeTrocar = True
                elif cartasParaTroca[0].forma == cartasParaTroca[1].forma == cartasParaTroca[2].forma:
                    podeTrocar = True
                elif cartasParaTroca[0].forma != cartasParaTroca[1].forma and \
                        cartasParaTroca[0].forma != cartasParaTroca[2].forma and \
                        cartasParaTroca[1].forma != cartasParaTroca[2].forma:
                    podeTrocar = True

                if podeTrocar:
                    self.turno.trocouCartas = True

                    self.quantidade_troca_por_jogador[jogador.usuario] += 1

                    self.colocaTropaNaTrocaDeCartasTerritorios(posicaoJogador, cartasParaTroca)

                    # Envia informacao do turno.
                    self.turno.quantidadeDeTropas = self.calculaQuantidadeDeTropasDaTroca(self.numeroDaTroca)
                    self.numeroDaTroca += 1
                    self.turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_troca_de_cartas
                    self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                    acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                    self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

                    # Remove e envia ao jogador suas cartas de territorios atualizadas.
                    for carta in cartasParaTroca:
                        jogador.removeCartaTerritorio(carta)
                        self.cartasTerritorioDescartadas.append(carta)
                    self.enviaMsgParaJogador(TipoMensagem.cartas_territorio, jogador.cartasTerritorio,
                                             jogador)
                else:
                    self.enviaMsgParaJogador(TipoMensagem.erro, None, jogador)

        return self.turno.trocouCartas

    def jogarDado(self):
        # TODO: VIP
        valores = [1, 2, 3, 4, 5, 6]
        random.shuffle(valores)
        return valores[random.randint(0, len(valores) - 1)]

    def calculaQuantidadeDeTropasDaTroca(self, numeroDaTroca):
        if 1 <= numeroDaTroca <= 5:
            quantidade = (numeroDaTroca * 2) + 2
        else:
            quantidade = (2 * numeroDaTroca) + (3 * (numeroDaTroca - 5))
        # TODO: Caso seja necessário limitar a quantidade de tropas.
        # return min(quantidade, 60)
        return quantidade

    def fatorTempoAdicional(self, numeroDaTroca):
        valorDaTroca = self.calculaQuantidadeDeTropasDaTroca(numeroDaTroca)
        return 1 if valorDaTroca > 35 else 0

    def pegaUmaCartaTerritorioDoBaralho(self):
        if len(self.cartasTerritorioDoBaralho) == 0:
            self.cartasTerritorioDoBaralho = list(self.cartasTerritorioDescartadas)
            random.shuffle(self.cartasTerritorioDoBaralho)
            self.cartasTerritorioDescartadas = []

        return self.cartasTerritorioDoBaralho.pop(0)

    def enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio(self):
        if self.jogadorDaVezConquistouTerritorio:
            jogador = self.jogadores[self.posicaoJogadorDaVez]
            cartaTerritorio = self.pegaUmaCartaTerritorioDoBaralho()
            jogador.adicionaCartaTerritorio(cartaTerritorio)

            self.enviaMsgParaJogador(TipoMensagem.cartas_territorio,
                                     jogador.cartasTerritorio, jogador)

            self.jogadorDaVezConquistouTerritorio = False

    def listaDeTerritoriosDosJogadores(self):
        territoriosDosJogadores = []
        for j in self.jogadores.values():
            territoriosDosJogadores.append({
                "territorios": j.territorios,
                "posicao": j.posicao
            })
        return territoriosDosJogadores

    def adiciona(self, cliente, usuario):
        listaJogadoresInfoCurta = []
        territoriosDosJogadores = []

        # Prepara as informacoes.
        for j in self.jogadores.values():
            listaJogadoresInfoCurta.append({
                "usuario": j.usuario,
                "posicao": j.posicao,
                "tipo": j.tipo,
                "total_territorios": len(j.territorios),
                "total_cartas_territorio": len(j.cartasTerritorio),
                "esta_na_sala": j.posicao in self.clientes.keys() if j.tipo == TipoJogador.humano else True
            })

            territoriosDosJogadores.append({
                "territorios": j.territorios,
                "posicao": j.posicao
            })

        olheiro = True
        posicao = -1
        for k, v in self.jogadores.items():
            if v != None and v.usuario == usuario:
                # Jogador reconectou!
                posicao = k
                olheiro = False
                self.clientes[k] = cliente

                total_territorios = 0
                total_cartas_territorio = 0
                listaJogadoresInfoCurta = []
                territoriosDosJogadores = []

                # Enviar lista dos jogadores
                for j in self.jogadores.values():
                    if j.posicao == k:
                        total_territorios = len(j.territorios)
                        total_cartas_territorio = len(j.cartasTerritorio)

                    listaJogadoresInfoCurta.append({
                        "usuario": j.usuario,
                        "posicao": j.posicao,
                        "tipo": j.tipo,
                        "total_territorios": len(j.territorios),
                        "total_cartas_territorio": len(j.cartasTerritorio),
                        "esta_na_sala": j.posicao in self.clientes.keys() if j.tipo == TipoJogador.humano else True
                    })

                    territoriosDosJogadores.append({
                        "territorios": j.territorios,
                        "posicao": j.posicao
                    })

                self.qtd_turnos_sem_jogadores_humanos = 0
                self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo,
                                       EntrouNoJogo(usuario, posicao, total_territorios, total_cartas_territorio))

                jogador = self.jogadores[posicao];
                self.enviaMsgParaJogador(TipoMensagem.carrega_jogo,
                                         CarregaJogo(self.posicaoJogadorDaVez,
                                                     territoriosDosJogadores,
                                                     listaJogadoresInfoCurta,
                                                     jogador.objetivo,
                                                     jogador.cartasTerritorio),
                                         jogador)

                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaJogador(TipoMensagem.turno, acaoDoTurno, jogador)

                break

        if olheiro:
            self.olheiros[usuario] = cliente
            self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo, EntrouNoJogo(usuario, 7, 0, 0))

            self.enviaMsgParaCliente(TipoMensagem.carrega_jogo_olheiro,
                                     CarregaJogoOlheiro(self.posicaoJogadorDaVez,
                                                        territoriosDosJogadores,
                                                        listaJogadoresInfoCurta),
                                     cliente)

            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaCliente(TipoMensagem.turno, acaoDoTurno, cliente)

    def remove(self, usuario):
        if usuario in self.olheiros.keys():
            self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, 7))
            del self.olheiros[usuario]
        else:
            for k, v in self.jogadores.items():
                if v.usuario == usuario:
                    self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, k))
                    del self.clientes[k]
                    break

    def temUmVencedor(self):
        jogador = self.jogadores[self.posicaoJogadorDaVez]
        objetivo = FabricaObjetivo().cria(jogador.objetivo)
        jogadorVenceu = objetivo.completou(jogador, self.jogadores)

        if jogadorVenceu and not self.contabilizouPontos:
            self.jogadorVencedor = jogador

            usuarios = []
            quemDestruiuQuem = {}
            for k, v in self.jogadores.items():
                usuarios.append(v.usuario)
                if len(v.jogadoresDestruidos) > 0:
                    quemDestruiuQuem[v.usuario] = []
                    for p in v.jogadoresDestruidos:
                        quemDestruiuQuem[v.usuario].append(self.jogadores[p].usuario)

            pontuacao = Pontuacao(self, self.jogadorVencedor.usuario, usuarios, quemDestruiuQuem, self.cpus)
            self.pontuacaoPelaVitoria = pontuacao.contabilizaPontuacaoDoVencedor()
            self.pontuacao_jogadores = pontuacao.contabilizaPontuacaoDosQueNaoVenceram()
            self.pontuacao_jogadores[self.jogadorVencedor.usuario] = self.pontuacaoPelaVitoria

            self.contabilizouPontos = True

        return jogadorVenceu

    def quemDestruiuQuem(self, jogadores):
        quemDestruiuQuem = {}
        for k, v in jogadores.items():
            if len(v.jogadoresDestruidos) > 0:
                quemDestruiuQuem[v.usuario] = []
                for p in v.jogadoresDestruidos:
                    quemDestruiuQuem[v.usuario].append(jogadores[p].usuario)
        return quemDestruiuQuem

    def usuarioFoiDestruidoPorAlguem(self, usuario, quemDestruiuQuem):
        for k, v in quemDestruiuQuem.items():
            if usuario in v:
                return True
        return False

    def usuarioDestruiOutroUsuario(self, usuario_destruiu, usuario_destruido, quemDestruiuQuem):
        for k, usuarios in quemDestruiuQuem.items():
            if k == usuario_destruiu:
                return usuario_destruido in usuarios
        return False

    def jogoTerminou(self):
        logging.info("{} Jogo terminou.".format(self.TAG))

        desafios = Desafios()
        for k, jogador in self.jogadores.items():
            desafios_em_andamento = desafios.em_andamento(jogador.usuario)
            if jogador.posicao in self.clientes.keys() and len(desafios_em_andamento) > 0:
                self.enviaMsgParaCliente(TipoMensagem.desafios_em_andamento, desafios_em_andamento,
                                         self.clientes[jogador.posicao])

        self.gerenciador.jogoTerminou(self.nome)

    def temJogadorOnLine(self):
        return len(self.clientes) > 0

    def grafoTerritorios(self, jogadores):
        grafo_territorios = {}
        for codigo_territorio in CodigoTerritorio.Lista:
            grafo_territorios[codigo_territorio] = {
                'codigo': codigo_territorio,
                'fronteiras': FronteiraTerritorio.Fronteiras[codigo_territorio]
            }
            if codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.Asia]:
                grafo_territorios[codigo_territorio]['borda'] = True
            elif codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.AmericaDoNorte]:
                grafo_territorios[codigo_territorio]['borda'] = True
            elif codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.Africa]:
                grafo_territorios[codigo_territorio]['borda'] = True
            elif codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.AmericaDoSul]:
                grafo_territorios[codigo_territorio]['borda'] = True
            elif codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.Europa]:
                grafo_territorios[codigo_territorio]['borda'] = True
            elif codigo_territorio in GrupoTerritorio.FronteirasContinentes[GrupoTerritorio.Oceania]:
                grafo_territorios[codigo_territorio]['borda'] = True
            else:
                grafo_territorios[codigo_territorio]['borda'] = False

            if codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.Asia]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.Asia
            elif codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.AmericaDoNorte]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.AmericaDoNorte
            elif codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.Africa]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.Africa
            elif codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.AmericaDoSul]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.AmericaDoSul
            elif codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.Europa]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.Europa
            elif codigo_territorio in GrupoTerritorio.Dicionario[GrupoTerritorio.Oceania]:
                grafo_territorios[codigo_territorio]['grupo'] = GrupoTerritorio.Oceania

        for jogador in jogadores.values():
            for territorio in jogador.territorios:
                grafo_territorios[territorio.codigo]['usuario'] = jogador.usuario
                grafo_territorios[territorio.codigo]['tipo'] = jogador.tipo
                grafo_territorios[territorio.codigo]['quantidade'] = territorio.quantidadeDeTropas

        return grafo_territorios

    def territoriosInimigos(self, usuario):
        territorios = []
        for j in self.jogadores.values():
            if j.usuario != usuario:
                territorios = territorios + j.territorios
        return territorios

    def msgChat(self, usuario, texto):
        posicao = self.posicaoDoUsuario(usuario)
        texto, comando = self.chat.interpreta_comandos(texto)

        if comando and comando == Chat.KICK_COMMAND:
            arg = texto
            if GrupoUsuariosDB().verifica_usuario_adm(usuario):
                if arg in self.olheiros:
                    self.gerenciador.sai(self.olheiros[arg])
                    texto = '[ADM] O jogador ' + arg + ' foi retirado da sala.'
                else:
                    posicao_usuario_kickado = self.posicaoDoUsuario(arg)
                    if posicao_usuario_kickado != -1:
                        cliente = self.clientes[posicao_usuario_kickado]
                        self.gerenciador.sai(cliente)
                        texto = '[ADM] O jogador ' + arg + ' foi retirado da sala.'

        self.enviaMsgParaTodos(TipoMensagem.msg_chat_jogo,
                               MsgChatJogo({"usuario": usuario, "posicao": posicao}, texto))

    def montaMsg(self, tipoMensagem, params):
        return Mensagem(tipoMensagem, params).toJson()

    def enviaMsgParaCliente(self, tipoMensagem, params, cliente):
        try:
            jsonMsg = self.montaMsg(tipoMensagem, params)
            # TODO: Log do jogo
            # print('LOG JOGO enviaMsgParaCliente', jsonMsg)
            cliente.sendMessage(jsonMsg)
        except Exception:
            logging.error("{} Nao foi possivel enviar a mensagem para o cliente - JSON: {}".format(self.TAG, jsonMsg))

    def enviaMsgParaCPU(self, tipoMensagem, params, cpu):
        try:
            jsonMsg = self.montaMsg(tipoMensagem, params)
            # TODO: Log do jogo
            # print('LOG JOGO enviaMsgParaCPU', jsonMsg)
            cpu.processa_msg(self, jsonMsg)
        except Exception:
            logging.error("{} Nao foi possivel enviar a mensagem para o cliente - JSON: {}".format(self.TAG, jsonMsg))

    def enviaMsgParaJogador(self, tipoMensagem, params, jogador):
        posicao = jogador.posicao
        if self.jogadores[posicao].tipo == TipoJogador.humano:
            self.enviaMsgParaCliente(tipoMensagem, params, self.clientes[posicao])
        elif self.jogadores[posicao].tipo == TipoJogador.cpu:
            self.enviaMsgParaCPU(tipoMensagem, params, self.cpus[jogador.usuario])

    def enviaMsgParaOlheiros(self, tipoMensagem, params):
        try:
            jsonMsg = self.montaMsg(tipoMensagem, params)
            for socket in self.olheiros.values():
                socket.sendMessage(jsonMsg)
        except Exception:
            logging.error(
                "{} Nao foi possivel enviar a mensagem para todos os olheiros - JSON: {}".format(self.TAG, jsonMsg))

    def enviaMsgParaTodos(self, tipoMensagem, params):
        try:
            jsonMsg = self.montaMsg(tipoMensagem, params)
            # TODO: Log do jogo
            # print('LOG JOGO enviaMsgParaTodos', jsonMsg)
            for socket in self.clientes.values():
                socket.sendMessage(jsonMsg)
            for socket in self.olheiros.values():
                socket.sendMessage(jsonMsg)
            for jogadorCpu in self.cpus.values():
                jogadorCpu.processa_msg(self, jsonMsg)
        except Exception:
            logging.error(
                "{} Nao foi possivel enviar a mensagem para todos os clientes - JSON: {}".format(self.TAG, jsonMsg))

    def fecha(self):
        self.terminou_em = int(time.time() * 1000)
        info_jogo = InfoJogo(self)
        logging.info("{} {}".format(self.TAG, info_jogo.toJson()))
        HistoricoJogo().new(info_jogo)

        self.enviaMsgParaTodos(TipoMensagem.jogo_interrompido, JogoInterrompido(self.nome))
        self.turno.paraTimeout()
        for jogadorCpu in self.cpus.values():
            jogadorCpu.para()


class InfoJogo(JSONSerializer):
    def __init__(self, jogo):
        self.tag = jogo.TAG
        self.nome = jogo.nome
        self.iniciou_em = jogo.iniciou_em
        self.terminou_em = jogo.terminou_em
        self.jogadores = jogo.jogadores
        self.quem_destruiu_quem = jogo.quemDestruiuQuem(jogo.jogadores)
        self.vencedor = jogo.jogadorVencedor
        self.ordem = jogo.ordemJogadores
        self.pontuacao = jogo.pontuacao_jogadores
        self.turno = jogo.turno.numero
