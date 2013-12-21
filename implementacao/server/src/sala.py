from jogador import *
from mensagens import *

class Sala(object):
    _proximaPosicao = 0
    _jogadores = {}
    _dono = None
    _clientes = []

    def __init__(self):
        print "Sala criada."
        self._clientes = []
    
    def salaEstaCheia(self):
        return len(self._jogadores) == 6;

    def adiciona(self, cliente, usuario):
        jogador = None

        if not self.salaEstaCheia():
            posicao = self._proximaPosicao
            self.verificaDono(posicao)
       
            jogador = JogadorDaSala(usuario, posicao, (self._dono == posicao))
            self._jogadores[posicao] = jogador

            for i in range(1, 6):
                proximaPosicao = (posicao + i) % 6
                if proximaPosicao not in self._jogadores.keys():
                    self._proximaPosicao = proximaPosicao
                    break

            self._clientes.append(cliente)

        # Apenas para o jogador que acabou de entrar na sala, indicamos se ele eh o dono da sala.
        entrouNaSalaMsg = EntrouNaSala(jogador)
        jsonMsg = json.dumps(Mensagem(TipoMensagem.entrou_na_sala, entrouNaSalaMsg), default=lambda o: o.__dict__)
        print "# ", jsonMsg
        cliente.sendMessage(jsonMsg)

        if jogador != None:
            for socket in self._clientes:
                # Envia a todos os clientes a lista da sala.
                listaSalaMsg = ListaSala(self._jogadores.values())
                jsonMsg = json.dumps(Mensagem(TipoMensagem.lista_sala, listaSalaMsg), default=lambda o: o.__dict__)
                print "# ", jsonMsg
                socket.sendMessage(jsonMsg)

    def remove(self, jogador):
        posicao = -1
        for k, v in self._jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.usuario == jogador.usuario:
                posicao = k
                self._proximaPosicao = posicao

        if posicao > -1:
            del self._jogadores[posicao]

        return posicao

    def verificaDono(self, posicao):
        if self._dono == None:
            self._dono = posicao

    def lista(self):
        return self._jogadoresDaSala

    @property
    def jogadores(self):
        return self._jogadores

    @property
    def dono(self):
        return self._dono
