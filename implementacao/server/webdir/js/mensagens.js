var TipoMensagem = {
    entrar: "Entrar",
    registrar: "Registrar",
    recuperar_senha: "RecuperarSenha",
    nova_senha: "NovaSenha",
    ranking: "Ranking",
    desafios_em_andamento: "DesafiosEmAndamento",
    doacoes: "Doacoes",
    lobby: "Lobby",
    erro: "Erro",
    criar_sala: "CriarSala",
    info_sala: "InfoSala",
    sair_da_sala: "SairDaSala",
    fechar_sala: "FecharSala",
    iniciar_partida: "IniciarPartida",
    jogo_fase_I: "JogoFaseI",
    carta_objetivo: "CartaObjetivo",
    finalizar_turno: "FinalizarTurno",
    colocar_tropa: "ColocarTropa",
    atacar: "Atacar",
    mover: "Mover",
    moverAposConquistarTerritorio: "MoverAposConquistarTerritorio",
    cartas_territorios: "CartasTerritorio",
    trocar_cartas_territorio: "TrocarCartasTerritorio",
    turno: "Turno",
    colocar_tropa_na_troca_de_cartas_territorios: "ColocarTropaNaTrocaDeCartasTerritorios",
    entrou_no_jogo: "EntrouNoJogo",
    saiu_do_jogo: "SaiuDoJogo",
    carrega_jogo: "CarregaJogo",
    carrega_jogo_olheiro: "CarregaJogoOlheiro",
    altera_posicao_na_sala: "AlteraPosicaoNaSala",
    altera_tipo_posicao_na_sala: "AlteraTipoPosicaoNaSala",
    msg_chat_jogo: "MsgChatJogo",
    msg_chat_geral: "MsgChatGeral",
    usuario_conectou: "UsuarioConectou",
    usuario_desconectou: "UsuarioDesconectou",
    jogador_destruido: "JogadorDestruido",
    jogo_interrompido: "JogoInterrompido",
    perfil: "Perfil"
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

