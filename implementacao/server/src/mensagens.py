import json

class TipoMensagem:
    entrar = "Entrar"
    registrar = "Registrar"
    erro = "Erro"
    entrou_na_sala = "EntrouNaSala"
    lista_sala = "ListaSala"
    saiu_da_sala = "SaiuDaSala"
    iniciar_partida = "IniciarPartida"
    jogo_fase_I = "JogoFaseI"
    carta_objetivo = "CartaObjetivo"
    turno = "Turno"
    finalizar_turno = "FinalizarTurno"
    colocar_tropa = "ColocarTropa"
    atacar = "Atacar"
    mover = "Mover"
    cartas_territorio = "CartasTerritorio"
    trocar_cartas_territorio = "TrocarCartasTerritorio"
    colocar_tropa_na_troca_de_cartas_territorios = "ColocarTropaNaTrocaDeCartasTerritorios"

class Mensagem(object):
    def __init__(self, tipo=None, params=None):
        self.tipo = tipo
        self.params = params

    def fromJson(self, jsonMsg):
        self.__dict__ = json.loads(jsonMsg)

class EntrouNaSala(object):
    def __init__(self, posicao, dono):
        self.posicao = posicao
        self.dono = dono

class ListaSala(object):
    def __init__(self, lista):
        self.lista = lista

class SaiuDaSala(object):
    def __init__(self, posicao):
        self.posicao = posicao

class TerritoriosPorJogador(object):
    def __init__(self, posicao, territorios):
        self.posicao = posicao
        self.territorios = territorios

class JogoFaseI(object):
    def __init__(self, posicao, territoriosDosJogadores):
        self.jogadorQueComeca = posicao
        self.territoriosDosJogadores = territoriosDosJogadores

class CartaObjetivo(object):
    def __init__(self, objetivo):
        self.objetivo = objetivo

class AcaoTurno(object):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador):
        self.tipoAcao = tipoAcao
        self.numeroDoTurno = numeroDoTurno
        self.vezDoJogador = posicaoJogador

class AcaoDistribuirTropasGlobais(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, quantidadeDeTropas):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador)
        self.quantidadeDeTropas = quantidadeDeTropas
        
class AcaoDistribuirTropasGrupoTerritorio(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, quantidadeDeTropas, grupoTerritorio):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador)
        self.quantidadeDeTropas = quantidadeDeTropas
        self.grupoTerritorio = grupoTerritorio
        
class AcaoTrocarCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, obrigatorio):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador)
        self.obrigatorio = obrigatorio

class AcaoDistribuirTropasTrocaDeCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, quantidadeDeTropas):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador)
        self.quantidadeDeTropas = quantidadeDeTropas

class ColocarTropa(object):
    def __init__(self, posicaoJogador, territorio, quantidadeDeTropasRestante):
        self.posicaoJogador = posicaoJogador
        self.territorio = territorio
        self.quantidadeDeTropasRestante = quantidadeDeTropasRestante
        
class Atacar(object):
    def __init__(self, posicaoJogador, dadosDefesa, dadosAtaque, territorioDaDefesa, territoriosDoAtaque, conquistouTerritorio):
        self.posicaoJogador = posicaoJogador
        self.dadosDefesa = dadosDefesa
        self.dadosAtaque = dadosAtaque
        self.territorioDaDefesa = territorioDaDefesa
        self.territoriosDoAtaque = territoriosDoAtaque
        self.conquistouTerritorio = conquistouTerritorio

class Mover(object):
    def __init__(self, posicaoJogador, doTerritorioObj, paraOTerritorioObj):
        self.posicaoJogador = posicaoJogador
        self.doTerritorioObj = doTerritorioObj
        self.paraOTerritorioObj = paraOTerritorioObj

class Territorios(object):
    def __init__(self, posicaoJogador, territorios):
        self.posicaoJogador = posicaoJogador
        self.territorios = territorios
        
class ColocarTropaNaTrocaDeCartasTerritorios(object):
    def __init__(self, posicaoJogador, territorios):
        self.posicaoJogador = posicaoJogador;
        self.territorios = territorios
