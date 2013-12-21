#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
import gerenciador
import banco
from mensagens import *
                               
class BroadcastServerProtocol(WebSocketServerProtocol):

    def onMessage(self, msg, binary):
        if not binary:
            print "[%s] Enviou: %s" % (self.peerstr, msg)
            mensagem = Mensagem()
            mensagem.fromJson(msg)
            if mensagem.tipo == TipoMensagem.entrar:
                params = {}
                
                usuario = mensagem.params['usuario']
                if self.factory.usuarioEstaConectado(usuario):
                    params["status"] = 2
                    # TODO: Enviar mensagem para o outro socket do usuario uma 
                    # mensagem com o motivo da sua desconexao.
                    # jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                    # print "# ", jsonMsg
                    # self.sendMessage(jsonMsg)
                    
                    self.factory.desconectaUsuario(usuario)
            
                if _banco.verificaCredenciaisDoUsuario(usuario, mensagem.params['senha']):
                    self.factory.clienteConectou(self, usuario)
                    _gerenciador.clienteConectou(self, usuario)
                    
                    params["status"] = 1
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                    print "# ", jsonMsg
                    self.sendMessage(jsonMsg)
                else:
                    params["status"] = 0
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.entrar, params), default=lambda o: o.__dict__)
                    print "# ", jsonMsg
                    self.sendMessage(jsonMsg)

            elif mensagem.tipo == TipoMensagem.registrar:
                params = {}
                usuario = mensagem.params['usuario']
                senha = mensagem.params['senha']
                if _banco.usuarioExiste(usuario):
                    params["status"] = 0
                else:
                    _banco.registraUsuario(usuario, senha)
                    params["status"] = 1
                    
                jsonMsg = json.dumps(Mensagem(TipoMensagem.registrar, params), default=lambda o: o.__dict__)
                print "# ", jsonMsg
                self.sendMessage(jsonMsg)
            elif mensagem.tipo == TipoMensagem.iniciar_partida:
                _gerenciador.iniciaPartida()
            elif mensagem.tipo == TipoMensagem.finalizar_turno:
                _gerenciador.finalizaTurno(self)
            elif (mensagem.tipo == TipoMensagem.colocar_tropa or 
                mensagem.tipo == TipoMensagem.atacar or 
                mensagem.tipo == TipoMensagem.mover or
                mensagem.tipo == TipoMensagem.trocar_cartas_territorio):
                _gerenciador.requisicao(self, mensagem)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        

class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug = False, debugCodePaths = False):
        WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.clientesConectados = {}

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            _gerenciador.clienteDesconectou(client)
            self.clients.remove(client)

    def broadcast(self, msg):
        print "broadcasting message '%s' .." % msg
        for c in self.clients:
            c.sendMessage(msg)
            print "message sent to " + c.peerstr
    
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

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

        
    ServerFactory = BroadcastServerFactory
    factory = ServerFactory("ws://localhost:9002",
                            debug = debug,
                            debugCodePaths = debug)
    print 'Servido websocket iniciado na porta 9002.'

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76 = True)
    listenWS(factory)

    _gerenciador = gerenciador.Gerenciador(factory)
    _banco = banco.Banco()

    webdir = File("./webdir")
    web = Site(webdir)
    reactor.listenTCP(9092, web)
    print 'Servido web iniciado na porta 9092.'

    reactor.run()
