import json
from mensagens import *
from estado import *
from jogador import *
from sala import *
from jogo import *

class Gerenciador(object):
    _websocket = None
    _estado = None 
    _sala = None
    _jogo = None
    _jogadores = {}

    def __init__(self, websocket):
        self._websocket = websocket
        self._estado = Estado.iniciando_sala
        self._sala = Sala()
        self._jogo = None
        self._jogadores = {}

    def clienteConectou(self, cliente, usuario):
        if self._estado == Estado.iniciando_sala and self._jogo == None:
            jogador = Jogador(usuario)
            self._jogadores[cliente] = jogador

            self._sala.adiciona(cliente, usuario)

    def clienteDesconectou(self, cliente):
        if self._estado == Estado.iniciando_sala:
            jogador = self._jogadores[cliente]
            self._sala.remove(jogador.usuario)

    def iniciaPartida(self):
        if self._jogo == None:
            jogadoresDaSala = self._sala.jogadores
            clientes = self._sala.clientes

            jogadoresDoJogo = {}
            for k, v in clientes.iteritems():
                jogadorDaSala = jogadoresDaSala[k]
                jogadoresDoJogo[k] = JogadorDoJogo(
                        jogadorDaSala.usuario,
                        jogadorDaSala.posicao,
                        jogadorDaSala.dono)
            self._jogo = Jogo(clientes, jogadoresDoJogo)

            self._jogo.inicia()
            self._estado = Estado.jogando

    def finalizaTurno(self, socket):
        if self._estado == Estado.jogando:
            self._jogo.finalizaTurno(socket)

    def requisicao(self, socket, mensagem):
        # TODO: Pegar a posicao do jogador pelo socket.
        if mensagem.tipo == TipoMensagem.colocar_tropa:
            posicaoJogador = mensagem.params['posicaoJogador']
            territorio = mensagem.params['territorio']
            quantidade = mensagem.params['quantidade']
            if self._jogo != None:
                self._jogo.colocaTropaReq(socket, posicaoJogador, territorio, quantidade)
        elif mensagem.tipo == TipoMensagem.atacar:
            posicaoJogador = mensagem.params['posicaoJogador']
            dosTerritorios = mensagem.params['dosTerritorios']
            paraOTerritorio = mensagem.params['paraOTerritorio']
            self._jogo.ataca(socket, posicaoJogador, dosTerritorios, paraOTerritorio)
        elif mensagem.tipo == TipoMensagem.mover:
            posicaoJogador = mensagem.params['posicaoJogador']
            doTerritorio = mensagem.params['doTerritorio']
            paraOTerritorio = mensagem.params['paraOTerritorio']
            quantidade = mensagem.params['quantidade']
            self._jogo.move(socket, posicaoJogador, doTerritorio, paraOTerritorio, quantidade)
        elif mensagem.tipo == TipoMensagem.trocar_cartas_territorio:
            posicaoJogador = mensagem.params['posicaoJogador']
            cartasTerritorio = mensagem.params['cartasTerritorios']
            self._jogo.trocaCartasTerritorio(socket, posicaoJogador, cartasTerritorio)
