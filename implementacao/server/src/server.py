#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import signal
import sys
import traceback

import banco
import gerenciador
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
from mensagens import *
from pontuacaodb import *
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onMessage(self, msg, binary):
        if not binary:
            # print "[%s] Enviou: %s" % (self.peer, msg)

            # Retirando qualquer tipo de tag html da mensagem.
            msg = re.sub('<[^<]+?>', '', msg)

            mensagem = Mensagem()
            mensagem.fromJson(msg)

            if mensagem.tipo == TipoMensagem.entrar:
                params = {}

                usuario = mensagem.params['usuario']
                params["usuario"] = usuario

                if len(usuario) > 0 and _banco.verificaCredenciaisDoUsuario(usuario, mensagem.params['senha']):
                    if self.factory.usuarioEstaConectado(usuario):
                        params["status"] = 2
                        # TODO: Enviar mensagem para o outro socket do usuario uma 
                        # mensagem com o motivo da sua desconexao.
                        # jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                        # print "# ", jsonMsg
                        # self.sendMessage(jsonMsg)

                        # TODO: Se for o mesmo socket, nao eh necessario desconectar o jogagdor.
                        self.factory.desconectaUsuario(usuario)

                    params["status"] = 1
                    self.factory.clienteConectou(self, usuario)
                    logging.info('%s %s', usuario, self.peer)

                    jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                    print
                    "# ", jsonMsg
                    self.sendMessage(jsonMsg)

                    _gerenciadorPrincipal.clienteConectou(self, usuario)
                else:
                    params["status"] = 0
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                    print
                    "# ", jsonMsg
                    self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.registrar:
                params = {}
                usuario = mensagem.params['usuario']
                senha = mensagem.params['senha']
                email = mensagem.params['email']
                # TODO: Validar email.
                if len(usuario) > 0 and len(senha) > 0 and len(email) > 0:
                    if _banco.usuarioExiste(usuario):
                        params["status"] = 0
                    else:
                        _banco.registraUsuario(usuario, senha, email)
                        params["status"] = 1
                else:
                    params["status"] = 2

                jsonMsg = json.dumps(Mensagem(TipoMensagem.registrar, params), default=lambda o: o.__dict__)
                print
                "# ", jsonMsg
                self.sendMessage(jsonMsg)
            elif mensagem.tipo == TipoMensagem.ranking:
                pontuacaoDB = PontuacaoDB()
                ranking = pontuacaoDB.ranking()

                jsonMsg = json.dumps(Mensagem(TipoMensagem.ranking, ranking), default=lambda o: o.__dict__)
                print
                "# ", jsonMsg
                self.sendMessage(jsonMsg)
            else:
                try:
                    _gerenciadorPrincipal.interpretaMensagem(self, mensagem)
                except:
                    traceback.print_exc()
                    print
                    "[ERRO][Server] Gerenciador nao interpretou a mensagem: ", mensagem

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
            print
            "registered client " + client.peer
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print
            "unregistered client " + client.peer
            _gerenciadorPrincipal.clienteDesconectou(client)
            self.clients.remove(client)

    def broadcast(self, msg):
        # print "broadcasting message '%s' .." % msg
        for c in self.clients:
            c.sendMessage(msg)
            print
            "message sent to " + c.peer

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

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
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
    factory = ServerFactory("ws://localhost:8080",
                            debug=debug,
                            debugCodePaths=debug)
    print
    'Servido websocket iniciado na porta 8080.'

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions()
    listenWS(factory)

    _gerenciadorPrincipal = gerenciador.GerenciadorPrincipal()
    _banco = banco.Banco()

    webdir = File("./webdir")
    web = Site(webdir)
    reactor.listenTCP(9092, web)
    print
    'Servido web iniciado na porta 9092.'

    reactor.run()

    signal.signal(signal.SIGINT, signal_handler)
