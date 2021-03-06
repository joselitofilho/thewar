from src.jsonserializer import *
from src.turno import *


class TipoMensagem:
    altera_posicao_na_sala = "AlteraPosicaoNaSala"
    altera_tipo_posicao_na_sala = "AlteraTipoPosicaoNaSala"
    atacar = "Atacar"
    carrega_jogo = "CarregaJogo"
    carrega_jogo_olheiro = "CarregaJogoOlheiro"
    carta_objetivo = "CartaObjetivo"
    cartas_territorio = "CartasTerritorio"
    colocar_tropa = "ColocarTropa"
    colocar_tropa_na_troca_de_cartas_territorios = "ColocarTropaNaTrocaDeCartasTerritorios"
    criar_sala = "CriarSala"
    desafios_em_andamento = "DesafiosEmAndamento"
    doacoes = "Doacoes"
    entrar = "Entrar"
    entrou_no_jogo = "EntrouNoJogo"
    erro = "Erro"
    fechar_sala = "FecharSala"
    finalizar_turno = "FinalizarTurno"
    iniciar_partida = "IniciarPartida"
    info_sala = "InfoSala"
    jogador_destruido = "JogadorDestruido"
    jogo_fase_I = "JogoFaseI"
    jogo_interrompido = "JogoInterrompido"
    lobby = "Lobby"
    mover = "Mover"
    moverAposConquistarTerritorio = "MoverAposConquistarTerritorio"
    msg_chat_geral = "MsgChatGeral"
    msg_chat_jogo = "MsgChatJogo"
    nova_senha = "NovaSenha"
    perfil = "Perfil"
    ranking = "Ranking"
    recuperar_senha = "RecuperarSenha"
    registrar = "Registrar"
    sair_da_sala = "SairDaSala"
    saiu_do_jogo = "SaiuDoJogo"
    trocar_cartas_territorio = "TrocarCartasTerritorio"
    turno = "Turno"
    usuario_conectou = "UsuarioConectou"
    usuario_desconectou = "UsuarioDesconectou"


class Mensagem(JSONSerializer):
    def __init__(self, tipo=None, params=None):
        self.tipo = tipo
        self.params = params


class Lobby(JSONSerializer):
    def __init__(self, salas, usuarios):
        self.salas = salas
        self.usuarios = usuarios


class CriarSala(JSONSerializer):
    def __init__(self, sala):
        self.sala = sala


class InfoSala(JSONSerializer):
    def __init__(self, sala, estado, jogadoresDaSala, extra):
        self.sala = sala
        self.estado = estado
        self.jogadores = jogadoresDaSala
        self.extra = extra


class FecharSala(JSONSerializer):
    def __init__(self, sala):
        self.sala = sala


class AlteraPosicaoNaSala(JSONSerializer):
    def __init__(self, sala, jogadorDaSala, posicaoAntiga):
        self.sala = sala
        self.jogadorDaSala = jogadorDaSala
        self.posicaoAntiga = posicaoAntiga


class TerritoriosPorJogador(JSONSerializer):
    def __init__(self, posicao, territorios):
        self.posicao = posicao
        self.territorios = territorios


class JogoFaseI(JSONSerializer):
    def __init__(self, posicao, territoriosDosJogadores):
        self.jogadorQueComeca = posicao
        self.territoriosDosJogadores = territoriosDosJogadores


class CartaObjetivo(JSONSerializer):
    def __init__(self, objetivo):
        self.objetivo = objetivo


class EntrouNoJogo(JSONSerializer):
    def __init__(self, usuario, posicao, total_territorios, total_cartas_territorio):
        self.usuario = usuario
        self.posicao = posicao
        self.total_territorios = total_territorios
        self.total_cartas_territorio = total_cartas_territorio


class SaiuDoJogo(JSONSerializer):
    def __init__(self, usuario, posicao):
        self.usuario = usuario
        self.posicao = posicao


class CarregaJogo(JSONSerializer):
    def __init__(self, posicao, territoriosDosJogadores, listaJogadores, objetivo, cartasTerritorio):
        self.jogadorDaVez = posicao
        self.territoriosDosJogadores = territoriosDosJogadores
        self.jogadores = listaJogadores
        self.objetivo = objetivo;
        self.cartasTerritorio = cartasTerritorio


