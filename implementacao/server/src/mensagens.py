import json

class TipoMensagem:
    entrar = "Entrar"
    registrar = "Registrar"
    lobby = "Lobby"
    erro = "Erro"
    criar_sala = "CriarSala"
    info_sala = "InfoSala"
    sair_da_sala = "SairDaSala"
    fechar_sala = "FecharSala"
    iniciar_partida = "IniciarPartida"
    jogo_fase_I = "JogoFaseI"
    carta_objetivo = "CartaObjetivo"
    turno = "Turno"
    finalizar_turno = "FinalizarTurno"
    colocar_tropa = "ColocarTropa"
    atacar = "Atacar"
    mover = "Mover"
    moverAposConquistarTerritorio = "MoverAposConquistarTerritorio"
    cartas_territorio = "CartasTerritorio"
    trocar_cartas_territorio = "TrocarCartasTerritorio"
    colocar_tropa_na_troca_de_cartas_territorios = "ColocarTropaNaTrocaDeCartasTerritorios"
    entrou_no_jogo = "EntrouNoJogo"
    saiu_do_jogo = "SaiuDoJogo"
    carrega_jogo = "CarregaJogo"
    carrega_jogo_olheiro = "CarregaJogoOlheiro"
    altera_posicao_na_sala = "AlteraPosicaoNaSala"
    jogador_destruido = "JogadorDestruido"
    jogo_interrompido = "JogoInterrompido"
    msg_chat_jogo = "MsgChatJogo"
    msg_chat_geral = "MsgChatGeral"
    usuario_conectou = "UsuarioConectou"
    usuario_desconectou = "UsuarioDesconectou"

class Mensagem(object):
    def __init__(self, tipo=None, params=None):
        self.tipo = tipo
        self.params = params

    def fromJson(self, jsonMsg):
        self.__dict__ = json.loads(jsonMsg)

class Lobby(object):
    def __init__(self, salas, usuarios):
        self.salas = salas
        self.usuarios = usuarios

class CriarSala(object):
    def __init__(self, sala):
        self.sala = sala

class InfoSala(object):
    def __init__(self, sala, estado, jogadoresDaSala, extra):
        self.sala = sala
        self.estado = estado
        self.jogadores = jogadoresDaSala
        self.extra = extra
        
class FecharSala(object):
    def __init__(self, sala):
        self.sala = sala

class AlteraPosicaoNaSala(object):
    def __init__(self, sala, jogadorDaSala, posicaoAntiga):
        self.sala = sala
        self.jogadorDaSala = jogadorDaSala
        self.posicaoAntiga = posicaoAntiga

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

class EntrouNoJogo(object):
    def __init__(self, usuario, posicao):
        self.usuario = usuario
        self.posicao = posicao

class SaiuDoJogo(object):
    def __init__(self, usuario, posicao):
        self.usuario = usuario
        self.posicao = posicao

class CarregaJogo(object):
    def __init__(self, posicao, territoriosDosJogadores, listaJogadores, objetivo, cartasTerritorio):
        self.jogadorDaVez = posicao
        self.territoriosDosJogadores = territoriosDosJogadores
        self.jogadores = listaJogadores
        self.objetivo = objetivo;
        self.cartasTerritorio = cartasTerritorio

class CarregaJogoOlheiro(object):
    def __init__(self, posicao, territoriosDosJogadores, listaJogadores):
        self.jogadorDaVez = posicao
        self.territoriosDosJogadores = territoriosDosJogadores
        self.jogadores = listaJogadores

class AcaoTurno(object):
    def __init__(self, tipoAcao, 
            numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca):
        self.tipoAcao = tipoAcao
        self.numeroDoTurno = numeroDoTurno
        self.vezDoJogador = posicaoJogador
        self.tempoRestante = tempoRestante  
        self.valorDaTroca = valorDaTroca

class AcaoDistribuirTropasGlobais(AcaoTurno):
    def __init__(self, tipoAcao, 
            numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca, quantidadeDeTropas):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca)
        self.quantidadeDeTropas = quantidadeDeTropas
        
class AcaoDistribuirTropasGrupoTerritorio(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca, quantidadeDeTropas, grupoTerritorio):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca)
        self.quantidadeDeTropas = quantidadeDeTropas
        self.grupoTerritorio = grupoTerritorio
        
class AcaoTrocarCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca, obrigatorio):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca)
        self.obrigatorio = obrigatorio

class AcaoDistribuirTropasTrocaDeCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca, quantidadeDeTropas):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca)
        self.quantidadeDeTropas = quantidadeDeTropas

class AcaoJogoTerminou(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca, objetivo, usuario):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, posicaoJogador, tempoRestante, valorDaTroca)
        self.objetivo = objetivo
        self.ganhador = usuario

class ColocarTropa(object):
    def __init__(self, jogador, quantidade, territorio, quantidadeDeTropasRestante):
        self.jogador = jogador
        self.quantidade = quantidade
        self.territorio = territorio
        self.quantidadeDeTropasRestante = quantidadeDeTropasRestante
        
class Atacar(object):
    def __init__(self, jogadorAtaque, jogadorDefesa, 
            dadosDefesa, dadosAtaque, 
            territorioDaDefesa, territoriosDoAtaque, 
            conquistouTerritorio):
        self.jogadorAtaque = jogadorAtaque
        self.jogadorDefesa = jogadorDefesa
        self.dadosDefesa = dadosDefesa
        self.dadosAtaque = dadosAtaque
        self.territorioDaDefesa = territorioDaDefesa
        self.territoriosDoAtaque = territoriosDoAtaque
        self.conquistouTerritorio = conquistouTerritorio

class Mover(object):
    def __init__(self, jogador, doTerritorioObj, paraOTerritorioObj, quantidade):
        self.jogador = jogador
        self.doTerritorioObj = doTerritorioObj
        self.paraOTerritorioObj = paraOTerritorioObj
        self.quantidade = quantidade

class Territorios(object):
    def __init__(self, posicaoJogador, territorios):
        self.posicaoJogador = posicaoJogador
        self.territorios = territorios
        
class ColocarTropaNaTrocaDeCartasTerritorios(object):
    def __init__(self, jogador, territorios):
        self.jogador = jogador;
        self.territorios = territorios
        
class JogadorDestruido(object):
    def __init__(self, jogador):
        self.jogador = jogador
        
class JogoInterrompido(object):
    def __init__(self, identificador):
        self.identificador = identificador
        
class MsgChatJogo(object):
    def __init__(self, usuario, texto):
        self.usuario = usuario
        self.texto = texto
        
class MsgChatGeral(object):
    def __init__(self, usuario, texto):
        self.usuario = usuario
        self.texto = texto
        
class UsuarioConectou(object):
    def __init__(self, usuario):
        self.usuario = usuario

class UsuarioDesconectou(object):
    def __init__(self, usuario):
        self.usuario = usuario
