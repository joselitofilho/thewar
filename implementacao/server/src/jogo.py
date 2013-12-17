import math
import random

from mensagens import *
from turno import *
from tipoAcaoTurno import *
from territorio import * 
from carta import * 

class Jogo(object):
    _turno = None
    _jogadores = {}
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
    
    def __init__(self, jogadores):
        self._turno = Turno()
        self._jogadores = jogadores
        self._ordemJogadores = self._jogadores.keys()
        random.seed()

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
        incremento = len(territorios) / len(self._jogadores)
        for i in range(len(self._jogadores)):
            territoriosJogador_i = []
            inicio = incremento * i
            fim = incremento * (i+1)
            for j in range(inicio, fim):
                territoriosJogador_i.append(territorios[j])

            self._jogadores[i].territorios = territoriosJogador_i
            listaTerritoriosPorJogador.append(
                    TerritoriosPorJogador(self._jogadores.keys()[i], self._jogadores[i].territorios))

        return listaTerritoriosPorJogador

    def faseI_DefinirObjetivos(self):
        objetivos = range(0, 14)
        random.shuffle(objetivos)
        random.shuffle(objetivos)
        random.shuffle(objetivos)

        objetivoPorJogadores = []
        for i in range(len(self._jogadores)):
            self._jogadores[i].objetivo = objetivos[i]
            objetivoPorJogadores.append(objetivos[i])

        return objetivoPorJogadores
    
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
            turno.quantidadeDeTropas = math.floor(len(jogador.territorios) / 2);
            acao = AcaoDistribuirTropasGlobais(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, turno.quantidadeDeTropas)
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
            turno.grupoTerritorioAtual = turno.gruposTerritorio.pop(0)
            turno.quantidadeDeTropas = GrupoTerritorio.BonusPorGrupo[turno.grupoTerritorioAtual]
            acao = AcaoDistribuirTropasGrupoTerritorio(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, 
                turno.quantidadeDeTropas, turno.grupoTerritorioAtual)
        elif tipoAcaoDoTurno == TipoAcaoTurno.trocar_cartas:
            acao = AcaoTrocarCartas(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, (len(jogador.cartasTerritorio) >= 5))
        elif tipoAcaoDoTurno == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
            acao = AcaoDistribuirTropasTrocaDeCartas(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez, turno.quantidadeDeTropas)
        else:
            acao = AcaoTurno(tipoAcaoDoTurno, numeroDoTurno, jogadorDaVez)

        return acao

    def inicia(self):
        self._cartasTerritorioDoBaralho = list(CartasTerritorio.Todas())
        random.shuffle(self._cartasTerritorioDoBaralho)
        random.shuffle(self._cartasTerritorioDoBaralho)
        random.shuffle(self._cartasTerritorioDoBaralho)
        self._cartasTerritorioDescartadas = []
        
        self._numeroDaTroca = 1

        return self.criaAcaoDoTurno(self._turno)

    def todosJogaram(self):
        return self._cabecaDaFila == self._indiceOrdemJogadores

    def passaParaProximoJogador(self):
        self._indiceOrdemJogadores = (self._indiceOrdemJogadores + 1) % len(self._ordemJogadores)
        self._posicaoJogadorDaVez = self._ordemJogadores[self._indiceOrdemJogadores]
        self._jogadorDaVezConquistouTerritorio = False

    def finalizaTurno_1(self):
        turno = self._turno
        
        if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais and turno.quantidadeDeTropas == 0:
            jogador = self._jogadores[self._posicaoJogadorDaVez]
            if len(jogador.gruposTerritorio()) > 0:
                turno.gruposTerritorio = list(jogador.gruposTerritorio())
                turno.tipoAcao = TipoAcaoTurno.distribuir_tropas_grupo_territorio
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

    def finalizaTurno_I(self, socket):
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
            jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            socket.sendMessage(jsonMsg)

    def finalizaTurno(self, socket):
        posicaoJogador = -1
        for k, v in self._jogadores.iteritems():
            if v.socket == socket:
                posicaoJogador = k

        if posicaoJogador == self._posicaoJogadorDaVez:
            if self._turno.numero == 1:
                self.finalizaTurno_1()
            elif self._turno.numero == 2:
                self.finalizaTurno_2()
            else:
                self.finalizaTurno_I(socket)
    
    def finalizaTurno_moverAposConquistarTerritorio(self):
        self._turno.reiniciarVariaveisExtras()
        self._turno.tipoAcao = TipoAcaoTurno.atacar
        acaoDoTurno = self.criaAcaoDoTurno(self._turno)
        self.enviaMsgParaTodos(TipoMensagem.turno, acaoDoTurno)
        
    def colocaTropaReq(self, socket, posicaoJogador, codigoTerritorio, quantidade):
        turno = self._turno
        jogador = self._jogadores[posicaoJogador]
        
        erro = True
        if self._posicaoJogadorDaVez == posicaoJogador and jogador.socket == socket:
            if turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais or \
                turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas:
                if quantidade <= turno.quantidadeDeTropas and jogador.temTerritorio(codigoTerritorio):
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(posicaoJogador, territorio, quantidadeTotalRestante))
                    erro = False
            elif turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio:
                if quantidade <= turno.quantidadeDeTropas and \
                    jogador.temTerritorio(codigoTerritorio) and \
                    codigoTerritorio in GrupoTerritorio.Dicionario[turno.grupoTerritorioAtual]:
                    
                    turno.quantidadeDeTropas -= quantidade
                    territorio = jogador.adicionaTropasNoTerritorio(codigoTerritorio, quantidade)

                    quantidadeTotalRestante = turno.quantidadeDeTropas
    
                    self.enviaMsgParaTodos(TipoMensagem.colocar_tropa, 
                        ColocarTropa(posicaoJogador, territorio, quantidadeTotalRestante))
                    erro = False

        if erro:
            jsonMsg = json.dumps(Mensagem(TipoMensagem.erro, None), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            socket.sendMessage(jsonMsg)
    
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
    
    def ataca(self, socket, posicaoJogador, dosTerritorios, paraOTerritorio):
        turno = self._turno
        jogador = self._jogadores[posicaoJogador]
        
        if self._posicaoJogadorDaVez == posicaoJogador:
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
                                                territorioDaDefesa.Codigo,
                                                1)
                                        # Verifica se o territorio foi conquistado.
                                        if territorioDaDefesa.QuantidadeDeTropas == 0:
                                            jogadorDefesa.territorios.remove(territorioDaDefesa)
                                            jogador.territorios.append(territorioDaDefesa)

                                            conquistouTerritorio = True
                                            self._jogadorDaVezConquistouTerritorio = True
                                            turno.tipoAcao = TipoAcaoTurno.mover_apos_conquistar_territorio
                                            turno.tropasParaMoverAposAtaque = 0
                                            turno.territoriosDoAtaqueDaConquista = []
                                            for t in territoriosDoAtaque:
                                                if t.QuantidadeDeTropas > 1:
                                                    turno.territoriosDoAtaqueDaConquista.append(t.Codigo)
                                                    turno.tropasParaMoverAposAtaque += t.QuantidadeDeTropas
                                                    if turno.tropasParaMoverAposAtaque > 3:
                                                        turno.tropasParaMoverAposAtaque = 3
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
            if pos < len(territoriosDoAtaque):
                territoriosDoAtaque[pos] = jogador.removeTropasNoTerritorio(
                    territoriosDoAtaque[pos].Codigo,
                    1)
                break
            pos -= 1
        
    def move(self, socket, posicaoJogador, doTerritorio, paraOTerritorio, quantidade):
        turno = self._turno
        jogador = self._jogadores[posicaoJogador]
        
        if self._posicaoJogadorDaVez == posicaoJogador:
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
    
    def trocaCartasTerritorio(self, socket, posicaoJogador, cartasTerritorio):
        turno = self._turno
        if turno.tipoAcao == TipoAcaoTurno.trocar_cartas and \
            self._posicaoJogadorDaVez == posicaoJogador and \
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
                    jogador.socket.sendMessage(jsonMsg)
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

    def enviaMsgParaTodos(self, tipoMensagem, params):
        jsonMsg = json.dumps(Mensagem(tipoMensagem, params), default=lambda o: o.__dict__)
        for k, v in self._jogadores.iteritems():
            v.socket.sendMessage(jsonMsg)
        print "# ", jsonMsg

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
            print "Jogador da vez: ", self._posicaoJogadorDaVez
            jogador = self._jogadores[self._posicaoJogadorDaVez]
            cartaTerritorio = self.pegaUmaCartaTerritorioDoBaralho()
            print "Cartas territorios: ", cartaTerritorio
            print "Antes: ",jogador.cartasTerritorio
            jogador.adicionaCartaTerritorio(cartaTerritorio)
            
            jsonMsg = json.dumps(Mensagem(TipoMensagem.cartas_territorio, jogador.cartasTerritorio), default=lambda o: o.__dict__)
            print "# " + jsonMsg
            jogador.socket.sendMessage(jsonMsg)

            self._jogadorDaVezConquistouTerritorio = False
