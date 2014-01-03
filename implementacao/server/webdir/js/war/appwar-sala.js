// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    var listaJogadores = msgParams.listaJogadores;
    
    if (typeof msgParams.extra != 'undefined') {
        var extra = msgParams.extra;
        if (extra.entrou_ou_saiu == 1) {
            entrouNaSala(msgParams.sala, extra.jogador, listaJogadores);
        } else {
            saiuDaSala(msgParams.sala, extra.jogador, listaJogadores);
        }
    }
 
    _quantidadeDeJogadoreNaSala = listaJogadores.length;
}

function entrouNaSala(sala, jogadorDaSala, listaJogadores) {
    this.tocarSom(this, "entrou.mp3");

    if (_posicaoJogador == -1) {
        _posicaoJogador = Number(jogadorDaSala.posicao);
        appwar_alterarTituloDaPagina(jogadorDaSala.usuario);
        if (typeof jogadorDaSala.dono != 'undefined') {
            $('#btnIniciarPartida' + sala).css('visibility', ((jogadorDaSala.dono) ? 'visible' : 'hidden'));
        }
    }
    
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#bloqueador_tela').css('visibility', 'hidden');
    
    $('#sala').css('visibility', 'visible');

    for (i=0; i < listaJogadores.length; i++) {
        if (listaJogadores[i] != null) {
            var posicaoJogador = Number(listaJogadores[i].posicao) + 1;
            var usuario = listaJogadores[i].usuario;
            sala_preencheJogador(posicaoJogador, usuario);
        }
    }
}

function saiuDaSala(sala, jogadorDaSala, listaJogadores) {
    this.tocarSom(this, "saindo.wav");
    
    var posicaoJogador = Number(jogadorDaSala.posicao) + 1;
    sala_limpaPosicao(posicaoJogador);
    
    for (i=0; i < listaJogadores.length; i++) {
        if (listaJogadores[i] != null) {
            var jog = listaJogadores[i];
            var posicaoJogador = Number(jog.posicao) + 1;
            var usuario = jog.usuario;
            sala_preencheJogador(posicaoJogador, usuario);

            if (jog.dono && _posicaoJogador == jog.posicao) {
                $('#btnIniciarPartida' + sala).css('visibility', 'visible');
            }
        }
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
    $("#jogador" + posicao).html("");
    $("#sala1_jogador" + posicao).html("");
}

function sala_preencheJogador(posicao, usuario) {
    $("#jogador" + posicao).html(usuario);
    $("#sala1_jogador" + posicao).html(usuario);
}

function appwar_alteraPosicaoSala(sala, posicao) {
    msg = comunicacao_alteraPosicaoNaSala(posicao);
    _libwebsocket.enviarObjJson(msg);
}
