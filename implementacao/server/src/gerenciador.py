#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import traceback

from jogador import *
from jogo import *
from mensagens import *
from pontuacaodb import *
from sala import *


class GerenciadorSala(object):
    def __init__(self, nome, gerenciadorPrincipal):
        self.nome = nome
        self.gerenciadorPrincipal = gerenciadorPrincipal
        self.sala = Sala(nome)
        self.jogo = None
        self.jogadores = {}
        self.estado = EstadoDaSala.sala_criada
        self.jogadoresDaSala = []

    def entra(self, cliente, usuario):
        self.jogadores[cliente] = usuario

        if self.jogo == None:
            if self.sala != None:
                infoSalaMsg = self.sala.adiciona(usuario)
                self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
                self.jogadoresDaSala = self.sala.jogadores.values()
        else:
            self.jogo.adiciona(cliente, usuario)

    def sai(self, cliente):
        try:
            usuario = self.jogadores[cliente]
            if self.jogo == None:
                if self.sala != None:
                    infoSalaMsg = self.sala.remove(usuario)
                    self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
                    self.jogadoresDaSala = self.sala.jogadores.values()

                    if self.sala.vazia():
                        self.gerenciadorPrincipal.fechaSala(self.nome)
                else:
                    self.gerenciadorPrincipal.enviaMsgLobbyParaCliente(cliente)
            else:
                self.jogo.remove(usuario)

                if not self.jogo.temJogadorOnLine():
                    self.jogoTerminou(self.nome)

                self.gerenciadorPrincipal.enviaMsgLobbyParaCliente(cliente)

            del self.jogadores[cliente]
        except:
            traceback.print_exc()
            print
            "[ERROR]", "Nao foi possivel desconectar o cliente ", cliente

    def iniciaPartida(self):
        if len(self.sala.jogadores) >= 3 and self.jogo == None:
            tempJogadoresDaSala = self.sala.jogadores

            jogadoresDoJogo = {}
            clientes = {}
            for k, v in tempJogadoresDaSala.iteritems():
                jogadorDaSala = tempJogadoresDaSala[k]
                jogadoresDoJogo[k] = JogadorDoJogo(
                    jogadorDaSala.usuario,
                    jogadorDaSala.posicao,
                    jogadorDaSala.dono)
                clientes[jogadorDaSala.posicao] = self.socketDoUsuario(jogadorDaSala.usuario)
            self.jogo = Jogo(self.nome, jogadoresDoJogo, clientes, self)

            # Distribui os territorios e define quem comeca.
            jogoFaseIMsg = self.jogo.faseI_Inicia()
            self.jogo.enviaMsgParaTodos(TipoMensagem.jogo_fase_I, jogoFaseIMsg)

            # Envia a carta objetivo para cada jogador individualmente.
            cartasObjetivos = self.jogo.faseI_DefinirObjetivos()
            for i in range(len(jogadoresDoJogo)):
                jsonMsg = json.dumps(Mensagem(
                    TipoMensagem.carta_objetivo,
                    CartaObjetivo(cartasObjetivos[i])), default=lambda o: o.__dict__)
                print
                "# ", jsonMsg
                posicaoJogador = self.jogo.ordemJogadores[i]
                clientes[posicaoJogador].sendMessage(jsonMsg)

            self.estado = EstadoDaSala.jogo_em_andamento

            infoSalaMsg = InfoSala(self.sala.id,
                                   self.estado, self.sala.jogadores.values(), None)
            self.jogo.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)

            self.jogo.iniciaTurnos()

            del self.sala
            self.sala = None

    def finalizaTurno(self, cliente):
        if self.jogo != None:
            usuario = self.jogadores[cliente]
            self.jogo.finalizaTurno(usuario)

    def requisicao(self, cliente, usuario, mensagem):
        if mensagem.tipo == TipoMensagem.altera_posicao_na_sala:
            if self.estaDentro(usuario):
                novaPosicao = mensagem.params['novaPosicao']
                alteraPosicaoNaSalaMsg = self.sala.alteraPosicao(usuario, novaPosicao)
                self.enviaMsgParaTodos(TipoMensagem.altera_posicao_na_sala, alteraPosicaoNaSalaMsg)
            else:
                self.entra(cliente, usuario)

        elif self.jogo != None:
            if mensagem.tipo == TipoMensagem.colocar_tropa:
                territorio = mensagem.params['territorio']
                quantidade = mensagem.params['quantidade']
                self.jogo.colocaTropaReq(usuario, territorio, quantidade)
            elif mensagem.tipo == TipoMensagem.atacar:
                dosTerritorios = mensagem.params['dosTerritorios']
                paraOTerritorio = mensagem.params['paraOTerritorio']
                self.jogo.ataca(usuario, dosTerritorios, paraOTerritorio)
            elif mensagem.tipo == TipoMensagem.mover:
                doTerritorio = mensagem.params['doTerritorio']
                paraOTerritorio = mensagem.params['paraOTerritorio']
                quantidade = mensagem.params['quantidade']
                self.jogo.move(usuario, doTerritorio, paraOTerritorio, quantidade)
            elif mensagem.tipo == TipoMensagem.moverAposConquistarTerritorio:
                quantidade = mensagem.params['quantidade']
                self.jogo.moveAposConquistarTerritorio(usuario, quantidade)
            elif mensagem.tipo == TipoMensagem.trocar_cartas_territorio:
                cartasTerritorio = mensagem.params['cartasTerritorios']
                self.jogo.trocaCartasTerritorio(usuario, cartasTerritorio)
            elif mensagem.tipo == TipoMensagem.msg_chat_jogo:
                texto = mensagem.params['texto']
                self.jogo.msgChat(usuario, texto)

    def jogoTerminou(self, idJogo):
        idJogo = str(idJogo)

        self.fecha()

        self.gerenciadorPrincipal.jogoTerminou(idJogo)
        self.jogadoresDaSala = []

        # TODO: Verificar criacao de salas pre-criadas.
        # if idJogo == "1" or idJogo == "2":
        print
        "Recriando sala ", idJogo
        self.sala = Sala(idJogo)
        self.estado = EstadoDaSala.sala_criada

        infoSalaMsg = InfoSala(self.sala.id,
                               self.estado, self.sala.jogadores.values(), None)
        self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)

    def fecha(self):
        if self.jogo != None:
            self.jogo.fecha()
            del self.jogo
            self.jogo = None

    def estaDentro(self, usuario):
        if self.sala != None:
            for jog in self.sala.jogadores.values():
                if jog.usuario == usuario:
                    return True
        return False

    def socketDoUsuario(self, usuario):
        for k, v in self.jogadores.iteritems():
            if v == usuario:
                return k
        return None

    def enviaMsgParaTodos(self, tipo, params):
        self.gerenciadorPrincipal.enviaMsgParaTodos(tipo, params)


