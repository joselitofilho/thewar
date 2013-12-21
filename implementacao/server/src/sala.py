from jogador import *

class Sala(object):
    _proximaPosicao = 0
    _jogadores = {}
    _dono = None

    def __init__(self):
        print "Sala criada."
    
    def salaEstaCheia(self):
        return len(self._jogadores) == 6;

    def adiciona(self, cliente, jogador):
        if self.salaEstaCheia():
            return -1

        posicao = self._proximaPosicao
        
        jogador.posicaoNaSala = posicao

        self.verificaDono(posicao)

        self._jogadores[posicao] = jogador

        for i in range(1, 6):
            proximaPosicao = (posicao + i) % 6
            if proximaPosicao not in self._jogadores.keys():
                self._proximaPosicao = proximaPosicao
                break

        return posicao

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
        return self._jogadores.keys()

    @property
    def jogadores(self):
        return self._jogadores

    @property
    def dono(self):
        return self._dono
