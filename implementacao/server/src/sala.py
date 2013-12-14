from jogador import *

class Sala(object):
    _proximaPosicao = 0
    _jogadores = {}
    _dono = None

    def __init__(self):
        print "Sala criada."

    def adiciona(self, jogador):
        posicao = self._proximaPosicao

        self.verificaDono(posicao)

        self._jogadores[posicao] = jogador
        self._proximaPosicao = (posicao + 1) % 6
        return posicao

    def remove(self, jogador):
        posicao = -1
        for k, v in self._jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.socket == jogador.socket:
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