class GerenciadorPrincipal(object):
    def __init__(self):
        self.jogadores = {}
        self.salas = {}
        self.usuarioPorSala = {}

        # TODO: Verificar criacao de salas pre-criadas.
        # self.salas["1"] = GerenciadorSala("1", self)
        # self.salas["2"] = GerenciadorSala("2", self)

    def clienteConectou(self, cliente, usuario):
        self.jogadores[cliente] = usuario

        if usuario in self.usuarioPorSala.keys():
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.entra(cliente, usuario)
        else:
            self.enviaMsgLobbyParaCliente(cliente)

        # TODO: Implementar mecanismo de cache.
        infoUsuario = {"nome": usuario}
        ranking = PontuacaoDB().ranking()
        for r in ranking:
            if r.nome == usuario:
                infoUsuario = r
                break

        if infoUsuario:
            self.enviaMsgParaTodos(TipoMensagem.usuario_conectou, UsuarioConectou(infoUsuario))

    def clienteDesconectou(self, cliente):
        usuario = self.jogadores[cliente]
        try:
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.sai(cliente)
            del self.usuarioPorSala[usuario]
        except:
            print
            "[ERRO][GerenciadorPrincipal] Erro ao tentar desconectar o usuario[" + usuario + "] da sala."
            print
            "\tProvavelmente ele nao esteja em nenhuma."
        del self.jogadores[cliente]

        self.enviaMsgParaTodos(TipoMensagem.usuario_desconectou, UsuarioDesconectou(usuario))

    def interpretaMensagem(self, cliente, mensagem):
        usuario = self.jogadores[cliente]

        if mensagem.tipo == TipoMensagem.criar_sala:
            self.criaSala(cliente, usuario, mensagem)
        elif mensagem.tipo == TipoMensagem.iniciar_partida:
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.iniciaPartida()
        elif mensagem.tipo == TipoMensagem.finalizar_turno:
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.finalizaTurno(cliente)
        elif (mensagem.tipo == TipoMensagem.colocar_tropa or
              mensagem.tipo == TipoMensagem.atacar or
              mensagem.tipo == TipoMensagem.mover or
              mensagem.tipo == TipoMensagem.moverAposConquistarTerritorio or
              mensagem.tipo == TipoMensagem.trocar_cartas_territorio or
              mensagem.tipo == TipoMensagem.msg_chat_jogo):
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.requisicao(cliente, usuario, mensagem)
        elif mensagem.tipo == TipoMensagem.altera_posicao_na_sala:
            idSala = mensagem.params['sala']
            gerenciadorSala = self.salas[idSala]

            # Usuario esta em uma sala.
            if usuario in self.usuarioPorSala.keys():
                idSalaAtual = self.usuarioPorSala[usuario]
                if idSalaAtual != idSala:
                    gerenciadorSalaAtual = self.salas[idSalaAtual]
                    gerenciadorSalaAtual.sai(cliente)

            gerenciadorSala.requisicao(cliente, usuario, mensagem)
            self.usuarioPorSala[usuario] = idSala
        elif mensagem.tipo == TipoMensagem.sair_da_sala:
            if usuario in self.usuarioPorSala.keys():
                gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
                gerenciadorSala.sai(cliente)

                try:
                    self.usuarioPorSala.pop(usuario)
                except:
                    print
                    "[DEBUG] Erro ao tentar retirar o jogador [" + usuario + "] da relacao usuario por sala."
            else:
                self.enviaMsgLobbyParaCliente(cliente)

        elif mensagem.tipo == TipoMensagem.msg_chat_geral:
            texto = mensagem.params['texto']
            self.enviaMsgParaTodos(TipoMensagem.msg_chat_geral, MsgChatGeral(usuario, texto))

    def criaSala(self, cliente, usuario, mensagem):
        idSala = mensagem.params['sala']

        # TODO: Validar nome.
        if idSala not in self.salas.keys() and len(idSala) > 0:
            # Usuario esta em uma sala.
            if usuario in self.usuarioPorSala.keys():
                idSalaAtual = self.usuarioPorSala[usuario]
                if idSalaAtual != idSala:
                    gerenciadorSalaAtual = self.salas[idSalaAtual]
                    gerenciadorSalaAtual.sai(cliente)

            self.enviaMsgParaTodos(TipoMensagem.criar_sala,
                                   CriarSala(idSala))

            gerenciadorSala = GerenciadorSala(idSala, self)
            gerenciadorSala.entra(cliente, usuario)
            self.salas[idSala] = gerenciadorSala
            self.usuarioPorSala[usuario] = idSala

    def fechaSala(self, idSala):
        idSala = str(idSala)
        print
        "[DEBUG] fechaSala(", idSala, ")"
        try:
            # TODO: Verificar criacao de salas pre-criadas.
            # if idSala != "1" and idSala != "2":
            del self.salas[idSala]
            self.enviaMsgParaTodos(TipoMensagem.fechar_sala,
                                   FecharSala(idSala))
            print
            "[DEBUG] Sala ", idSala, " fechada."
        except:
            traceback.print_exc()
            print
            "[ERRO] Tentou fechar sala de id:", idSala

    def jogoTerminou(self, idJogo):
        removerUsuarios = []
        for usuario in self.usuarioPorSala.keys():
            if self.usuarioPorSala[usuario] == idJogo:
                removerUsuarios.append(usuario)
        for u in removerUsuarios:
            self.usuarioPorSala.pop(u)
        del removerUsuarios

        self.fechaSala(idJogo)

    def enviaMsgLobbyParaCliente(self, cliente):
        # Envia a lista de salas para o cliente.
        infoSalas = []
        for gerenciadorSala in self.salas.values():
            info = {
                "sala": gerenciadorSala.nome,
                "jogadores": gerenciadorSala.jogadoresDaSala,
                "estado": gerenciadorSala.estado
            }
            infoSalas.append(info)

        # TODO: Implementar mecanismo de cache.
        infoUsuarios = []
        ranking = PontuacaoDB().ranking()
        for r in ranking:
            if r.nome in self.jogadores.values():
                infoUsuarios.append(r)
        self.enviaMsgParaCliente(TipoMensagem.lobby,
                                 Lobby(infoSalas, infoUsuarios), cliente)

    def enviaMsgParaCliente(self, tipoMensagem, params, cliente):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        print
        "[INFO][GerenciadorPrincipal] Enviando: " + jsonMsg
        cliente.sendMessage(jsonMsg)

    def enviaMsgParaTodos(self, tipoMensagem, params):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        for socket in self.jogadores.keys():
            socket.sendMessage(jsonMsg)
        print
        "[INFO][GerenciadorPrincipal] Broadcast: ", jsonMsg

    def fecha(self):
        for gerenciadorSala in self.salas.values():
            gerenciadorSala.fecha()
