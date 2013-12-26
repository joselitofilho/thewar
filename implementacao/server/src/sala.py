from jogador import *
from mensagens import *

class Sala(object):
    _proximaPosicao = 0
    _jogadores = {}
    _dono = None
    _clientes = {} #[posicao] = socket

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
            self.enviaMsgParaTodos(TipoMensagem.lista_sala, listaSalaMsg)

    def remove(self, usuario):
        posicao = -1
        for k, v in self._jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v != None and v.usuario == usuario:
                posicao = k
                self._proximaPosicao = posicao

        if posicao > -1:
            jogador = self._jogadores[posicao]

            saiuDaSalaMsg = SaiuDaSala(jogador)
            self.enviaMsgParaTodos(TipoMensagem.saiu_da_sala, saiuDaSalaMsg)

            del self._jogadores[posicao]
            del self._clientes[posicao]
            
    def alteraPosicao(self, usuario, novaPosicao):
        if 0 <= novaPosicao <= 5:
            posicaoAtual = -1
            for k, v in self._jogadores.iteritems():
                if v != None and v.usuario == usuario:
                    posicaoAtual = k
                    v.posicao = novaPosicao
                    self._jogadores[novaPosicao] = self._jogadores[k]
                    self._jogadores[k] = None
                    
                    msg = AlteraPosicaoNaSala(self._jogadores[novaPosicao], k)
                    self.enviaMsgParaTodos(TipoMensagem.altera_posicao_na_sala, msg)
                    break

    def verificaDono(self, posicao):
        if self._dono == None:
            self._dono = posicao

    def lista(self):
        return self._jogadoresDaSala

    def enviaMsgParaTodos(self, tipo, msg):
        jsonMsg = json.dumps(Mensagem(tipo, msg), default=lambda o: o.__dict__)
        for socket in self._clientes.values():
            socket.sendMessage(jsonMsg)
        print "# ", jsonMsg

    @property
    def jogadores(self):
        return self._jogadores

    @property
    def clientes(self):
        return self._clientes

    @property
    def dono(self):
        return self._dono