class CarregaJogoOlheiro(JSONSerializer):
    def __init__(self, posicao, territoriosDosJogadores, listaJogadores):
        self.jogadorDaVez = posicao
        self.territoriosDosJogadores = territoriosDosJogadores
        self.jogadores = listaJogadores


class AcaoTurno(JSONSerializer):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                 jogadorQueComecou, ordemJogadores):
        self.tipoAcao = tipoAcao
        self.numeroDoTurno = numeroDoTurno
        self.vezDoJogador = infoJogadorDaVez
        self.tempoRestante = tempoRestante
        self.timeoutSemTolerancia = Turno.TIMEOUT_SEM_TOLERANCIA
        self.valorDaTroca = valorDaTroca
        self.infoJogadores = infoJogadores
        self.jogadorQueComecou = jogadorQueComecou
        self.ordemJogadores = ordemJogadores


class AcaoDistribuirTropasGlobais(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, quantidadeDeTropas,
                 territoriosDosJogadores, infoJogadores, jogadorQueComecou, ordemJogadores):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                           jogadorQueComecou, ordemJogadores)
        self.quantidadeDeTropas = quantidadeDeTropas
        self.territoriosDosJogadores = territoriosDosJogadores


class AcaoDistribuirTropasGrupoTerritorio(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, quantidadeDeTropas,
                 grupoTerritorio, infoJogadores, jogadorQueComecou, ordemJogadores):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                           jogadorQueComecou, ordemJogadores)
        self.quantidadeDeTropas = quantidadeDeTropas
        self.grupoTerritorio = grupoTerritorio


class AcaoTrocarCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, obrigatorio,
                 infoJogadores, jogadorQueComecou, ordemJogadores):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                           jogadorQueComecou, ordemJogadores)
        self.obrigatorio = obrigatorio


class AcaoDistribuirTropasTrocaDeCartas(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, quantidadeDeTropas,
                 infoJogadores, jogadorQueComecou, ordemJogadores):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                           jogadorQueComecou, ordemJogadores)
        self.quantidadeDeTropas = quantidadeDeTropas


class AcaoJogoTerminou(AcaoTurno):
    def __init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, objetivo, ganhador,
                 infoJogadores, jogadorQueComecou, ordemJogadores):
        AcaoTurno.__init__(self, tipoAcao, numeroDoTurno, infoJogadorDaVez, tempoRestante, valorDaTroca, infoJogadores,
                           jogadorQueComecou, ordemJogadores)
        self.objetivo = objetivo
        self.ganhador = ganhador


class ColocarTropa(JSONSerializer):
    def __init__(self, jogador, quantidade, territorio, quantidadeDeTropasRestante):
        self.jogador = jogador
        self.quantidade = quantidade
        self.territorio = territorio
        self.quantidadeDeTropasRestante = quantidadeDeTropasRestante


class Atacar(JSONSerializer):
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


class Mover(JSONSerializer):
    def __init__(self, jogador, doTerritorioObj, paraOTerritorioObj, quantidade):
        self.jogador = jogador
        self.doTerritorioObj = doTerritorioObj
        self.paraOTerritorioObj = paraOTerritorioObj
        self.quantidade = quantidade


class Territorios(JSONSerializer):
    def __init__(self, posicaoJogador, territorios):
        self.posicaoJogador = posicaoJogador
        self.territorios = territorios


class ColocarTropaNaTrocaDeCartasTerritorios(JSONSerializer):
    def __init__(self, jogador, territorios):
        self.jogador = jogador;
        self.territorios = territorios


class JogadorDestruido(JSONSerializer):
    def __init__(self, jogador):
        self.jogador = jogador


class JogoInterrompido(JSONSerializer):
    def __init__(self, identificador):
        self.identificador = identificador


class MsgChatJogo(JSONSerializer):
    def __init__(self, jogador, texto, som=None):
        self.jogador = jogador
        self.texto = texto
        self.som = som


class MsgChatGeral(JSONSerializer):
    def __init__(self, usuario, texto, som=None):
        self.usuario = usuario
        self.texto = texto
        self.som = som


class UsuarioConectou(JSONSerializer):
    def __init__(self, usuario):
        self.usuario = usuario


class UsuarioDesconectou(JSONSerializer):
    def __init__(self, usuario):
        self.usuario = usuario
