// --------------------------------------------------------------------------------
// Mensagens que são enviadas para o servidor.
// --------------------------------------------------------------------------------
function comunicacao_entrar(usuario, senha) {
    return new Mensagem(TipoMensagem.entrar,
    {
        usuario: usuario,
        senha: senha
    });
}

function comunicacao_registrar(usuario, senha, email) {
    return new Mensagem(TipoMensagem.registrar,
    {
        usuario: usuario,
        senha: senha,
        email: email
    });
}

function comunicacao_criarSala(id) {
    return new Mensagem(TipoMensagem.criar_sala,
    {
        sala: id
    });
}

function comunicacao_sairDaSala() {
    return new Mensagem(TipoMensagem.sair_da_sala, null);
}

function comunicacao_iniciarPartida() {
    return new Mensagem(TipoMensagem.iniciar_partida, null);
}

function comunicacao_finalizarTurno() {
    return new Mensagem(TipoMensagem.finalizar_turno, null);
}

function comunicacao_colocarTropa(posicaoJogador, codigoTerritorio, qtd) {
    return new Mensagem(TipoMensagem.colocar_tropa,
    {
        posicaoJogador: posicaoJogador,
        territorio: codigoTerritorio,
        quantidade: qtd
    });
}

function comunicacao_atacar(posicaoJogador, codigoTerritorioAlvo, codigosTerritoriosAtacante) {
    return new Mensagem(TipoMensagem.atacar,
    {
        posicaoJogador: posicaoJogador,
        dosTerritorios: codigosTerritoriosAtacante,
        paraOTerritorio: codigoTerritorioAlvo
    });
}

function comunicacao_mover(posicaoJogador, doTerritorio, paraOTerritorio, quantidade) {
    return new Mensagem(TipoMensagem.mover,
    {
        posicaoJogador: posicaoJogador,
        doTerritorio: doTerritorio,
        paraOTerritorio: paraOTerritorio,
        quantidade: quantidade
    }); 
}

function comunicacao_moverAposConquistarTerritorio(quantidade) {
    return new Mensagem(TipoMensagem.moverAposConquistarTerritorio,
    {
        quantidade: quantidade
    }); 
}

function comunicacao_trocar_cartas_territorio(posicaoJogador, cartasTerritorios) {
    return new Mensagem(TipoMensagem.trocar_cartas_territorio,
    {
        posicaoJogador: posicaoJogador,
        cartasTerritorios: cartasTerritorios
    });
}

function comunicacao_alteraPosicaoNaSala(sala, posicao) {
    return new Mensagem(TipoMensagem.altera_posicao_na_sala,
    {
        sala: sala,
        novaPosicao: posicao
    });
}

function comunicacao_MsgChatJogo(texto) {
    return new Mensagem(TipoMensagem.msg_chat_jogo,
    {
        texto: texto
    });
}

function comunicacao_MsgChatGeral(texto) {
    return new Mensagem(TipoMensagem.msg_chat_geral,
    {
        texto: texto
    });
}
