// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    var listaJogadores = msgParams.listaJogadores;
    var sala = msgParams.sala;
    
    if (typeof msgParams.extra != 'undefined') {
        var extra = msgParams.extra;
        if (extra.entrou_ou_saiu == 1) {
            entrouNaSala(msgParams.sala, extra.jogador);
        } else {
            saiuDaSala(msgParams.sala, extra.jogador);
        }
    }
 
    $('#btnIniciarPartida' + sala).css('visibility', 'hidden');
    for (i=0; i < listaJogadores.length; i++) {
        if (listaJogadores[i] != null) {
            var jog = listaJogadores[i];
            var posicaoJogador = Number(jog.posicao);
            var usuario = jog.usuario;
            sala_preencheJogador(sala, posicaoJogador, usuario);

            if (jog.dono && _usuario == usuario) {
                $('#btnIniciarPartida' + sala).css('visibility', 'visible');
                console.log('Novo dono['+usuario+'] na sala['+sala+']');
            }
        }
    }
    
    if (_salaDoJogador == sala)
        _quantidadeDeJogadoresNaSala = listaJogadores.length;
}

function entrouNaSala(sala, jogadorDaSala) {
    this.tocarSom(this, "entrou.mp3");

    if (_usuario == jogadorDaSala.usuario) {
        _salaDoJogador = sala;
        _posicaoJogador = Number(jogadorDaSala.posicao);
        $('#sc_bloqueador' + sala).css('visibility', 'hidden');
    }
}

function saiuDaSala(sala, jogadorDaSala) {
    this.tocarSom(this, "saindo.wav");
    
    sala_limpaPosicao(sala, Number(jogadorDaSala.posicao));

    if (_usuario == jogadorDaSala.usuario) {
        _posicaoJogador = -1;
        _salaDoJogador = null;
        $('#sc_bloqueador' + sala).css('visibility', 'visible');
    }    
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    this.tocarSom(this, "entrou.mp3");

    var posicaoAntigaJogador = Number(msgParams.posicaoAntiga);
    sala_limpaPosicao(msgParams.sala, posicaoAntigaJogador);
    
    var usuario = msgParams.jogadorDaSala.usuario;
    var novaPosicaoJogador = Number(msgParams.jogadorDaSala.posicao);
    sala_preencheJogador(msgParams.sala, novaPosicaoJogador, usuario);
    
    if (_posicaoJogador == msgParams.posicaoAntiga) {
        _posicaoJogador = Number(msgParams.jogadorDaSala.posicao);
    }
}

function processarMsg_lobby(msgParams) {
    for (iSala = 0; iSala < msgParams.salas.length; iSala++) { 
        var sala = msgParams.salas[iSala].sala
        var jogadores =  msgParams.salas[iSala].jogadores;
        var estado = msgParams.salas[iSala].estado;
        $('#btnEntrarNaSala' + sala).html((estado == 'sala_criada') ? 'Entrar' : 'Assistir');
        for (i=0; i < jogadores.length; i++) {
            if (jogadores[i] != null) {
                var jog = jogadores[i];
                var posicaoJogador = Number(jog.posicao);
                var usuario = jog.usuario;
                sala_preencheJogador(sala, posicaoJogador, usuario);
            }
        }
    }
}

/* Funções gerais */
function sala_limpaPosicao(sala, posicao) {
    $("#jogador" + (posicao+1)).html("");
    $("#sala" + sala + "_jogador" + (posicao+1)).html("");
}

function sala_preencheJogador(sala, posicao, usuario) {
    $("#jogador" + (posicao+1)).html(usuario);
    $("#sala" + sala + "_jogador" + (posicao+1)).html(usuario);
}

function appwar_alteraPosicaoSala(sala, posicao) {
    msg = comunicacao_alteraPosicaoNaSala(sala, posicao);
    _libwebsocket.enviarObjJson(msg);
}
