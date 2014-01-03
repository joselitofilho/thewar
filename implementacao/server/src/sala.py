from jogador import *
from mensagens import *

class Sala(object):
    def __init__(self):
        self.id = 1
        self.proximaPosicao = 0
        self.jogadores = {}
        self.dono = None
        self.clientes = {} #[posicao] = socket
    
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
            self.clientes[posicao] = cliente

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
            del self.clientes[posicao]
            
            self.defineProximaPosicao()
            
            if jogador.dono:
                self.verificaDono();

            extra = {
                "entrou_ou_saiu": 0,
                "jogador": jogador
            }
            listaSalaMsg = ListaSala(self.id, self.jogadores.values(), extra)
            self.enviaMsgParaTodos(TipoMensagem.lista_sala, listaSalaMsg)
            
    def alteraPosicao(self, usuario, novaPosicao):
        try:
            if 0 <= novaPosicao <= 5 and novaPosicao not in self.jogadores.keys():
                posicaoAtual = -1
                for k, v in self.jogadores.iteritems():
                    if v != None and v.usuario == usuario:
                        posicaoAtual = k
                        v.posicao = novaPosicao
                        self.jogadores[novaPosicao] = self.jogadores[k]
                        del self.jogadores[k]
                        
                        self.clientes[novaPosicao] = self.clientes[k]
                        del self.clientes[k]
                        
                        msg = AlteraPosicaoNaSala(self.jogadores[novaPosicao], k)
                        self.enviaMsgParaTodos(TipoMensagem.altera_posicao_na_sala, msg)
                        
                        self.defineProximaPosicao()
                        break
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
        jsonMsg = json.dumps(Mensagem(tipo, msg), default=lambda o: o.__dict__)
        for socket in self.clientes.values():
            if socket != None:
                socket.sendMessage(jsonMsg)
        print "# ", jsonMsg

    def __del__(self):
        del self.jogadores
        del self.clientes
