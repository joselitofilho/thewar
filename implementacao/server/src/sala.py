from jogador import *
from mensagens import *


class EstadoDaSala:
    sala_criada = "sala_criada"
    jogo_em_andamento = "jogo_em_andamento"


class Sala(object):
    def __init__(self, nome):
        self.id = nome
        self.proximaPosicao = 0
        self.jogadores = {}
        self.dono = None

        print
        "Sala[" + str(self.id) + "] criada."

    def salaEstaCheia(self):
        return len(self.jogadores) == 6;

    def adiciona(self, usuario):
        jogador = None
        posicao = self.posicaoDoUsuario(usuario)
        if not self.salaEstaCheia() and posicao == -1:
            posicao = self.proximaPosicao
            self.verificaDono(posicao)

            jogador = JogadorDaSala(usuario, posicao, (self.dono == posicao and posicao > -1))
            self.jogadores[posicao] = jogador

            self.defineProximaPosicao()

        if jogador != None:
            extra = {
                "entrou_ou_saiu": 1,
                "jogador": jogador
            }
            infoSalaMsg = InfoSala(self.id,
                                   EstadoDaSala.sala_criada,
                                   self.jogadores.values(), extra)
            return infoSalaMsg

        return None

    def remove(self, usuario):
        posicao = self.posicaoDoUsuario(usuario)

        if posicao > -1:
            jogador = self.jogadores[posicao]
            self.jogadores.pop(posicao)

            self.defineProximaPosicao()

            extra = {
                "entrou_ou_saiu": 0,
                "jogador": jogador
            }

            if jogador.dono:
                self.dono = None
                self.escolheNovoDono()

            infoSalaMsg = InfoSala(self.id,
                                   EstadoDaSala.sala_criada,
                                   self.jogadores.values(), extra)
            return infoSalaMsg

        return None

    def posicaoDoUsuario(self, usuario):
        posicao = -1

        for k, v in self.jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.usuario == usuario:
                posicao = k

        return posicao

    def alteraPosicao(self, usuario, novaPosicao):
        retorno = None

        if 0 <= novaPosicao <= 5 and novaPosicao not in self.jogadores.keys():
            posicaoAtual = self.posicaoDoUsuario(usuario)

            # Usuario entrando na sala.
            if posicaoAtual == -1:
                retorno = self.adiciona(usuario)
            else:
                jogador = self.jogadores[posicaoAtual]
                jogador.posicao = novaPosicao
                self.jogadores[novaPosicao] = self.jogadores[posicaoAtual]
                self.jogadores.pop(posicaoAtual)

                if jogador.dono:
                    self.dono = novaPosicao

                retorno = AlteraPosicaoNaSala(self.id, self.jogadores[novaPosicao], posicaoAtual)

                self.defineProximaPosicao()

        return retorno

    def verificaDono(self, posicao):
        if self.dono == None:
            self.dono = posicao

    def escolheNovoDono(self):
        if self.dono == None:
            for pos in self.jogadores.keys():
                self.jogadores[pos].dono = False

            for pos in self.jogadores.keys():
                self.dono = pos
                self.jogadores[pos].dono = True
                break

    def defineProximaPosicao(self):
        for i in range(6):
            proximaPosicao = i % 6
            if proximaPosicao not in self.jogadores.keys():
                self.proximaPosicao = proximaPosicao
                break

    def vazia(self):
        return len(self.jogadores) == 0

    # def __del__(self):
    #    del self.jogadores
