from jogador import *
from mensagens import *

class Sala(object):
    def __init__(self, nome, gerenciadorSala):
        self.id = nome
        self.gerenciadorSala = gerenciadorSala
        self.proximaPosicao = 0
        self.jogadores = {}
        self.dono = None
    
        print "Sala[" + str(self.id) + "] criada."
    
    def salaEstaCheia(self):
        return len(self.jogadores) == 6;

    def adiciona(self, cliente, usuario):
        jogador = None

        if not self.salaEstaCheia():
            posicao = self.proximaPosicao
            self.verificaDono(posicao)
       
            jogador = JogadorDaSala(usuario, posicao, (self.dono == posicao))
            self.jogadores[posicao] = jogador

            self.defineProximaPosicao()

        if jogador != None:
            extra = {
                "entrou_ou_saiu": 1,
                "jogador": jogador
            }
            listaSalaMsg = ListaSala(self.id, self.jogadores.values(), extra)
            self.enviaMsgParaTodos(TipoMensagem.lista_sala, listaSalaMsg)

    def remove(self, usuario):
        posicao = -1
        for k, v in self.jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.usuario == usuario:
                posicao = k

        if posicao > -1:
            jogador = self.jogadores[posicao]
            del self.jogadores[posicao]
            
            self.defineProximaPosicao()
            
            if jogador.dono:
                self.verificaDono();

            extra = {
                "entrou_ou_saiu": 0,
                "jogador": jogador
            }
            listaSalaMsg = ListaSala(self.id, self.jogadores.values(), extra)
            self.enviaMsgParaTodos(TipoMensagem.lista_sala, listaSalaMsg)
            
    def alteraPosicao(self, cliente, usuario, novaPosicao):
        try:
            if 0 <= novaPosicao <= 5 and novaPosicao not in self.jogadores.keys():
                posicaoAtual = -1
                for k, v in self.jogadores.iteritems():
                    if v != None and v.usuario == usuario:
                        posicaoAtual = k
                        v.posicao = novaPosicao
                        self.jogadores[novaPosicao] = self.jogadores[k]
                        del self.jogadores[k]
                        
                        msg = AlteraPosicaoNaSala(self.id, self.jogadores[novaPosicao], k)
                        self.enviaMsgParaTodos(TipoMensagem.altera_posicao_na_sala, msg)
                        
                        self.defineProximaPosicao()
                        break

                # Usuario entrando na sala.
                if posicaoAtual == -1:
                    self.adiciona(cliente, usuario)
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def verificaDono(self, posicao = -1):
        if self.dono == None:
            self.dono = posicao
        else:
            self.dono = None
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

    def lista(self):
        return self.jogadoresDaSala
    
    def enviaMsgParaTodos(self, tipo, msg):
        self.gerenciadorSala.enviaMsgParaTodos(tipo, msg)

    def __del__(self):
        del self.jogadores
