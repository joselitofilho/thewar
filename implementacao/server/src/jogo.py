import math
import random

from mensagens import *
from turno import *
from tipoAcaoTurno import *
from territorio import * 
from carta import * 
from objetivos import * 

class Jogo(object):
    def __init__(self, clientes, jogadores, gerenciador = None):
        random.seed()

        self.gerenciador = gerenciador
        
        self.id = 1
        self.turno = Turno()

        self.clientes = clientes
        self.jogadores = jogadores

        self.olheiros = {}

        self.ordemJogadores = self.jogadores.keys()
        # Indice que aponta para a fila da ordem dos jogador.
        self.indiceOrdemJogadores = None
        # Posicao do jogador que esta jogando no momento.
        self.posicaoJogadorDaVez = None
        # Cabeca da fila que auxiliara a decisao do proximo jogador que ira jogar.
        self.cabecaDaFila = None

        self.cartasTerritorioDoBaralho = []
        self.cartasTerritorioDescartadas = []

        self.jogadorDaVezConquistouTerritorio = False

        self.numeroDaTroca = 1
        
        self.obrigatorioPassarAVez = False

    def inicia(self):
        self.iniciaFaseI()
        self.iniciaTurnos()

    def iniciaFaseI(self):
        jogadorQueComeca = self.faseI_DefinirQuemComeca()
        territoriosDosJogadores = self.faseI_DistribuirTerritorios()
        cartasObjetivos = self.faseI_DefinirObjetivos()
        
        self.enviaMsgParaTodos(TipoMensagem.jogo_fase_I, JogoFaseI(jogadorQueComeca, territoriosDosJogadores))

        # NOTA: A carta objetivo deve ser enviada apenas ao jogador.
        for i in range(len(self.jogadores)):
            jsonMsg = json.dumps(Mensagem(
                TipoMensagem.carta_objetivo,
                CartaObjetivo(cartasObjetivos[i])), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            posicaoJogador = self.ordemJogadores[i]
            self.clientes[posicaoJogador].sendMessage(jsonMsg)

    def faseI_DefinirQuemComeca(self):
        numeroAleatorio = random.randint(0, len(self.jogadores)-1)
        numeroAleatorio = random.randint(0, len(self.jogadores)-1)
        numeroAleatorio = random.randint(0, len(self.jogadores)-1)
        self.cabecaDaFila = numeroAleatorio
        self.indiceOrdemJogadores = self.cabecaDaFila
        self.posicaoJogadorDaVez = self.ordemJogadores[self.cabecaDaFila]
        
        return self.posicaoJogadorDaVez

    def faseI_DistribuirTerritorios(self):
        territorios = list(CodigoTerritorio.Lista)
        random.shuffle(territorios)
        random.shuffle(territorios)
        random.shuffle(territorios)

        listaTerritoriosPorJogador = []
        incremento = []
        
        # Calculando incremento.
        quantidadeDeJogadores = len(self.jogadores)
        if quantidadeDeJogadores == 4:
            incremento.append(10)
            incremento.append(10)
            incremento.append(11)
            incremento.append(11)
        elif quantidadeDeJogadores == 5:
            incremento.append(8)
            incremento.append(8)
            incremento.append(8)
            incremento.append(9)
            incremento.append(9)
        else:
            for i in range(quantidadeDeJogadores):
                incremento.append(42 / quantidadeDeJogadores)
        inicio = 0
        fim = 0
        for i in range(quantidadeDeJogadores):
            fim = fim + incremento[i]

            territoriosJogador_i = []
            for j in range(inicio, fim):
                territoriosJogador_i.append(territorios[j])

            self.jogadores[self.posicaoJogadorDaVez].iniciaTerritorios(territoriosJogador_i)
            listaTerritoriosPorJogador.append(
                    TerritoriosPorJogador(self.posicaoJogadorDaVez, self.jogadores[self.posicaoJogadorDaVez].territorios))
            
            inicio = inicio + incremento[i]
            self.passaParaProximoJogador();

        return listaTerritoriosPorJogador

    def faseI_DefinirObjetivos(self):
        objetivos = range(0, 14)
        random.shuffle(objetivos)
        random.shuffle(objetivos)
        random.shuffle(objetivos)

        objetivoPorJogadores = []
        for i in range(len(self.jogadores)):
            posicaoJogador = self.ordemJogadores[i]
            self.jogadores[posicaoJogador].objetivo = objetivos[i]
            objetivoPorJogadores.append(objetivos[i])

        return objetivoPorJogadores
    
    def iniciaTurnos(self):
        self.cartasTerritorioDoBaralho = list(CartasTerritorio.Todas())
        random.shuffle(self.cartasTerritorioDoBaralho)
        random.shuffle(self.cartasTerritorioDoBaralho)
        random.shuffle(self.cartasTerritorioDoBaralho)
        self.cartasTerritorioDescartadas = []
        
        self.numeroDaTroca = 1

        self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
        acaoDoTurno = self.criaAcaoDoTurno(self.turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

    def criaAcaoDoTurno(self, turno):
        # Qual o turno que esta: 1, 2, 3, ...
        numeroDoTurno = turno.numero
        # Quem esta jogando: posicao do jogador...
        jogadorDaVez = self.posicaoJogadorDaVez
        # Qual a acao que ele deve fazer...
        tipoAcaoDoTurno = turno.tipoAcao

        tempoRestante = turno.tempoRestante
        valorDaTroca = self.calculaQuantidadeDeTropasDaTroca(self.numeroDaTroca)
        
        jogador = self.jogadores[jogadorDaVez]

        acao = None
        # Preencher os dados da acao
        if tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_globais:
            if turno.quantidadeDeTropas == 0:
                qtd = len(jogador.territorios) / 2
                if qtd > 3:
                    turno.quantidadeDeTropas = qtd
                else:
                    turno.quantidadeDeTropas = 3
            acao = AcaoDistribuirTropasGlobais(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca, 
                    turno.quantidadeDeTropas)
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            turno.grupoTerritorioAtual = None
            for grupo in turno.gruposTerritorio:
                turno.grupoTerritorioAtual = grupo
                break
            if turno.quantidadeDeTropas == 0:
                turno.quantidadeDeTropas = GrupoTerritorio.BonusPorGrupo[turno.grupoTerritorioAtual]
            acao = AcaoDistribuirTropasGrupoTerritorio(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca,
                    turno.quantidadeDeTropas, turno.grupoTerritorioAtual)
        elif tipoAcaoDoTurno == TipoAcaoTurno.trocar_cartas:
            acao = AcaoTrocarCartas(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca,
                    (len(jogador.cartasTerritorio) >= 5))
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            acao = AcaoDistribuirTropasTrocaDeCartas(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca,
                    turno.quantidadeDeTropas)
        elif tipoAcaoDoTurno == TipoAcaoTurno.jogo_terminou:
            acao = AcaoJogoTerminou(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca,
                    jogador.objetivo, jogador.usuario)
        else:
            acao = AcaoTurno(tipoAcaoDoTurno, 
                    numeroDoTurno, jogadorDaVez, tempoRestante, valorDaTroca)

        return acao
 
    def todosJogaram(self):
        return self.cabecaDaFila == self.indiceOrdemJogadores

    def passaParaProximoJogador(self):
        # Verifica se o jogador ainda esta no jogo. Caso nao esteja, pula a vez dele.
        ok = False
        for i in range(len(self.ordemJogadores)):
            self.indiceOrdemJogadores = (self.indiceOrdemJogadores + 1) % len(self.ordemJogadores)
            self.posicaoJogadorDaVez = self.ordemJogadores[self.indiceOrdemJogadores]
            self.jogadorDaVezConquistouTerritorio = False
            
            # Verifica se o jogador esta logado na sala e nao foi destruido.
            if self.posicaoJogadorDaVez in self.jogadores.keys():
                if len(self.jogadores[self.posicaoJogadorDaVez].territorios) > 0:
                    ok = True
                    break

        if not ok and self.gerenciador != None:
            self.gerenciador.jogoTerminou(self.id)

    def finalizaTurno_1(self):
        turno = self.turno
        
        if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais and turno.quantidadeDeTropas == 0:
            jogador = self.jogadores[self.posicaoJogadorDaVez]
            if len(jogador.gruposTerritorio()) > 0:
                turno.gruposTerritorio = list(jogador.gruposTerritorio())
                turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
                
                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            else:
                if not self.temUmVencedor():
                    self.passaParaProximoJogador()

                    if self.todosJogaram():
                        turno.numero = 2
                        turno.tipoAcao = TipoAcaoTurno.atacar
                    else:
                        turno.numero = 1
                        turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

                    self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                    acaoDoTurno = self.criaAcaoDoTurno(turno)
                    self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

            if self.temUmVencedor() and self.gerenciador != None:
                self.gerenciador.jogoTerminou(self.id)

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio and turno.quantidadeDeTropas == 0:
            try:
                turno.gruposTerritorio.pop(0)
            except:
                print "[WARN] Nao tem grupo territorio para remover."

            if len(turno.gruposTerritorio) == 0:
                if self.temUmVencedor():
                    turno.tipoAcao = TipoAcaoTurno.jogo_terminou
                else:
                    self.passaParaProximoJogador()
                
                    if self.todosJogaram():
                        turno.numero = 2
                        turno.tipoAcao = TipoAcaoTurno.atacar
                    else:
                        turno.numero = 1
                        turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            
            if self.temUmVencedor() and self.gerenciador != None:
                self.gerenciador.jogoTerminou(self.id)
            
    def finalizaTurno_2(self):
        turno = self.turno

        if turno.tipoAcao == TipoAcaoTurno.atacar:
            turno.numero = 2
            turno.tipoAcao = TipoAcaoTurno.mover
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
        
        elif turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            if turno.tropasParaMoverAposAtaque < 3:
                self.finalizaTurno_moverAposConquistarTerritorio()

        elif turno.tipoAcao == TipoAcaoTurno.mover:
            if self.temUmVencedor():
                turno.tipoAcao = TipoAcaoTurno.jogo_terminou
            else:
                self.enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio()

                self.passaParaProximoJogador()

                if self.todosJogaram():
                    turno.numero = 3
                    turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais
                else:
                    turno.numero = 2
                    turno.tipoAcao = TipoAcaoTurno.atacar

            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            
            if self.temUmVencedor() and self.gerenciador != None:
                self.gerenciador.jogoTerminou(self.id)
            
    def finalizaTurno_I(self):
        turno = self.turno
        erro = True

        if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais:
            if turno.quantidadeDeTropas == 0:
                jogador = self.jogadores[self.posicaoJogadorDaVez]
                if len(jogador.gruposTerritorio()) > 0:
                    turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
                    turno.gruposTerritorio = list(jogador.gruposTerritorio())
                elif len(jogador.cartasTerritorio) > 2:
                    turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    turno.tipoAcao = TipoAcaoTurno.atacar
                    
                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            if turno.quantidadeDeTropas == 0:
                try:
                    turno.gruposTerritorio.pop(0)
                except:
                    print "WARN: Nao tem grupo territorio para remover."

                jogador = self.jogadores[self.posicaoJogadorDaVez]

                if len(turno.gruposTerritorio) == 0:
                    if len(jogador.cartasTerritorio) > 2:
                        turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                    else:
                        turno.tipoAcao = TipoAcaoTurno.atacar

                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            if turno.quantidadeDeTropas == 0:
                jogador = self.jogadores[self.posicaoJogadorDaVez]
                if len(jogador.cartasTerritorio) > 2:
                    turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    turno.tipoAcao = TipoAcaoTurno.atacar
                
                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.trocar_cartas:
            jogador = self.jogadores[self.posicaoJogadorDaVez]
            print "Obrigatorio passar a vez?", self.obrigatorioPassarAVez
            if len(jogador.cartasTerritorio) < 5 or self.obrigatorioPassarAVez:
                if self.obrigatorioPassarAVez:
                    turno.tipoAcao = TipoAcaoTurno.mover
                else:
                    turno.tipoAcao = TipoAcaoTurno.atacar
                
                self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False
                self.obrigatorioPassarAVez = False

        elif turno.tipoAcao == TipoAcaoTurno.atacar:
            turno.tipoAcao = TipoAcaoTurno.mover
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            erro = False
            
        elif turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            if turno.tropasParaMoverAposAtaque < 3:
                self.finalizaTurno_moverAposConquistarTerritorio()
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.mover:
            if self.temUmVencedor():
                turno.tipoAcao = TipoAcaoTurno.jogo_terminou
            else:
                self.enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio()
            
                self.passaParaProximoJogador()
                turno.trocouCartas = False

                if self.todosJogaram():
                    turno.numero += 1
                turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais
            
            self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            erro = False

            if self.temUmVencedor() and self.gerenciador != None:
                self.gerenciador.jogoTerminou(self.id)
                
            
        if erro:
            socket = self.clientes[self.posicaoJogadorDaVez]
            jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            socket.sendMessage(jsonMsg)

    def finalizaTurno(self, usuario):
        posicaoJogador = -1
        for k, v in self.jogadores.iteritems():
            if v.usuario == usuario:
                posicaoJogador = k

        if posicaoJogador == self.posicaoJogadorDaVez:
            self.turno.paraTimeout()
            if self.turno.numero == 1:
                self.finalizaTurno_1()
            elif self.turno.numero == 2:
                self.finalizaTurno_2()
            else:
                self.finalizaTurno_I()
    
    def finalizaTurnoPorTimeout(self):
        self.turno.reiniciaVariaveisExtras()
        if self.turno.tipoAcao == TipoAcaoTurno.trocar_cartas:
            self.obrigatorioPassarAVez = True
        else:
            self.obrigatorioPassarAVez = False

        if self.turno.numero == 1:
            self.finalizaTurno_1()
        elif self.turno.numero == 2:
            self.finalizaTurno_2()
        else:
            self.finalizaTurno_I()
    
    def finalizaTurno_moverAposConquistarTerritorio(self):
        self.turno.reiniciaVariaveisExtrasMoverAposConquistar()
        self.turno.tipoAcao = TipoAcaoTurno.atacar
        self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
        acaoDoTurno = self.criaAcaoDoTurno(self.turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
        
    def colocaTropaReq(self, usuario, codigoTerritorio, quantidade):
        turno = self.turno
        jogador = self.jogadores[self.posicaoJogadorDaVez]
        
        erro = True
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais or \
                turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
                if quantidade <= turno.quantidadeDeTropas and jogador.temTerritorio(codigoTerritorio):
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(self.jogadores[self.posicaoJogadorDaVez].usuario,
                            quantidade,
                            territorio, 
                            quantidadeTotalRestante))
                    erro = False
            elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
                if quantidade <= turno.quantidadeDeTropas and \
                    jogador.temTerritorio(codigoTerritorio) and \
                    codigoTerritorio in GrupoTerritorio.Dicionario[turno.grupoTerritorioAtual]:
                    
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(self.jogadores[self.posicaoJogadorDaVez].usuario,
                            quantidade,
                            territorio, 
                            quantidadeTotalRestante))
                    erro = False

    def colocaTropaNaTrocaDeCartasTerritorios(self, posicaoJogador, cartasParaTroca):
        territoriosBeneficiados = []
        jogador = self.jogadores[posicaoJogador]
    
        # Verifica se o jogador tem os territorios das cartas, se tiver, adiciona duas tropas nele.
        for carta in cartasParaTroca:
            if jogador.temTerritorio(carta.codigoTerritorio):
                territorio = jogador.adicionaTropasNoTerritorio(carta.codigoTerritorio, 2)
                territoriosBeneficiados.append(territorio);
                
        self.enviaMsgParaTodos(TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios, 
            ColocarTropaNaTrocaDeCartasTerritorios(self.jogadores[posicaoJogador].usuario, 
                territoriosBeneficiados))
    
    def ataca(self, usuario, dosTerritorios, paraOTerritorio):
        turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]
        socket = self.clientes[posicaoJogador]
        
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.atacar:
                if jogador.temOsTerritorios(dosTerritorios) and not jogador.temTerritorio(paraOTerritorio):
                    temErro = False
                
                    # Recuperando territorio da defesa.
                    #   - Identifica o jogador que esta sendo atacado;
                    #   - Identifica o territorio que esta sendo atacado;
                    #   - Pega a quantidade de tropas desse territorio.
                    for k, v in self.jogadores.iteritems():
                        if v.temTerritorio(paraOTerritorio):
                            jogadorDefesa = v
                            territorioDaDefesa = jogadorDefesa.seuTerritorio(paraOTerritorio)
                            quantidadeDadosDefesa = territorioDaDefesa.quantidadeDeTropas
                            if quantidadeDadosDefesa > 3:
                                quantidadeDadosDefesa = 3
                            break
                    
                    if quantidadeDadosDefesa > 0:
                        # Sortear os dados da defesa.
                        dadosDefesa = []
                        for t in range(0, quantidadeDadosDefesa):
                            valorDado = self.jogarDado()
                            dadosDefesa.append(valorDado)
                        dadosDefesa = sorted(dadosDefesa, reverse=True)
                        print "Dados da defesa: ", dadosDefesa
                
                        # Recuperando territorios do ataque.
                        territoriosDoAtaque = []
                        quantidadeDadosAtaque = 0
                        for t in dosTerritorios:
                            territorioObj = jogador.seuTerritorio(t)
                            if (territorioObj.quantidadeDeTropas > 1 and 
                                FronteiraTerritorio.TemFronteira(
                                    territorioDaDefesa.codigo, territorioObj.codigo)):
                                territoriosDoAtaque.append(territorioObj)
                                
                                if territorioObj.quantidadeDeTropas > 3:
                                    quantidadeDadosAtaque += territorioObj.quantidadeDeTropas
                                elif territorioObj.quantidadeDeTropas > 1:
                                    quantidadeDadosAtaque += territorioObj.quantidadeDeTropas - 1
                                else:
                                    temErro = True
                            else:
                                temErro = True
                                break
                    
                        if not temErro:
                            if quantidadeDadosAtaque > 3:
                                quantidadeDadosAtaque = 3
                        
                            # Sortear os dados do ataque.
                            dadosAtaque = []
                            for i in range(0, quantidadeDadosAtaque):
                                valorDado = self.jogarDado()
                                dadosAtaque.append(valorDado)
                            dadosAtaque = sorted(dadosAtaque, reverse=True)
                            print "Dados do ataque: ", dadosAtaque
                        
                            conquistouTerritorio = False
                        
                            # Efetuar ataque e descontar as tropas dos territorios envolvidos nele.
                            for i in range(len(dadosAtaque)):
                                if i < len(dadosDefesa):
                                    if dadosAtaque[i] > dadosDefesa[i]:
                                        # Ataque venceu.
                                        territorioDaDefesa = jogadorDefesa.removeTropasNoTerritorio(
                                                territorioDaDefesa.codigo, 1)

                                        # Verifica se o territorio foi conquistado.
                                        if territorioDaDefesa.quantidadeDeTropas == 0:
                                            jogadorDefesa.territorios.remove(territorioDaDefesa)
                                            jogador.territorios.append(territorioDaDefesa)

                                            # Movendo uma tropa para o territorio conquistado.
                                            territorioDaDefesa = jogador.adicionaTropasNoTerritorio(
                                                    territorioDaDefesa.codigo, 1)

                                            for t in territoriosDoAtaque:
                                                if t.quantidadeDeTropas > 1:
                                                    jogador.removeTropasNoTerritorio(t.codigo, 1)
                                                    break
                                            ######

                                            conquistouTerritorio = True

                                            # Verifica se o jogador destruiu o outro. Caso positivo, as cartas dos territorios
                                            # do jogador derrotado vai para o jogador que o destruiu.
                                            if len(jogadorDefesa.territorios) == 0:
                                                jogador.jogadoresDestruidos.append(jogadorDefesa.posicao)
                                                jogador.cartasTerritorio.extend(jogadorDefesa.cartasTerritorio)
                                                
                                                # Envia as cartas atualizadas para o cliente.
                                                jsonMsg = json.dumps(Mensagem(TipoMensagem.cartas_territorio, 
                                                    jogador.cartasTerritorio), default=lambda o: o.__dict__)
                                                print "# " + jsonMsg
                                                self.clientes[jogador.posicao].sendMessage(jsonMsg)
                                                
                                                # Envia para todos que o jogador foi destruido.
                                                self.enviaMsgParaTodos(TipoMensagem.jogador_destruido,
                                                    JogadorDestruido(jogadorDefesa))

                                            self.jogadorDaVezConquistouTerritorio = True
                                            turno.tropasParaMoverAposAtaque = 0
                                            turno.territoriosDoAtaqueDaConquista = []
                                            for t in territoriosDoAtaque:
                                                if t.quantidadeDeTropas > 1:
                                                    turno.territoriosDoAtaqueDaConquista.append(t.codigo)
                                                    turno.tropasParaMoverAposAtaque += t.quantidadeDeTropas-1
                                                    if turno.tropasParaMoverAposAtaque > 2:
                                                        turno.tropasParaMoverAposAtaque = 2
                                            turno.territorioConquistado = territorioDaDefesa.codigo
                                            
                                            if turno.tropasParaMoverAposAtaque > 0:
                                                turno.tipoAcao = TipoAcaoTurno.mover_apos_conquistar_territorio
                                            break

                                    else:
                                        # Defesa venceu.
                                        self.defesaVenceu(i, territoriosDoAtaque, jogador)
                            
                            self.enviaMsgParaTodos(TipoMensagem.atacar, 
                                Atacar(
                                    {
                                        "posicao": posicaoJogador,
                                        "usuario": self.jogadores[posicaoJogador].usuario
                                    },
                                    {
                                        "posicao": jogadorDefesa.posicao,
                                        "usuario": jogadorDefesa.usuario
                                    },
                                    dadosDefesa, dadosAtaque, 
                                    territorioDaDefesa, territoriosDoAtaque, 
                                    conquistouTerritorio))
                    else:
                        temErro = True
                
                    if temErro:
                        jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                        print "# " + jsonMsg
                        socket.sendMessage(jsonMsg)
                    
    def defesaVenceu(self, i, territoriosDoAtaque, jogador):
        pos = i
        while pos >= 0:
            if pos < len(territoriosDoAtaque) and territoriosDoAtaque[pos].quantidadeDeTropas > 1:
                territoriosDoAtaque[pos] = jogador.removeTropasNoTerritorio(
                    territoriosDoAtaque[pos].codigo,
                    1)
                break
            pos -= 1
        
    def move(self, usuario, doTerritorio, paraOTerritorio, quantidade):
        turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]
        socket = self.clientes[posicaoJogador]
        
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.mover:
                if jogador.temTerritorio(doTerritorio) and jogador.temTerritorio(paraOTerritorio) and \
                    FronteiraTerritorio.TemFronteira(doTerritorio, paraOTerritorio):
                    doTerritorioObj = jogador.seuTerritorio(doTerritorio)
                    paraOTerritorioObj = jogador.seuTerritorio(paraOTerritorio)
                    
                    if doTerritorioObj.quantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.codigo, quantidade)
                        
                        self.enviaMsgParaTodos(TipoMensagem.mover, 
                            Mover(self.jogadores[posicaoJogador].usuario, 
                            doTerritorioObj, paraOTerritorioObj,
                            quantidade))
                    else:
                        jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                        print "# " + jsonMsg
                        socket.sendMessage(jsonMsg)
                else:
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    socket.sendMessage(jsonMsg)
            
            elif turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
                if jogador.temTerritorio(doTerritorio) and \
                    jogador.temTerritorio(paraOTerritorio) and \
                    turno.territorioConquistado == paraOTerritorio and \
                    doTerritorio in turno.territoriosDoAtaqueDaConquista and \
                    turno.tropasParaMoverAposAtaque > 0:
                    
                    doTerritorioObj = jogador.seuTerritorio(doTerritorio)
                    paraOTerritorioObj = jogador.seuTerritorio(paraOTerritorio)
                    
                    if doTerritorioObj.quantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.codigo, quantidade)
                        
                        turno.tropasParaMoverAposAtaque -= quantidade
                        self.enviaMsgParaTodos(TipoMensagem.mover, 
                            Mover(self.jogadores[posicaoJogador].usuario, 
                                doTerritorioObj, paraOTerritorioObj,
                                quantidade))
                    else:
                        jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                        print "# " + jsonMsg
                        socket.sendMessage(jsonMsg)
                else:
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    socket.sendMessage(jsonMsg)
                    
    def moveAposConquistarTerritorio(self, usuario, quantidade):
        turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]
        socket = self.clientes[posicaoJogador]
        
        if jogador.usuario == usuario and turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio:
            paraOTerritorio = turno.territorioConquistado
            for codigo in turno.territoriosDoAtaqueDaConquista:
                terr = jogador.seuTerritorio(codigo)
                if quantidade > 0:
                    doTerritorio = terr.codigo
                    qtdTropasQuePodemSerMovidas = terr.quantidadeDeTropas-1
                    if quantidade > qtdTropasQuePodemSerMovidas:
                        print usuario, doTerritorio, paraOTerritorio, qtdTropasQuePodemSerMovidas
                        self.move(usuario, doTerritorio, paraOTerritorio, qtdTropasQuePodemSerMovidas)
                        quantidade -= qtdTropasQuePodemSerMovidas
                    else:
                        print usuario, doTerritorio, paraOTerritorio, qtdTropasQuePodemSerMovidas   
                        self.move(usuario, doTerritorio, paraOTerritorio, quantidade)
                        break
                        
            self.finalizaTurno_moverAposConquistarTerritorio()
    
    def trocaCartasTerritorio(self, usuario, cartasTerritorio):
        turno = self.turno
        posicaoJogador = self.posicaoJogadorDaVez
        jogador = self.jogadores[posicaoJogador]
        socket = self.clientes[posicaoJogador]
        
        print "[trocaCartasTerritorio] ", cartasTerritorio

        if turno.tipoAcao == TipoAcaoTurno.trocar_cartas and \
            jogador.usuario == usuario and \
            len(cartasTerritorio) == 3:
            
            jogador = self.jogadores[posicaoJogador]
            
            cartasParaTroca = []
            for carta in jogador.cartasTerritorio:
                if carta.codigoTerritorio in cartasTerritorio:
                    cartasParaTroca.append(carta)

            if len(cartasParaTroca) != 3:
                jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                print "# " + jsonMsg
                socket.sendMessage(jsonMsg)
            else:
                # Se chegou aqui, eh porque o jogador tem as cartas dos territorios.
                
                # Verifica se a troca pode ser feita.
                #   - 3 formas iguais
                #   - 3 formas diferentes
                
                podeTrocar = False
                if CartasTerritorio.Coringa in cartasParaTroca:
                    podeTrocar = True
                elif cartasParaTroca[0].forma == cartasParaTroca[1].forma == cartasParaTroca[2].forma:
                    podeTrocar = True
                elif cartasParaTroca[0].forma != cartasParaTroca[1].forma != cartasParaTroca[2].forma:
                    podeTrocar = True
                
                if podeTrocar:
                    turno.trocouCartas = True
                    
                    # Envia informacao do turno.
                    turno.quantidadeDeTropas = self.calculaQuantidadeDeTropasDaTroca(self.numeroDaTroca)
                    self.numeroDaTroca += 1
                    turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_troca_de_cartas
                    self.turno.iniciaTimeout(self.finalizaTurnoPorTimeout)
                    acaoDoTurno = self.criaAcaoDoTurno(turno)
                    self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                
                    self.colocaTropaNaTrocaDeCartasTerritorios(posicaoJogador, cartasParaTroca)

                    # Remove e envia ao jogador suas cartas de territorios atualizadas.
                    for carta in cartasParaTroca:
                        jogador.removeCartaTerritorio(carta)
                        self.cartasTerritorioDescartadas.append(carta);
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.cartas_territorio, jogador.cartasTerritorio), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    self.clientes[self.posicaoJogadorDaVez].sendMessage(jsonMsg)
                else:
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    socket.sendMessage(jsonMsg)                    

    def jogarDado(self):
        dado = [1,2,3,4,5,6]
        random.shuffle(dado)
        random.shuffle(dado)
        random.shuffle(dado)
        return dado[0]

    def calculaQuantidadeDeTropasDaTroca(self, numeroDaTroca):
        if 1 <= numeroDaTroca <= 5:
            return (numeroDaTroca * 2) + 2
        else:
            return (2 * numeroDaTroca) + (3 * (numeroDaTroca - 5))

    def pegaUmaCartaTerritorioDoBaralho(self):
        if len(self.cartasTerritorioDoBaralho) == 0:
            self.cartasTerritorioDoBaralho = list(self.cartasTerritorioDescartadas)
            random.shuffle(self.cartasTerritorioDoBaralho)
            random.shuffle(self.cartasTerritorioDoBaralho)
            random.shuffle(self.cartasTerritorioDoBaralho)
            self.cartasTerritorioDescartadas = []

        return self.cartasTerritorioDoBaralho.pop(0)

    def enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio(self):
        if self.jogadorDaVezConquistouTerritorio:
            jogador = self.jogadores[self.posicaoJogadorDaVez]
            cartaTerritorio = self.pegaUmaCartaTerritorioDoBaralho()
            jogador.adicionaCartaTerritorio(cartaTerritorio)
           
            self.enviaMsgParaCliente(TipoMensagem.cartas_territorio, 
                    jogador.cartasTerritorio, self.clientes[self.posicaoJogadorDaVez])

            self.jogadorDaVezConquistouTerritorio = False

    def adiciona(self, cliente, usuario):
        listaJogadoresInfoCurta = []
        territoriosDosJogadores = []

        # Prepara as informacoes.
        for j in self.jogadores.values():
            # Verifica se o jogador ainda esta conectado.
            if j.posicao in self.clientes.keys():
                listaJogadoresInfoCurta.append({
                    "usuario": j.usuario,
                    "posicao": j.posicao,
                })
                    
            territoriosDosJogadores.append({
                "territorios": j.territorios,
                "posicao": j.posicao
            })

        olheiro = True
        posicao = -1
        for k, v in self.jogadores.iteritems():
            if v != None and v.usuario == usuario:
                # Jogador reconectou!
                posicao = k
                olheiro = False
                self.clientes[k] = cliente

                listaJogadoresInfoCurta = []
                territoriosDosJogadores = []

                # Enviar lista dos jogadores
                for j in self.jogadores.values():
                    # Verifica se o jogador ainda esta conectado.
                    if j.posicao in self.clientes.keys():
                        listaJogadoresInfoCurta.append({
                            "usuario": j.usuario,
                            "posicao": j.posicao,
                        })
                    
                    territoriosDosJogadores.append({
                        "territorios": j.territorios,
                        "posicao": j.posicao
                    })

                self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo, EntrouNoJogo(usuario, posicao))

                jogador = self.jogadores[posicao];
                self.enviaMsgParaCliente(TipoMensagem.carrega_jogo, 
                    CarregaJogo(self.posicaoJogadorDaVez, 
                        territoriosDosJogadores, 
                        listaJogadoresInfoCurta,
                        jogador.objetivo,
                        jogador.cartasTerritorio),
                    cliente)
                
                acaoDoTurno = self.criaAcaoDoTurno(self.turno)
                self.enviaMsgParaCliente(TipoMensagem.turno, acaoDoTurno, cliente)
                
                break

        if olheiro:
            self.olheiros[usuario] = cliente
            self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo, EntrouNoJogo(usuario, 7))
            
            self.enviaMsgParaCliente(TipoMensagem.carrega_jogo_olheiro, 
                CarregaJogoOlheiro(self.posicaoJogadorDaVez, 
                    territoriosDosJogadores, 
                    listaJogadoresInfoCurta),
                cliente)
                
            acaoDoTurno = self.criaAcaoDoTurno(self.turno)
            self.enviaMsgParaCliente(TipoMensagem.turno, acaoDoTurno, cliente)
        
    def remove(self, usuario):
        if usuario in self.olheiros.keys():
            self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, 7))
            del self.olheiros[usuario]
        else:
            for k, v in self.jogadores.iteritems():
                if v.usuario == usuario:
                    self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, k))
                    del self.clientes[k]
                    break

    def temUmVencedor(self):
        jogador = self.jogadores[self.posicaoJogadorDaVez]
        objetivo = FabricaObjetivo().cria(jogador.objetivo)
        return objetivo.completou(jogador, self.jogadores)

    def temJogadorOnLine(self):
        return len(self.clientes) > 0
        
    def msgChat(self, usuario, texto):
        self.enviaMsgParaTodos(TipoMensagem.msg_chat_jogo, MsgChatJogo(usuario, texto))

    def enviaMsgParaCliente(self, tipoMensagem, params, cliente):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        print "# " + jsonMsg
        cliente.sendMessage(jsonMsg)

    def enviaMsgParaTodos(self, tipoMensagem, params):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        for socket in self.clientes.values():
            socket.sendMessage(jsonMsg)
        for socket in self.olheiros.values():
            socket.sendMessage(jsonMsg)
        print "# ", jsonMsg

    def fecha(self):
        self.enviaMsgParaTodos(TipoMensagem.jogo_interrompido, JogoInterrompido(self.id))
        self.turno.paraTimeout()

    def __del__(self):
        self.fecha()
