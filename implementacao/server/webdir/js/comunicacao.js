// --------------------------------------------------------------------------------
// Mensagens que são enviadas para o servidor.
// --------------------------------------------------------------------------------
function comunicacao_colocarTropa(posicaoJogador, codigoTerritorio, qtd) {
    var colocarTropaMsg = new Mensagem(TipoMensagem.colocar_tropa,
    {
        posicaoJogador: posicaoJogador,
        territorio: codigoTerritorio,
        quantidade: qtd
    });

    return colocarTropaMsg;
}
