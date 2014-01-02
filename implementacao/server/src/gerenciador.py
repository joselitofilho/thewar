import json
from mensagens import *
from jogador import *
from sala import *
from jogo import *

class Gerenciador(object):
    def __init__(self):
        self.sala = Sala()
        self.jogo = None
        self.jogadores = {}

    def clienteConectou(self, cliente, usuario):
        self.jogadores[cliente] = usuario
        
        if self.jogo == None:
            self.sala.adiciona(cliente, usuario)
        else:
            self.jogo.adiciona(cliente, usuario)

    def clienteDesconectou(self, cliente):
        usuario = self.jogadores[cliente]
        if self.jogo == None:
            self.sala.remove(usuario)
        else:
            self.jogo.remove(usuario)
            
            if not self.jogo.temJogadorOnLine():
                self.jogoTerminou(self.jogo.id)
        
        del self.jogadores[cliente]

    def iniciaPartida(self):
        if len(self.sala.jogadores) >= 3 and self.jogo == None:
            jogadoresDaSala = self.sala.jogadores
            clientes = self.sala.clientes.copy()

            jogadoresDoJogo = {}
            for k, v in clientes.iteritems():
                jogadorDaSala = jogadoresDaSala[k]
                jogadoresDoJogo[k] = JogadorDoJogo(
                        jogadorDaSala.usuario,
                        jogadorDaSala.posicao,
                        jogadorDaSala.dono)
            self.jogo = Jogo(self, clientes, jogadoresDoJogo)

            self.jogo.inicia()
            del self.sala

    def finalizaTurno(self, cliente):
        if self.jogo != None:
            usuario = self.jogadores[cliente]
            self.jogo.finalizaTurno(usuario)

    def requisicao(self, cliente, mensagem):
        usuario = self.jogadores[cliente]
        
        if self.sala != None and self.jogo == None:
            if mensagem.tipo == TipoMensagem.altera_posicao_na_sala:
                novaPosicao = mensagem.params['novaPosicao']
                self.sala.alteraPosicao(usuario, novaPosicao)
                
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
            elif mensagem.tipo == TipoMensagem.trocar_cartas_territorio:
                cartasTerritorio = mensagem.params['cartasTerritorios']
                self.jogo.trocaCartasTerritorio(usuario, cartasTerritorio)
            elif mensagem.tipo == TipoMensagem.msg_chat_jogo:
                texto = mensagem.params['texto']
                self.jogo.msgChat(usuario, texto)
                
    def jogoTerminou(self, idJogo):
        if self.jogo != None:
            self.jogo.fecha()
            del self.jogo
            self.jogo = None
        self.sala = Sala()

    def fecha(self):
        if self.jogo != None:
            self.jogo.fecha()
            del self.jogo
            self.jogo = None
