from jogador import *
from mensagens import *

class Sala(object):
    _proximaPosicao = 0
    _jogadores = {}
    _dono = None
    _clientes = {}

    def __init__(self):
        print "Sala criada."
    
    def salaEstaCheia(self):
        return len(self._jogadores) == 6;

    def adiciona(self, cliente, usuario):
        jogador = None

        if not self.salaEstaCheia():
            posicao = self._proximaPosicao
            self.verificaDono(posicao)
       
            jogador = JogadorDaSala(usuario, posicao, (self._dono == posicao))
            self._jogadores[posicao] = jogador
            self._clientes[posicao] = cliente

            for i in range(1, 6):
                proximaPosicao = (posicao + i) % 6
                if proximaPosicao not in self._jogadores.keys():
                    self._proximaPosicao = proximaPosicao
                    break

        # Apenas para o jogador que acabou de entrar na sala, indicamos se ele eh o dono da sala.
        entrouNaSalaMsg = EntrouNaSala(jogador)
        jsonMsg = json.dumps(Mensagem(TipoMensagem.entrou_na_sala, entrouNaSalaMsg), default=lambda o: o.__dict__)
        print "# ", jsonMsg
        cliente.sendMessage(jsonMsg)

        if jogador != None:
            listaSalaMsg = ListaSala(self._jogadores.values())
            self.enviaParaTodos(TipoMensagem.lista_sala, listaSalaMsg)

    def remove(self, usuario):
        posicao = -1
        for k, v in self._jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.usuario == usuario:
                posicao = k
                self._proximaPosicao = posicao

        if posicao > -1:
            jogador = self._jogadores[posicao]

            saiuDaSalaMsg = SaiuDaSala(jogador)
            self.enviaParaTodos(TipoMensagem.saiu_da_sala, saiuDaSalaMsg)

            del self._jogadores[posicao]
            del self._clientes[posicao]

    def verificaDono(self, posicao):
        if self._dono == None:
            self._dono = posicao

    def lista(self):
        return self._jogadoresDaSala

    def enviaParaTodos(self, tipo, msg):
        for socket in self._clientes.values():
            jsonMsg = json.dumps(Mensagem(tipo, msg), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            socket.sendMessage(jsonMsg)

    @property
    def jogadores(self):
        return self._jogadores

    @property
    def dono(self):
        return self._dono
