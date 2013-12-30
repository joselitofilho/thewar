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
        self._sala = Sala()
        self._jogo = None
        self._jogadores = {}

    def clienteConectou(self, cliente, usuario):
        self._jogadores[cliente] = usuario
        
        if self._jogo == None:
            self._sala.adiciona(cliente, usuario)
        else:
            self._jogo.adiciona(cliente, usuario)

    def clienteDesconectou(self, cliente):
        usuario = self._jogadores[cliente]
        if self._jogo == None:
            self._sala.remove(usuario)
        else:
            self._jogo.remove(usuario)
            
            if not self._jogo.temJogadorOnLine():
                self.jogoTerminou(self._jogo.id)
        
        del self._jogadores[cliente]

    def iniciaPartida(self):
        if len(self._sala.jogadores) >= 3 and self._jogo == None:
            jogadoresDaSala = self._sala.jogadores
            clientes = self._sala.clientes.copy()

            jogadoresDoJogo = {}
            for k, v in clientes.iteritems():
                jogadorDaSala = jogadoresDaSala[k]
                jogadoresDoJogo[k] = JogadorDoJogo(
                        jogadorDaSala.usuario,
                        jogadorDaSala.posicao,
                        jogadorDaSala.dono)
            self._jogo = Jogo(self, clientes, jogadoresDoJogo)

            self._jogo.inicia()
            del self._sala

    def finalizaTurno(self, cliente):
        if self._jogo != None:
            usuario = self._jogadores[cliente]
            self._jogo.finalizaTurno(usuario)

    def requisicao(self, cliente, mensagem):
        usuario = self._jogadores[cliente]
        
        if self._sala != None and self._jogo == None:
            if mensagem.tipo == TipoMensagem.altera_posicao_na_sala:
                novaPosicao = mensagem.params['novaPosicao']
                self._sala.alteraPosicao(usuario, novaPosicao)
                
        elif self._jogo != None:
            if mensagem.tipo == TipoMensagem.colocar_tropa:
                territorio = mensagem.params['territorio']
                quantidade = mensagem.params['quantidade']
                self._jogo.colocaTropaReq(usuario, territorio, quantidade)
            elif mensagem.tipo == TipoMensagem.atacar:
                dosTerritorios = mensagem.params['dosTerritorios']
                paraOTerritorio = mensagem.params['paraOTerritorio']
                self._jogo.ataca(usuario, dosTerritorios, paraOTerritorio)
            elif mensagem.tipo == TipoMensagem.mover:
                doTerritorio = mensagem.params['doTerritorio']
                paraOTerritorio = mensagem.params['paraOTerritorio']
                quantidade = mensagem.params['quantidade']
                self._jogo.move(usuario, doTerritorio, paraOTerritorio, quantidade)
            elif mensagem.tipo == TipoMensagem.trocar_cartas_territorio:
                cartasTerritorio = mensagem.params['cartasTerritorios']
                self._jogo.trocaCartasTerritorio(usuario, cartasTerritorio)
            elif mensagem.tipo == TipoMensagem.msg_chat_jogo:
                texto = mensagem.params['texto']
                self._jogo.msgChat(usuario, texto)
                
    def jogoTerminou(self, idJogo):
        if self._jogo != None:
            self._jogo.fecha()
            del self._jogo
            self._jogo = None
        self._sala = Sala()

    def fecha(self):
        if self._jogo != None:
            self._jogo.fecha()
            del self._jogo
            self._jogo = None
