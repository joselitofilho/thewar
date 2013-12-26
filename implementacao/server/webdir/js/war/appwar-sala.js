// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    var listaJogadores = msgParams.listaJogadores;
    for (i=0; i < listaJogadores.length; i++) {
        var posicaoJogador = Number(listaJogadores[i].posicao) + 1;
        var usuario = listaJogadores[i].usuario;
        $("#jogador" + posicaoJogador).html(usuario);
        $("#sala_jogador" + posicaoJogador).html(usuario);
    }
    
    _quantidadeDeJogadoreNaSala = listaJogadores.length;
}

function processarMsg_entrou_na_sala(msgParams) {
    var jogadorDaSala = msgParams.jogadorDaSala;
    _posicaoJogador = Number(jogadorDaSala.posicao);

    appwar_alterarTituloDaPagina(jogadorDaSala.usuario);

    if (typeof jogadorDaSala.dono != 'undefined') {
        $('#btnIniciarPartida').css('visibility', ((jogadorDaSala.dono) ? 'visible' : 'hidden'));
    }
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#bloqueador_tela').css('visibility', 'hidden');
    
    $('#sala').css('visibility', 'visible');
}

function processarMsg_saiu_da_sala(msgParams) {
    var posicaoJogador = Number(msgParams.jogadorDaSala.posicao) + 1;
    $("#jogador" + posicaoJogador).html("-");
    $("#sala_jogador" + posicaoJogador).html("-");
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    var posicaoAntigaJogador = Number(msgParams.posicaoAntiga) + 1;
    $("#jogador" + posicaoAntigaJogador).html("-");
    $("#sala_jogador" + posicaoAntigaJogador).html("-");
    
    var usuario = msgParams.jogadorDaSala.usuario;
    var novaPosicaoJogador = Number(msgParams.jogadorDaSala.posicao) + 1;
    $("#jogador" + novaPosicaoJogador).html(usuario);
    $("#sala_jogador" + novaPosicaoJogador).html(usuario);
}

/* Funções gerais */
function appwar_alteraPosicaoSala(posicao) {
    msg = comunicacao_alteraPosicaoNaSala(posicao);
    _libwebsocket.enviarObjJson(msg);
}
