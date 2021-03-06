#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import random
import traceback

from src.badges import *
from src.chat.chat import *
from src.desafios.desafios import *
from src.doacaodb import *
from src.grupousuariosdb import *
from src.ia.iaathena import *
from src.ia.iafactory import *
from src.ia.ialucy import *
from src.jogador import *
from src.jogo import *
from src.mensagens import *
from src.pontuacaodb import *
from src.sala import *


class GerenciadorSala(object):
    def __init__(self, nome, gerenciadorPrincipal):
        self.nome = nome
        self.gerenciadorPrincipal = gerenciadorPrincipal
        self.sala = Sala(nome)
        self.jogo = None
        self.jogadores = {}
        self.estado = EstadoDaSala.sala_criada
        self.jogadoresDaSala = []
        self.chat = Chat()

    def info_sala_msg(self):
        return InfoSala(self.sala.id, self.estado, self.sala.jogadores.values(), None)

    def entra(self, cliente, usuario):
        self.jogadores[cliente] = usuario

        if self.jogo == None:
            if self.sala != None:
                infoSalaMsg = self.sala.adiciona(usuario)
                self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
                self.jogadoresDaSala = self.sala.jogadores.values()
        else:
            self.jogo.adiciona(cliente, usuario)

    def entra_posicao(self, cliente, usuario, posicao):
        self.jogadores[cliente] = usuario

        if self.jogo == None:
            if self.sala != None:
                infoSalaMsg = self.sala.adiciona(usuario)
                self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
                self.jogadoresDaSala = self.sala.jogadores.values()
                # TODO: VIP
                alteraPosicaoNaSalaMsg = self.sala.alteraPosicao(usuario, posicao)
                self.enviaMsgParaTodos(TipoMensagem.altera_posicao_na_sala, alteraPosicaoNaSalaMsg)
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

                if not self.jogo.temJogadorOnLine() and len(self.jogo.cpus) == 0:
                    self.jogoTerminou(self.nome)
                    self.gerenciadorPrincipal.enviaMsgLobbyParaTodos()
                else:
                    self.gerenciadorPrincipal.enviaMsgLobbyParaCliente(cliente)

            del self.jogadores[cliente]
        except:
            traceback.print_exc()
            print("[ERROR]", "Nao foi possivel desconectar o cliente ", cliente)

    def iniciaPartida(self):
        quantidade_jogadores_na_sala = 0
        for k, v in self.sala.jogadores.items():
            jogadorDaSala = self.sala.jogadores[k]
            if jogadorDaSala.tipo != TipoJogador.desabilitado:
                quantidade_jogadores_na_sala = quantidade_jogadores_na_sala + 1
        if quantidade_jogadores_na_sala >= 3 and self.jogo == None:
            self.jogadoresDaSala = self.sala.jogadores
            tempJogadoresDaSala = self.sala.jogadores

            jogadoresDoJogo = {}
            clientes = {}
            cpus = {}

            cpu_factory = IAFactory()
            sufixos = []
            for i in range(10, 99):
                sufixos.append(str(i))
            random.shuffle(sufixos)

            for k, v in tempJogadoresDaSala.items():
                jogadorDaSala = tempJogadoresDaSala[k]
                if jogadorDaSala.tipo != TipoJogador.desabilitado:
                    cpu = None
                    usuario = jogadorDaSala.usuario
                    posicao = jogadorDaSala.posicao
                    if jogadorDaSala.tipo == TipoJogador.cpu:
                        if len(cpus) == 0:
                            cpu = IAAthena()
                        else:
                            cpu = IALucy(sufixo=sufixos[posicao])
                        # cpu = cpu_factory.dummy()(sufixo=sufixos[posicao])
                        usuario = cpu.usuario
                    jogadoresDoJogo[k] = JogadorDoJogo(
                        usuario,
                        posicao,
                        jogadorDaSala.dono,
                        jogadorDaSala.tipo)
                    if jogadorDaSala.tipo == TipoJogador.humano:
                        clientes[jogadorDaSala.posicao] = self.socketDoUsuario(jogadorDaSala.usuario)
                    elif cpu and jogadorDaSala.tipo == TipoJogador.cpu:
                        cpu.jogador_ref(jogadoresDoJogo[k])
                        cpus[usuario] = cpu
                        cpu.start()
            self.jogo = Jogo(self.nome, jogadoresDoJogo, cpus, clientes, self)

            self.jogo.prepara_para_comecar()

            self.estado = EstadoDaSala.jogo_em_andamento
            infoSalaMsg = InfoSala(self.sala.id,
                                   self.estado, self.sala.jogadores.values(), None)
            self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)

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
                novaPosicao = mensagem.params['novaPosicao']
                self.entra_posicao(cliente, usuario, novaPosicao)

        elif mensagem.tipo == TipoMensagem.altera_tipo_posicao_na_sala:
            if self.estaDentro(usuario):
                posicao = mensagem.params['posicao']
                infoSalaMsg = self.sala.alteraTipoPosicao(usuario, posicao)
                if infoSalaMsg:
                    self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)

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
        logging.info("GERENCIADOR Jogo {} terminou.".format(idJogo))

        self.fecha()

        self.gerenciadorPrincipal.jogoTerminou(idJogo)
        self.jogadoresDaSala = []

        self.gerenciadorPrincipal.enviaMsgLobbyParaTodos()

    def fecha(self):
        if self.jogo is not None:
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
        for k, v in self.jogadores.items():
            if v == usuario:
                return k
        return None

    def jogadores_da_sala(self):
        if self.sala:
            self.jogadoresDaSala = self.sala.jogadores
        return self.jogadoresDaSala

    def enviaMsgParaTodos(self, tipo, params):
        self.gerenciadorPrincipal.enviaMsgParaTodos(tipo, params)


