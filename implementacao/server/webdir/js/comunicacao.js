// --------------------------------------------------------------------------------
// Mensagens que são enviadas para o servidor.
// --------------------------------------------------------------------------------
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
