// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    this.tocarSom(this, "entrou.mp3");
    
    var listaJogadores = msgParams.listaJogadores;
    for (i=0; i < listaJogadores.length; i++) {
        if (listaJogadores[i] != null) {
            var posicaoJogador = Number(listaJogadores[i].posicao) + 1;
            var usuario = listaJogadores[i].usuario;
            sala_preencheJogador(posicaoJogador, usuario);
        }
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
    this.tocarSom(this, "saindo.wav");
    
    var posicaoJogador = Number(msgParams.jogadorDaSala.posicao) + 1;
    sala_limpaPosicao(posicaoJogador);
    
    var usuario = msgParams.novoDono.usuario;
    var novoDonoPosicao = Number(msgParams.novoDono.posicao) + 1;
    sala_preencheJogador(novoDonoPosicao, usuario);
    
    if (_posicaoJogador == msgParams.novoDono.posicao) {
        $('#btnIniciarPartida').css('visibility', ((msgParams.novoDono.dono) ? 'visible' : 'hidden'));
    }
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    this.tocarSom(this, "entrou.mp3");

    var posicaoAntigaJogador = Number(msgParams.posicaoAntiga) + 1;
    sala_limpaPosicao(posicaoAntigaJogador);
    
    var usuario = msgParams.jogadorDaSala.usuario;
    var novaPosicaoJogador = Number(msgParams.jogadorDaSala.posicao) + 1;
    sala_preencheJogador(novaPosicaoJogador, usuario);
    
    if (_posicaoJogador == msgParams.posicaoAntiga) {
        _posicaoJogador = Number(msgParams.jogadorDaSala.posicao);
    }
}

/* Funções gerais */
function sala_limpaPosicao(posicao) {
    $("#jogador" + posicao).html("-");
    $("#sala_jogador" + posicao).html("-");
}

function sala_preencheJogador(posicao, usuario) {
    $("#jogador" + posicao).html(usuario);
    $("#sala_jogador" + posicao).html(usuario);
}

function appwar_alteraPosicaoSala(posicao) {
    msg = comunicacao_alteraPosicaoNaSala(posicao);
    _libwebsocket.enviarObjJson(msg);
}