class GerenciadorPrincipal(object):
    def __init__(self):
        self.jogadores = {}
        self.salas = {}
        self.usuarioPorSala = {}
        self.chat = Chat()

    def clienteConectou(self, cliente, usuario):
        self.jogadores[cliente] = usuario

        if usuario in self.usuarioPorSala.keys():
            gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
            gerenciadorSala.entra(cliente, usuario)
        else:
            self.enviaMsgLobbyParaCliente(cliente)

        # TODO: Implementar mecanismo de cache.
        infoUsuario = {"nome": usuario}
        ranking = self.ranking()
        for r in ranking['ranking']:
            if r.nome == usuario:
                infoUsuario = r
                break

        if infoUsuario:
            self.enviaMsgParaTodos(TipoMensagem.usuario_conectou, UsuarioConectou(infoUsuario))
            self.enviaMsgParaTodos(TipoMensagem.ranking, ranking)

        # TODO:  Rever a forma de mandar essas mensagens com mais frequência.
        doacoes = DoacaoDB().doadores()
        self.enviaMsgParaCliente(TipoMensagem.doacoes, doacoes, cliente)

        desafios_em_andamento = Desafios().em_andamento(usuario)
        self.enviaMsgParaCliente(TipoMensagem.desafios_em_andamento, desafios_em_andamento, cliente)

    def clienteDesconectou(self, cliente):
        usuario = self.jogadores[cliente]
        try:
            if usuario in self.usuarioPorSala and self.usuarioPorSala[usuario] in self.salas:
                gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
                gerenciadorSala.sai(cliente)
                del self.usuarioPorSala[usuario]
        except:
            print("[ERRO][GerenciadorPrincipal] Erro ao tentar desconectar o usuario[" + usuario + "] da sala.")
            print("\tProvavelmente ele nao esteja em nenhuma.")

        if cliente in self.jogadores:
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
        elif mensagem.tipo == TipoMensagem.altera_tipo_posicao_na_sala:
            # Usuario esta em uma sala.
            if usuario in self.usuarioPorSala.keys():
                idSala = mensagem.params['sala']
                gerenciadorSala = self.salas[idSala]
                gerenciadorSala.requisicao(cliente, usuario, mensagem)
        elif mensagem.tipo == TipoMensagem.sair_da_sala:
            if usuario in self.usuarioPorSala.keys():
                gerenciadorSala = self.salas[self.usuarioPorSala[usuario]]
                gerenciadorSala.sai(cliente)

                # TODO: Verificar qual o motivo deste codigo estar aqui, pois ele sempre da excecao.
                try:
                    self.usuarioPorSala.pop(usuario)
                except:
                    print("[DEBUG] Erro ao tentar retirar o jogador [" + usuario + "] da relacao usuario por sala.")
            else:
                self.enviaMsgLobbyParaCliente(cliente)

        elif mensagem.tipo == TipoMensagem.msg_chat_geral:
            texto = mensagem.params['texto']
            texto, comando = self.chat.interpreta_comandos(texto)

            if comando == Chat.KILL_COMMAND:
                id_sala = texto
                if id_sala in self.salas:
                    if GrupoUsuariosDB().verifica_usuario_adm(usuario):
                        self.mata_jogo(id_sala)
                        self.enviaMsgLobbyParaTodos()
                        texto = '[ADM] A sala ' + id_sala + ' foi encerrada.'
                        self.enviaMsgParaTodos(TipoMensagem.msg_chat_geral, MsgChatGeral(usuario, texto))
            else:
                self.enviaMsgParaTodos(TipoMensagem.msg_chat_geral, MsgChatGeral(usuario, texto))

        elif mensagem.tipo == TipoMensagem.desafios_em_andamento:
            desafios_em_andamento = Desafios().em_andamento(usuario)
            self.enviaMsgParaCliente(TipoMensagem.desafios_em_andamento, desafios_em_andamento, cliente)

    def criaSala(self, cliente, usuario, mensagem):
        # TODO: VIP
        # idSala = mensagem.params['sala']
        idSala = 1
        while str(idSala) in self.salas.keys():
            idSala = idSala + 1
        idSala = str(idSala)
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

    def ranking(self):
        badges_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'badges.csv')
        pontuacao_db = PontuacaoDB()
        ranking = {
            'ranking': pontuacao_db.ranking_geral(),
            'ranking_evento': pontuacao_db.ranking_evento(),
            'badges': Badges().ler_csv(badges_path),
            'doacoes': {'meta': DoacaoDB().meta_doacoes_progresso()}
        }
        return ranking

    def fechaSala(self, idSala):
        idSala = str(idSala)
        print("[DEBUG] fechaSala(", idSala, ")")
        try:
            if idSala in self.salas:
                self.salas[idSala].fecha()
                del self.salas[idSala]
                self.enviaMsgParaTodos(TipoMensagem.fechar_sala,
                                       FecharSala(idSala))
                logging.info("Sala {} fechada.".format(idSala))
            else:
                logging.info("Sala {}  já foi fechada anteriormente.".format(idSala))
        except:
            traceback.print_exc()
            logging.error("Erro ao fechar a sala {}".format(idSala))

    def jogoTerminou(self, idJogo):
        removerUsuarios = []
        for usuario in self.usuarioPorSala.keys():
            if self.usuarioPorSala[usuario] == idJogo:
                removerUsuarios.append(usuario)
        for u in removerUsuarios:
            self.usuarioPorSala.pop(u)
        del removerUsuarios

        self.fechaSala(idJogo)

        self.enviaMsgParaTodos(TipoMensagem.ranking, self.ranking())

    def mata_jogo(self, id_jogo):
        self.jogoTerminou(id_jogo)

    def montaMensagemParamsLobby(self):
        # Envia a lista de salas para o cliente.
        infoSalas = []
        for gerenciadorSala in self.salas.values():
            info = {
                "sala": gerenciadorSala.nome,
                "jogadores": gerenciadorSala.jogadores_da_sala(),
                "estado": gerenciadorSala.estado
            }
            infoSalas.append(info)

        # TODO: Implementar mecanismo de cache.
        infoUsuarios = []
        ranking = self.ranking()
        for r in ranking['ranking']:
            if r.nome in self.jogadores.values():
                infoUsuarios.append(r)
        return Lobby(infoSalas, infoUsuarios)

    def enviaMsgLobbyParaTodos(self):
        lobby = self.montaMensagemParamsLobby()
        self.enviaMsgParaTodos(TipoMensagem.lobby, lobby)

    def enviaMsgLobbyParaCliente(self, cliente):
        lobby = self.montaMensagemParamsLobby()
        self.enviaMsgParaCliente(TipoMensagem.lobby, lobby, cliente)

    def enviaMsgParaCliente(self, tipoMensagem, params, cliente):
        jsonMsg = Mensagem(tipoMensagem, params).toJson()
        # print("[INFO][GerenciadorPrincipal] Enviando: " + jsonMsg)
        cliente.sendMessage(jsonMsg)

    def enviaMsgParaTodos(self, tipoMensagem, params):
        jsonMsg = Mensagem(tipoMensagem, params).toJson()
        for socket in self.jogadores.keys():
            socket.sendMessage(jsonMsg)
        # print("[INFO][GerenciadorPrincipal] Broadcast: ", jsonMsg)

    def fecha(self):
        for gerenciadorSala in self.salas.values():
            gerenciadorSala.fecha()
