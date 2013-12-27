import math
import random

from mensagens import *
from turno import *
from tipoAcaoTurno import *
from territorio import * 
from carta import * 
from objetivos import * 

class Jogo(object):
    _turno = None

    _ordemJogadores = []
    _indiceOrdemJogadores = None
    # Posicao do jogador que esta jogando no momento.
    _posicaoJogadorDaVez = None
    # Cabeca da fila que auxiliara a decisao do proximo jogador que ira jogar.
    _cabecaDaFila = None

    _cartasTerritorioDoBaralho = []
    _cartasTerritorioDescartadas = []

    _jogadorDaVezConquistouTerritorio = False

    _numeroDaTroca = 1
    
    def __init__(self, gerenciador, clientes, jogadores):
        self.gerenciador = gerenciador
        
        self.id = 1
        self._turno = Turno()

        self._clientes = clientes
        self._jogadores = jogadores

        self._olheiros = {}

        self._ordemJogadores = self._jogadores.keys()
        random.seed()

    def inicia(self):
        self.iniciaFaseI()
        self.iniciaTurnos()

    def iniciaFaseI(self):
        jogadorQueComeca = self.faseI_DefinirQuemComeca()
        territoriosDosJogadores = self.faseI_DistribuirTerritorios()
        cartasObjetivos = self.faseI_DefinirObjetivos()
        
        self.enviaMsgParaTodos(TipoMensagem.jogo_fase_I, JogoFaseI(jogadorQueComeca, territoriosDosJogadores))

        # NOTA: A carta objetivo deve ser enviada apenas ao jogador.
        for i in range(len(self._jogadores)):
            jsonMsg = json.dumps(Mensagem(
                TipoMensagem.carta_objetivo,
                CartaObjetivo(cartasObjetivos[i])), default=lambda o: o.__dict__)
            print "# ", jsonMsg
            posicaoJogador = self._ordemJogadores[i]
            self._clientes[posicaoJogador].sendMessage(jsonMsg)

    def faseI_DefinirQuemComeca(self):
        self._cabecaDaFila = random.randrange(len(self._jogadores))
        self._indiceOrdemJogadores = self._cabecaDaFila
        self._posicaoJogadorDaVez = self._ordemJogadores[self._cabecaDaFila]
        
        return self._posicaoJogadorDaVez

    def faseI_DistribuirTerritorios(self):
        territorios = list(CodigoTerritorio.Lista)
        random.shuffle(territorios)
        random.shuffle(territorios)
        random.shuffle(territorios)

        listaTerritoriosPorJogador = []
        incremento = []
        
        # Calculando incremento.
        quantidadeDeJogadores = len(self._jogadores)
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

            self._jogadores[self._posicaoJogadorDaVez].iniciaTerritorios(territoriosJogador_i)
            listaTerritoriosPorJogador.append(
                    TerritoriosPorJogador(self._posicaoJogadorDaVez, self._jogadores[self._posicaoJogadorDaVez].territorios))
            
            inicio = inicio + incremento[i]
            self.passaParaProximoJogador(False);

        return listaTerritoriosPorJogador

    def faseI_DefinirObjetivos(self):
        objetivos = range(0, 14)
        random.shuffle(objetivos)
        random.shuffle(objetivos)
        random.shuffle(objetivos)

        objetivoPorJogadores = []
        for i in range(len(self._jogadores)):
            posicaoJogador = self._ordemJogadores[i]
            self._jogadores[posicaoJogador].objetivo = objetivos[i]
            objetivoPorJogadores.append(objetivos[i])

        return objetivoPorJogadores
    
    def iniciaTurnos(self):
        self._cartasTerritorioDoBaralho = list(CartasTerritorio.Todas())
        random.shuffle(self._cartasTerritorioDoBaralho)
        random.shuffle(self._cartasTerritorioDoBaralho)
        random.shuffle(self._cartasTerritorioDoBaralho)
        self._cartasTerritorioDescartadas = []
        
        self._numeroDaTroca = 1

        acaoDoTurno = self.criaAcaoDoTurno(self._turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

    def criaAcaoDoTurno(self, turno):
        # Qual o turno que esta: 1, 2, 3, ...
        numeroDoTurno = turno.numero
        # Quem esta jogando: posicao do jogador...
        jogadorDaVez = self._posicaoJogadorDaVez
        # Qual a acao que ele deve fazer...
        tipoAcaoDoTurno = turno.tipoAcao
        
        jogador = self._jogadores[jogadorDaVez]

        acao = None
        # Preencher os dados da acao
        if tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_globais:
            if turno.quantidadeDeTropas == 0:
                turno.quantidadeDeTropas = math.floor(len(jogador.territorios) / 2);
            acao = AcaoDistribuirTropasGlobais(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, turno.quantidadeDeTropas)
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            turno.grupoTerritorioAtual = turno.gruposTerritorio.pop(0)
            if turno.quantidadeDeTropas == 0:
                turno.quantidadeDeTropas = GrupoTerritorio.BonusPorGrupo[turno.grupoTerritorioAtual]
            acao = AcaoDistribuirTropasGrupoTerritorio(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, 
                turno.quantidadeDeTropas, turno.grupoTerritorioAtual)
        elif tipoAcaoDoTurno == TipoAcaoTurno.trocar_cartas:
            acao = AcaoTrocarCartas(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, (len(jogador.cartasTerritorio) >= 5))
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            acao = AcaoDistribuirTropasTrocaDeCartas(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, turno.quantidadeDeTropas)
        elif tipoAcaoDoTurno == TipoAcaoTurno.jogo_terminou:
            acao = AcaoJogoTerminou(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, jogador.objetivo, jogador.usuario)
        else:
            acao = AcaoTurno(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez)

        return acao
 
    def todosJogaram(self):
        return self._cabecaDaFila == self._indiceOrdemJogadores

    def passaParaProximoJogador(self, comVerificacaoExtra = True):
        # Verifica se o jogador ainda esta no jogo. Caso nao esteja, pula a vez dele.
        ok = False
        for i in range(len(self._ordemJogadores)):
            self._indiceOrdemJogadores = (self._indiceOrdemJogadores + 1) % len(self._ordemJogadores)
            self._posicaoJogadorDaVez = self._ordemJogadores[self._indiceOrdemJogadores]
            self._jogadorDaVezConquistouTerritorio = False
            
            # Verifica se o jogador esta logado na sala e nao foi destruido.
            if self._posicaoJogadorDaVez in self._clientes.keys():
                if not comVerificacaoExtra:
                    ok = True
                    break
                elif len(self._jogadores[self._posicaoJogadorDaVez].territorios) > 0:
                    ok = True
                    break

        if not ok:
            # TODO: O que fazer quando ninguen estiver conectado no jogo?
            print "Ninguem esta mais conectado no jogo... O que fazer?"

    def finalizaTurno_1(self):
        turno = self._turno
        
        if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais and turno.quantidadeDeTropas == 0:
            jogador = self._jogadores[self._posicaoJogadorDaVez]
            if len(jogador.gruposTerritorio()) > 0:
                turno.gruposTerritorio = list(jogador.gruposTerritorio())
                turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
            else:
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

            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio and turno.quantidadeDeTropas == 0:
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

            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            
    def finalizaTurno_2(self):
        turno = self._turno

        if turno.tipoAcao == TipoAcaoTurno.atacar:
            turno.numero = 2
            turno.tipoAcao = TipoAcaoTurno.mover
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

            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            
    def finalizaTurno_I(self):
        turno = self._turno
        erro = True

        if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais:
            if turno.quantidadeDeTropas == 0:
                jogador = self._jogadores[self._posicaoJogadorDaVez]
                if len(jogador.gruposTerritorio()) > 0:
                    turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
                    turno.gruposTerritorio = list(jogador.gruposTerritorio())
                elif len(jogador.cartasTerritorio) > 2:
                    turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    turno.tipoAcao = TipoAcaoTurno.atacar
                    
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            if turno.quantidadeDeTropas == 0:
                jogador = self._jogadores[self._posicaoJogadorDaVez]
                if len(turno.gruposTerritorio) == 0:
                    if len(jogador.cartasTerritorio) > 2:
                        turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                    else:
                        turno.tipoAcao = TipoAcaoTurno.atacar

                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            if turno.quantidadeDeTropas == 0:
                jogador = self._jogadores[self._posicaoJogadorDaVez]
                if len(jogador.cartasTerritorio) > 2:
                    turno.tipoAcao = TipoAcaoTurno.trocar_cartas
                else:
                    turno.tipoAcao = TipoAcaoTurno.atacar
                
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.trocar_cartas:
            jogador = self._jogadores[self._posicaoJogadorDaVez]
            if len(jogador.cartasTerritorio) < 5:
                turno.tipoAcao = TipoAcaoTurno.atacar
                
                acaoDoTurno = self.criaAcaoDoTurno(turno)
                self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                erro = False

        elif turno.tipoAcao == TipoAcaoTurno.atacar:
            turno.tipoAcao = TipoAcaoTurno.mover
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
            
            acaoDoTurno = self.criaAcaoDoTurno(turno)
            self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
            erro = False
            
        if erro:
            socket = self._clientes[self._posicaoJogadorDaVez]
            jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            socket.sendMessage(jsonMsg)

    def finalizaTurno(self, usuario):
        posicaoJogador = -1
        for k, v in self._jogadores.iteritems():
            if v.usuario == usuario:
                posicaoJogador = k

        if posicaoJogador == self._posicaoJogadorDaVez:
            if self._turno.numero == 1:
                self.finalizaTurno_1()
            elif self._turno.numero == 2:
                self.finalizaTurno_2()
            else:
                self.finalizaTurno_I()
    
    def finalizaTurno_moverAposConquistarTerritorio(self):
        self._turno.reiniciarVariaveisExtras()
        self._turno.tipoAcao = TipoAcaoTurno.atacar
        acaoDoTurno = self.criaAcaoDoTurno(self._turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
        
    def colocaTropaReq(self, usuario, codigoTerritorio, quantidade):
        turno = self._turno
        jogador = self._jogadores[self._posicaoJogadorDaVez]
        
        erro = True
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais or \
                turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
                if quantidade <= turno.quantidadeDeTropas and jogador.temTerritorio(codigoTerritorio):
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(self._posicaoJogadorDaVez, territorio, quantidadeTotalRestante))
                    erro = False
            elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
                if quantidade <= turno.quantidadeDeTropas and \
                    jogador.temTerritorio(codigoTerritorio) and \
                    codigoTerritorio in GrupoTerritorio.Dicionario[turno.grupoTerritorioAtual]:
                    
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(self._posicaoJogadorDaVez, territorio, quantidadeTotalRestante))
                    erro = False

    def colocaTropaNaTrocaDeCartasTerritorios(self, posicaoJogador, cartasParaTroca):
        territoriosBeneficiados = []
        jogador = self._jogadores[posicaoJogador]
    
        # Verifica se o jogador tem os territorios das cartas, se tiver, adiciona duas tropas nele.
        for carta in cartasParaTroca:
            if jogador.temTerritorio(carta.codigoTerritorio):
                territorio = jogador.adicionaTropasNoTerritorio(carta.codigoTerritorio, 2)
                territoriosBeneficiados.append(territorio);
                
        self.enviaMsgParaTodos(TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios, 
            ColocarTropaNaTrocaDeCartasTerritorios(posicaoJogador, territoriosBeneficiados))
    
    def ataca(self, usuario, dosTerritorios, paraOTerritorio):
        turno = self._turno
        posicaoJogador = self._posicaoJogadorDaVez
        jogador = self._jogadores[posicaoJogador]
        socket = self._clientes[posicaoJogador]
        
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.atacar:
                if jogador.temOsTerritorios(dosTerritorios) and not jogador.temTerritorio(paraOTerritorio):
                    temErro = False
                
                    # Recuperando territorio da defesa.
                    #   - Identifica o jogador que esta sendo atacado;
                    #   - Identifica o territorio que esta sendo atacado;
                    #   - Pega a quantidade de tropas desse territorio.
                    for k, v in self._jogadores.iteritems():
                        if v.temTerritorio(paraOTerritorio):
                            jogadorDefesa = v
                            territorioDaDefesa = jogadorDefesa.seuTerritorio(paraOTerritorio)
                            quantidadeDadosDefesa = territorioDaDefesa.QuantidadeDeTropas
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
                            if (territorioObj.QuantidadeDeTropas > 1 and 
                                FronteiraTerritorio.TemFronteira(
                                    territorioDaDefesa.Codigo, territorioObj.Codigo)):
                                territoriosDoAtaque.append(territorioObj)
                                
                                if territorioObj.QuantidadeDeTropas > 3:
                                    quantidadeDadosAtaque += territorioObj.QuantidadeDeTropas
                                elif territorioObj.QuantidadeDeTropas > 1:
                                    quantidadeDadosAtaque += territorioObj.QuantidadeDeTropas - 1
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
                                                territorioDaDefesa.Codigo, 1)

                                        # Verifica se o territorio foi conquistado.
                                        if territorioDaDefesa.QuantidadeDeTropas == 0:
                                            jogadorDefesa.territorios.remove(territorioDaDefesa)
                                            jogador.territorios.append(territorioDaDefesa)

                                            # Movendo uma tropa para o territorio conquistado.
                                            territorioDaDefesa = jogador.adicionaTropasNoTerritorio(
                                                    territorioDaDefesa.Codigo, 1)

                                            for t in territoriosDoAtaque:
                                                if t.QuantidadeDeTropas > 1:
                                                    jogador.removeTropasNoTerritorio(t.Codigo, 1)
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
                                                self._clientes[jogador.posicao].sendMessage(jsonMsg)
                                                
                                                # Envia para todos que o jogador foi destruido.
                                                self.enviaMsgParaTodos(TipoMensagem.jogador_destruido,
                                                    JogadorDestruido(jogadorDefesa))

                                            self._jogadorDaVezConquistouTerritorio = True
                                            turno.tipoAcao = TipoAcaoTurno.mover_apos_conquistar_territorio
                                            turno.tropasParaMoverAposAtaque = 0
                                            turno.territoriosDoAtaqueDaConquista = []
                                            for t in territoriosDoAtaque:
                                                if t.QuantidadeDeTropas > 1:
                                                    turno.territoriosDoAtaqueDaConquista.append(t.Codigo)
                                                    turno.tropasParaMoverAposAtaque += t.QuantidadeDeTropas
                                                    if turno.tropasParaMoverAposAtaque > 2:
                                                        turno.tropasParaMoverAposAtaque = 2
                                            turno.territorioConquistado = territorioDaDefesa.Codigo
                                            break

                                    else:
                                        # Defesa venceu.
                                        self.defesaVenceu(i, territoriosDoAtaque, jogador)
                        
                            self.enviaMsgParaTodos(TipoMensagem.atacar, 
                                Atacar(posicaoJogador, dadosDefesa, dadosAtaque, 
                                    territorioDaDefesa, territoriosDoAtaque, conquistouTerritorio))
                    else:
                        temErro = True
                
                    if temErro:
                        jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                        print "# " + jsonMsg
                        socket.sendMessage(jsonMsg)
                    
    def defesaVenceu(self, i, territoriosDoAtaque, jogador):
        pos = i
        while pos >= 0:
            if pos < len(territoriosDoAtaque) and territoriosDoAtaque[pos].QuantidadeDeTropas > 1:
                territoriosDoAtaque[pos] = jogador.removeTropasNoTerritorio(
                    territoriosDoAtaque[pos].Codigo,
                    1)
                break
            pos -= 1
        
    def move(self, usuario, doTerritorio, paraOTerritorio, quantidade):
        turno = self._turno
        posicaoJogador = self._posicaoJogadorDaVez
        jogador = self._jogadores[posicaoJogador]
        socket = self._clientes[posicaoJogador]
        
        if jogador.usuario == usuario:
            if turno.tipoAcao == TipoAcaoTurno.mover:
                if jogador.temTerritorio(doTerritorio) and jogador.temTerritorio(paraOTerritorio) and \
                    FronteiraTerritorio.TemFronteira(doTerritorio, paraOTerritorio):
                    doTerritorioObj = jogador.seuTerritorio(doTerritorio)
                    paraOTerritorioObj = jogador.seuTerritorio(paraOTerritorio)
                    
                    if doTerritorioObj.QuantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.Codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.Codigo, quantidade)
                        
                        self.enviaMsgParaTodos(TipoMensagem.mover, Mover(posicaoJogador, doTerritorioObj, paraOTerritorioObj))
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
                    
                    if doTerritorioObj.QuantidadeDeTropas > quantidade:
                        jogador.removeTropasNoTerritorio(doTerritorioObj.Codigo, quantidade)
                        jogador.adicionaTropasNoTerritorio(paraOTerritorioObj.Codigo, quantidade)
                        
                        turno.tropasParaMoverAposAtaque -= 1
                        self.enviaMsgParaTodos(TipoMensagem.mover, Mover(posicaoJogador, doTerritorioObj, paraOTerritorioObj))
                        
                        # Se nao tiver mais tropas para mover, finaliza o turno.
                        if turno.tropasParaMoverAposAtaque == 0:
                            self.finalizaTurno_moverAposConquistarTerritorio()
                    else:
                        jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                        print "# " + jsonMsg
                        socket.sendMessage(jsonMsg)
                else:
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    socket.sendMessage(jsonMsg)
    
    def trocaCartasTerritorio(self, usuario, cartasTerritorio):
        turno = self._turno
        posicaoJogador = self._posicaoJogadorDaVez
        jogador = self._jogadores[posicaoJogador]
        socket = self._clientes[posicaoJogador]

        if turno.tipoAcao == TipoAcaoTurno.trocar_cartas and \
            jogador.usuario == usuario and \
            len(cartasTerritorio) == 3:
            
            jogador = self._jogadores[posicaoJogador]
            
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
                    turno.quantidadeDeTropas = self.calculaQuantidadeDeTropasDaTroca(self._numeroDaTroca)
                    self._numeroDaTroca += 1
                    turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_troca_de_cartas
                    acaoDoTurno = self.criaAcaoDoTurno(turno)
                    self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
                
                    self.colocaTropaNaTrocaDeCartasTerritorios(posicaoJogador, cartasParaTroca)

                    # Remove e envia ao jogador suas cartas de territorios atualizadas.
                    for carta in cartasParaTroca:
                        jogador.removeCartaTerritorio(carta)
                        self._cartasTerritorioDescartadas.append(carta);
                    jsonMsg = json.dumps(Mensagem(TipoMensagem.cartas_territorio, jogador.cartasTerritorio), default=lambda o: o.__dict__)
                    print "# " + jsonMsg
                    self._clientes[self._posicaoJogadorDaVez].sendMessage(jsonMsg)
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
        if len(self._cartasTerritorioDoBaralho) == 0:
            self._cartasTerritorioDoBaralho = list(self._cartasTerritorioDescartadas)
            random.shuffle(self._cartasTerritorioDoBaralho)
            random.shuffle(self._cartasTerritorioDoBaralho)
            random.shuffle(self._cartasTerritorioDoBaralho)
            self._cartasTerritorioDescartadas = []

        return self._cartasTerritorioDoBaralho.pop(0)

    def enviaCartaTerritorioSeJogadorDaVezConquistouTerritorio(self):
        if self._jogadorDaVezConquistouTerritorio:
            jogador = self._jogadores[self._posicaoJogadorDaVez]
            cartaTerritorio = self.pegaUmaCartaTerritorioDoBaralho()
            jogador.adicionaCartaTerritorio(cartaTerritorio)
            
            jsonMsg = json.dumps(Mensagem(TipoMensagem.cartas_territorio, jogador.cartasTerritorio), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            self._clientes[self._posicaoJogadorDaVez].sendMessage(jsonMsg)

            self._jogadorDaVezConquistouTerritorio = False

    def adiciona(self, cliente, usuario):
        listaJogadoresInfoCurta = []
        territoriosDosJogadores = []

        # Prepara as informacoes.
        for j in self._jogadores.values():
            # Verifica se o jogador ainda esta conectado.
            if j.posicao in self._clientes.keys():
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
        for k, v in self._jogadores.iteritems():
            if v != None and v.usuario == usuario:
                # Jogador reconectou!
                posicao = k
                olheiro = False
                self._clientes[k] = cliente

                listaJogadoresInfoCurta = []
                territoriosDosJogadores = []

                # Enviar lista dos jogadores
                for j in self._jogadores.values():
                    # Verifica se o jogador ainda esta conectado.
                    if j.posicao in self._clientes.keys():
                        listaJogadoresInfoCurta.append({
                            "usuario": j.usuario,
                            "posicao": j.posicao,
                        })
                    
                    territoriosDosJogadores.append({
                        "territorios": j.territorios,
                        "posicao": j.posicao
                    })

                self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo, EntrouNoJogo(usuario, posicao))

                jogador = self._jogadores[posicao];
                self.enviaMsgParaCliente(TipoMensagem.carrega_jogo, 
                    CarregaJogo(self._posicaoJogadorDaVez, 
                        territoriosDosJogadores, 
                        listaJogadoresInfoCurta,
                        jogador.objetivo,
                        jogador.cartasTerritorio),
                    cliente)
                
                acaoDoTurno = self.criaAcaoDoTurno(self._turno)
                self.enviaMsgParaCliente(TipoMensagem.turno, acaoDoTurno, cliente)
                
                break

        if olheiro:
            self._olheiros[usuario] = cliente
            self.enviaMsgParaTodos(TipoMensagem.entrou_no_jogo, EntrouNoJogo(usuario, 7))
            
            self.enviaMsgParaCliente(TipoMensagem.carrega_jogo_olheiro, 
                CarregaJogoOlheiro(self._posicaoJogadorDaVez, 
                    territoriosDosJogadores, 
                    listaJogadoresInfoCurta),
                cliente)
                
            acaoDoTurno = self.criaAcaoDoTurno(self._turno)
            self.enviaMsgParaCliente(TipoMensagem.turno, acaoDoTurno, cliente)
        
    def remove(self, usuario):
        if usuario in self._olheiros.keys():
            self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, 7))
            del self._olheiros[usuario]
        else:
            for k, v in self._jogadores.iteritems():
                if v.usuario == usuario:
                    self.enviaMsgParaTodos(TipoMensagem.saiu_do_jogo, SaiuDoJogo(usuario, k))
                    del self._clientes[k]
                    break

    def temUmVencedor(self):
        jogador = self._jogadores[self._posicaoJogadorDaVez]
        objetivo = FabricaObjetivo().cria(jogador.objetivo)
        return objetivo.completou(jogador, self._jogadores)

    def temJogadorOnLine(self):
        return len(self._clientes) > 0
        
    def msgChat(self, usuario, texto):
        self.enviaMsgParaTodos(TipoMensagem.msg_chat_jogo, MsgChatJogo(usuario, texto))

    def enviaMsgParaCliente(self, tipoMensagem, params, cliente):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        print "# " + jsonMsg
        cliente.sendMessage(jsonMsg)

    def enviaMsgParaTodos(self, tipoMensagem, params):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        for socket in self._clientes.values():
            socket.sendMessage(jsonMsg)
        for socket in self._olheiros.values():
            socket.sendMessage(jsonMsg)
        print "# ", jsonMsg

    def __del__(self):
        self.enviaMsgParaTodos(TipoMensagem.jogo_interrompido, JogoInterrompido(self.id))
