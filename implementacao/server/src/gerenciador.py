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
        self._jogadores = {}

    def clienteConectou(self, cliente, usuario):
        if self._estado == Estado.iniciando_sala:
            jogador = Jogador(usuario)
            jogador.socket = cliente
            self._jogadores[cliente] = jogador

            posicaoJogador = self._sala.adiciona(cliente, jogador)
            donoDaSala = (self._sala.dono == posicaoJogador)

            # Apenas para o jogador que acabou de entrar na sala, indicamos se ele eh o dono da sala.
            jogadorDaSala = JogadorDaSala(usuario, posicaoJogador, donoDaSala)
            entrouNaSalaMsg = EntrouNaSala(jogadorDaSala)
            jsonMsg = json.dumps(Mensagem(TipoMensagem.entrou_na_sala, entrouNaSalaMsg), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            cliente.sendMessage(jsonMsg)

            # Envia a todos os clientes a lista da sala.
            listaSalaMsg = ListaSala(self._sala.lista())
            jsonMsg = json.dumps(Mensagem(TipoMensagem.lista_sala, listaSalaMsg), default=lambda o: o.__dict__) 
            print "# ", jsonMsg
            self._websocket.broadcast(jsonMsg)

    def clienteDesconectou(self, cliente):
        if self._estado == Estado.iniciando_sala:
            jogador = self._jogadores[cliente]
            posicaoJogador = self._sala.remove(jogador)

            saiuDaSalaMsg = SaiuDaSala(posicaoJogador)

            jsonMsg = json.dumps(Mensagem(TipoMensagem.saiu_da_sala, saiuDaSalaMsg), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            self._websocket.broadcast(jsonMsg)

    def iniciaPartida(self):
        if self._estado == Estado.iniciando_sala:

            jogadores = self._sala.jogadores
            self._jogo = Jogo(jogadores)
            
            jogadorQueComeca = self._jogo.faseI_DefinirQuemComeca()
            territoriosDosJogadores = self._jogo.faseI_DistribuirTerritorios()
            cartasObjetivos = self._jogo.faseI_DefinirObjetivos()

            jsonMsg = json.dumps(Mensagem(
                TipoMensagem.jogo_fase_I, 
                JogoFaseI(jogadorQueComeca, territoriosDosJogadores)), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            self._websocket.broadcast(jsonMsg)

            # NOTA: A carta objetivo deve ser enviada apenas ao jogador.
            for i in range(len(jogadores)):
                jsonMsg = json.dumps(Mensagem(
                    TipoMensagem.carta_objetivo,
                    CartaObjetivo(cartasObjetivos[i])), default=lambda o: o.__dict__)
                print "# ", jsonMsg
                jogadores[i].socket.sendMessage(jsonMsg)

            self._estado = Estado.iniciando_jogo

            self.iniciaTurnoDoJogo()

    def iniciaTurnoDoJogo(self):
        if self._estado == Estado.iniciando_jogo:
            self._estado = Estado.jogando
            acaoDoTurno = self._jogo.inicia()
            
            jsonMsg = json.dumps(Mensagem(TipoMensagem.turno, acaoDoTurno), default=lambda o: o.__dict__)
            self._websocket.broadcast(jsonMsg)
            print "# ", jsonMsg

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
