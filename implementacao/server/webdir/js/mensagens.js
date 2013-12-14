var TipoMensagem = {
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
    turno: "Turno"
};

var TipoAcaoTurno = {
    distribuir_tropas_globais: "DistribuirTropasGlobais",
    distribuir_tropas_grupo_territorio: "DistribuirTropasGrupoTerritorio",
    atacar: "Atacar",
    mover: "Mover"
};

function Mensagem(tipo, params) {
    this.tipo = tipo;
    this.params = params;
}

