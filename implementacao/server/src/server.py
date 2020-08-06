#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import re
import signal
import sys
import traceback

import banco
import gerenciador
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
from badges import *
from email_util import *
from mensagens import *
from pontuacaodb import *
from src.desafios.desafios import *
from src.doacaodb import *
from src.historicojogo import *
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onMessage(self, msg, binary):
        if not binary:
            # print("[%s] Enviou: %s" % (self.peer, msg))

            # Retirando qualquer tipo de tag html da mensagem.
            msg = re.sub('<[^<]+?>', '', msg.decode('utf-8'))

            mensagem = Mensagem()
            mensagem.fromJson(msg)

            if mensagem.tipo == TipoMensagem.entrar:
                params = {}

                usuario = mensagem.params['usuario']
                usuario = _banco.verificaCredenciaisDoUsuario(usuario, mensagem.params['senha'])
                params["usuario"] = usuario
                if usuario and len(usuario) > 0:
                    if self.factory.usuarioEstaConectado(usuario):
                        params['status'] = 2
                        # TODO: Enviar mensagem para o outro socket do usuario uma 
                        # mensagem com o motivo da sua desconexao.
                        # jsonMsg = Mensagem(TipoMensagem.entrar, params).toJson()
                        # print("# ", jsonMsg)
                        # self.sendMessage(jsonMsg)

                        # TODO: Se for o mesmo socket, nao eh necessario desconectar o jogagdor.
                        self.factory.desconectaUsuario(usuario)

                    params["status"] = 1
                    self.factory.clienteConectou(self, usuario)
                    logging.info('%s %s', usuario, self.peer)

                    jsonMsg = Mensagem(TipoMensagem.entrar, params).toJson()
                    self.sendMessage(jsonMsg)

                    _gerenciadorPrincipal.clienteConectou(self, usuario)
                else:
                    params["status"] = 0
                    jsonMsg = Mensagem(TipoMensagem.entrar, params).toJson()
                    self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.registrar:
                params = {}
                usuario = mensagem.params['usuario']
                senha = mensagem.params['senha']
                email = mensagem.params['email']
                if len(usuario) > 0 and len(senha) > 0 and len(email) > 0 and Email().is_valid(email):
                    if _banco.usuarioExiste(usuario, email):
                        params["status"] = 0
                    else:
                        _banco.registraUsuario(usuario, senha, email)
                        params["status"] = 1
                else:
                    params["status"] = 2

                jsonMsg = Mensagem(TipoMensagem.registrar, params).toJson()
                self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.recuperar_senha:
                email = mensagem.params['email']
                params = {
                    "email": email
                }
                email_inst = Email()
                if email_inst.is_valid(email):
                    params["status"] = 1
                    if _banco.emailExiste(email):
                        codigo_recuperacao = _banco.geraCodigoRecuperacao(email)
                        if codigo_recuperacao:
                            email_conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email.conf')
                            with open(email_conf_path, 'r') as conf_json:
                                conf = json.load(conf_json)
                                try:
                                    email_inst.send_mail(conf['email'], conf['password'], [email], 'Password recovery',
                                                         'Your recovery code is: <b>' + codigo_recuperacao + '</b>',
                                                         files=None, server=conf['server'], port=conf['port'])
                                    params["status"] = 0
                                except:
                                    pass
                else:
                    params["status"] = 2

                jsonMsg = Mensagem(TipoMensagem.recuperar_senha, params).toJson()
                print("Recuperar senha # ", jsonMsg, email, codigo_recuperacao)
                self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.nova_senha:
                params = {}
                codigo = mensagem.params['codigo']
                email = mensagem.params['email']
                senha = mensagem.params['senha']
                if len(senha) > 0 and len(email) > 0 and Email().is_valid(email) and _banco.atualizaSenha(codigo, email,
                                                                                                          senha):
                    params["status"] = 0
                else:
                    params["status"] = 1

                jsonMsg = Mensagem(TipoMensagem.nova_senha, params).toJson()
                self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.ranking:
                badges_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'badges.csv')
                pontuacao_db = PontuacaoDB()
                ranking = {
                    'ranking': pontuacao_db.ranking_geral(),
                    'ranking_evento': pontuacao_db.ranking_evento(),
                    'badges': Badges().ler_csv(badges_path),
                    'doacoes': {'meta': DoacaoDB().meta_doacoes_progresso()}
                }

                jsonMsg = Mensagem(TipoMensagem.ranking, ranking).toJson()
                self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.perfil:
                usuario = mensagem.params['usuario']
                if usuario:
                    badges_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'badges.csv')
                    pontuacao_db = PontuacaoDB()
                    doacao_db = DoacaoDB()
                    ranking = {
                        'ranking': pontuacao_db.ranking_geral(),
                        'ranking_evento': pontuacao_db.ranking_evento(),
                        'badges': Badges().ler_csv(badges_path),
                        'doacoes': {'meta': doacao_db.meta_doacoes_progresso()}
                    }

                    historico_jogos = HistoricoJogo().all(usuario)

                    perfil = {
                        'usuario': usuario,
                        'ranking': ranking,
                        'historico_jogos': historico_jogos,
                        'doadores': doacao_db.nomes_doadores()
                    }
                else:
                    perfil = {}
                jsonMsg = Mensagem(TipoMensagem.perfil, perfil).toJson()
                self.sendMessage(jsonMsg)

            else:
                try:
                    _gerenciadorPrincipal.interpretaMensagem(self, mensagem)
                except:
                    traceback.print_exc()
                    print("[ERRO][Server] Gerenciador nao interpretou a mensagem: ", mensagem.toJson())

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0
        self.clientesConectados = {}

    def register(self, client):
        if not client in self.clients:
            print("registered client " + client.peer)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client " + client.peer)
            _gerenciadorPrincipal.clienteDesconectou(client)
            self.clients.remove(client)

    def broadcast(self, msg):
        # print("broadcasting message '%s' .." % msg)
        for c in self.clients:
            c.sendMessage(msg.encode('utf-8'))
            print("message sent to " + c.peer)

    def usuarioEstaConectado(self, usuario):
        return usuario in self.clientesConectados

    def clienteConectou(self, socket, usuario):
        self.register(socket)
        self.clientesConectados[usuario] = socket

    def desconectaUsuario(self, usuario):
        socket = self.clientesConectados[usuario]
        socket.sendClose()
        self.unregister(socket)
        del self.clientesConectados[usuario]


