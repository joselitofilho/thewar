var TipoMensagem = {
    entrar: "Entrar",
    registrar: "Registrar",
    erro: "Erro",
    entrou_na_sala: "EntrouNaSala",
    lista_sala: "ListaSala",
    saiu_da_sala: "SaiuDaSala",
    iniciar_partida: "IniciarPartida",
    jogo_fase_I: "JogoFaseI",
    carta_objetivo: "CartaObjetivo",
    finalizar_turno: "FinalizarTurno",
    colocar_tropa: "ColocarTropa",
    atacar: "Atacar",
    mover: "Mover",
    cartas_territorios: "CartasTerritorio",
    trocar_cartas_territorio: "TrocarCartasTerritorio",
    turno: "Turno",
    colocar_tropa_na_troca_de_cartas_territorios: "ColocarTropaNaTrocaDeCartasTerritorios",
    entrou_no_jogo: "EntrouNoJogo",
    saiu_do_jogo: "SaiuDoJogo",
    carrega_jogo: "CarregaJogo",
    carrega_jogo_olheiro: "CarregaJogoOlheiro"
};

var TipoAcaoTurno = {
    distribuir_tropas_globais: "DistribuirTropasGlobais",
    distribuir_tropas_grupo_territorio: "DistribuirTropasGrupoTerritorio",
    distribuir_tropas_troca_de_cartas: "DistribuirTropasTrocaDeCartas",
    trocar_cartas: "TrocarCartas",
    atacar: "Atacar",
    mover: "Mover",
    mover_apos_conquistar_territorio: "MoverAposConquistarTerritorio",
    jogo_terminou: "JogoTerminou"
};

function Mensagem(tipo, params) {
    this.tipo = tipo;
    this.params = params;
}

