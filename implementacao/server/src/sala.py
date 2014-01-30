from jogador import *
from mensagens import *

class EstadoDaSala:
    sala_criada = "sala_criada"
    jogo_em_andamento = "jogo_em_andamento"

class Sala(object):
    def __init__(self, nome, gerenciadorSala = None):
        self.id = nome
        self.gerenciadorSala = gerenciadorSala
        self.proximaPosicao = 0
        self.jogadores = {}
        self.dono = None
    
        print "Sala[" + str(self.id) + "] criada."
    
    def salaEstaCheia(self):
        return len(self.jogadores) == 6;

    def adiciona(self, usuario):
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
            infoSalaMsg = InfoSala(self.id, 
                    EstadoDaSala.sala_criada,
                    self.jogadores.values(), extra)
            self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
            return Mensagem(TipoMensagem.info_sala, infoSalaMsg)

        return None

    def remove(self, usuario):
        posicao = -1
        for k, v in self.jogadores.iteritems():
            # TODO: Equals do objeto jogador...
            if v.usuario == usuario:
                posicao = k

        if posicao > -1:
            jogador = self.jogadores[posicao]
            self.jogadores.pop(posicao)
            
            self.defineProximaPosicao()
            
            if jogador.dono:
                self.verificaDono();

            extra = {
                "entrou_ou_saiu": 0,
                "jogador": jogador
            }
            infoSalaMsg = InfoSala(self.id,
                    EstadoDaSala.sala_criada,
                    self.jogadores.values(), extra)
            self.enviaMsgParaTodos(TipoMensagem.info_sala, infoSalaMsg)
            
    def alteraPosicao(self, cliente, usuario, novaPosicao):
        try:
            if 0 <= novaPosicao <= 5 and novaPosicao not in self.jogadores.keys():
                posicaoAtual = -1
                for k, v in self.jogadores.iteritems():
                    if v != None and v.usuario == usuario:
                        posicaoAtual = k
                        v.posicao = novaPosicao
                        self.jogadores[novaPosicao] = self.jogadores[k]
                        self.jogadores.pop(k)
                        
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
        
    def vazia(self):
        return len(self.jogadores) == 0
    
    def enviaMsgParaTodos(self, tipo, msg):
        if self.gerenciadorSala != None:
            self.gerenciadorSala.enviaMsgParaTodos(tipo, msg)

    def __del__(self):
        del self.jogadores