_gerenciadorPrincipal = None


def signal_handler(signal, frame):
    if _gerenciadorPrincipal != None:
        _gerenciadorPrincipal.fecha()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='war server')
    parser.add_argument('-d', '--debug',
                        action='store_true', dest='debug',
                        help='Execute server on debug mode.')
    parser.add_argument('-ws', '--websocket',
                        default=8080,
                        help='Web socket port.')
    parser.add_argument('-s', '--server',
                        default=9092,
                        help='Server port.')

    args = parser.parse_args()

    if args.debug:
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    logging.basicConfig(filename='log/server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S')

    # _loggerIP = logging.getLogger('ip')
    # _loggerIP.setLevel(logging.DEBUG)
    # loggerIPch = logging.StreamHandler()
    # loggerIPch.setLevel(logging.DEBUG)
    # loggerFormatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s","%Y-%m-%d %H:%M:%S")
    # loggerIPch.setFormatter(loggerFormatter)
    # _loggerIP.addHandler(loggerIPch)

    # _loggerIP.debug('Teste')

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory("ws://localhost:{}".format(args.websocket),
                            debug=debug,
                            debugCodePaths=debug)
    print('Servido websocket iniciado na porta {}.'.format(args.websocket))

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions()
    listenWS(factory)

    _gerenciadorPrincipal = gerenciador.GerenciadorPrincipal()
    _banco = banco.Banco()

    webdir = File("./webdir")
    web = Site(webdir)
    reactor.listenTCP(int(args.server), web)
    print('Servido web iniciado na porta {}.'.format(args.server))

    reactor.run()

    signal.signal(signal.SIGINT, signal_handler)
