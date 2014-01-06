var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Sala = function() {
    
    this.cria = function(id) {
        msg = comunicacao_criarSala(id);
        _libwebsocket.enviarObjJson(msg);
    };

    this.limpaPosicao = function(sala, posicao) {
        $("#jogador" + (posicao+1)).html("");
        $("#sala" + sala + "_jogador" + (posicao+1)).html("");
    };

    this.preencheJogador = function(sala, posicao, usuario) {
        $("#jogador" + (posicao+1)).html(usuario);
        $("#sala" + sala + "_jogador" + (posicao+1)).html(usuario);
    };

    this.sai = function() {
        msg = comunicacao_sairDaSala();
        _libwebsocket.enviarObjJson(msg);
    };

    this.criaElementoHtml = function(id) {
        var html = "<div id=\"sala_"+id+"\" class=\"form-signin\">";
        html += "<h3 class=\"form-signin-heading\"><span>#"+id+"</span>&nbsp;-&nbsp;Escolha sua cor</h3>";
        html += "<div class=\"sala_posicoes\">";
        html += "<ul>";
        html += "<li><a id=\"sala"+id+"_jogador1\" class=\"jogador_sala_vermelho\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 0);\"></a></li>";
        html += "<li><a id=\"sala"+id+"_jogador2\" class=\"jogador_sala_azul\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 1);\"></a></li>";
        html += "<li><a id=\"sala"+id+"_jogador3\" class=\"jogador_sala_verde\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 2);\"></a></li>";
        html += "<li><a id=\"sala"+id+"_jogador4\" class=\"jogador_sala_preto\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 3);\"></a></li>";
        html += "<li><a id=\"sala"+id+"_jogador5\" class=\"jogador_sala_branco\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 4);\"></a></li>";
        html += "<li><a id=\"sala"+id+"_jogador6\" class=\"jogador_sala_amarelo\" href=\"javascript:void(0)\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 5);\"></a></li>";
        html += "</ul>";
        html += "</div>";
        html += "<button id=\"btnSairDaSala"+id+"\" class=\"btn btn-default\" onclick=\"_sala.sai();\">Sair da sala</button>";
        html += "<button id=\"btnIniciarPartida"+id+"\" class=\"btn btn-default btnIniciarPartida\" onclick=\"iniciarPartida();\">Iniciar partida</button>";
        html += "<div id=\"sc_bloqueador"+id+"\" class=\"sc_bloqueador\">";
        html += "<button id=\"btnEntrarNaSala"+id+"\" class=\"btn btn-default btnEntrarNaSala\" onclick=\"appwar_alteraPosicaoSala(\'"+id+"\', 0);\">Entrar</button>";
        html += "</div>";
        html += "</div>";

        return html;
    };

    this.adicionaElementoHtml = function(id) {
        var html = this.criaElementoHtml(id);
        $('#sala_content').append(html);
    };
    
    this.removeElementoHtml = function(id) {
        $('#sala_' + id).remove();
    };
};

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_info_sala(msgParams) {
    var listaJogadores = msgParams.jogadores;
    var sala = msgParams.sala;
    var estado = msgParams.estado;
    
    if (typeof msgParams.extra != 'undefined' && msgParams.extra != null) {
        var extra = msgParams.extra;
        if (extra.entrou_ou_saiu == 1) {
            entrouNaSala(msgParams.sala, extra.jogador);
        } else {
            saiuDaSala(msgParams.sala, extra.jogador);
        }
    }
 
    $('#btnIniciarPartida' + sala).css('visibility', 'hidden');
    $('#btnEntrarNaSala' + sala).html((estado == 'sala_criada') ? 'Entrar' : 'Assistir');

    if (listaJogadores.length == 0) {
        for (i=0; i<6; i++) {
            _sala.limpaPosicao(sala, i);
        }
    }

    for (i=0; i < listaJogadores.length; i++) {
        if (listaJogadores[i] != null) {
            var jog = listaJogadores[i];
            var posicaoJogador = Number(jog.posicao);
            var usuario = jog.usuario;
            _sala.preencheJogador(sala, posicaoJogador, usuario);

            if (jog.dono && _usuario == usuario && estado == 'sala_criada') {
                $('#btnIniciarPartida' + sala).css('visibility', 'visible');
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
    
    _sala.limpaPosicao(sala, Number(jogadorDaSala.posicao));

    if (_usuario == jogadorDaSala.usuario) {
        _posicaoJogador = -1;
        _salaDoJogador = null;
        $('#sc_bloqueador' + sala).css('visibility', 'visible');
    }    
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    this.tocarSom(this, "entrou.mp3");

    var posicaoAntigaJogador = Number(msgParams.posicaoAntiga);
    _sala.limpaPosicao(msgParams.sala, posicaoAntigaJogador);
    
    var usuario = msgParams.jogadorDaSala.usuario;
    var novaPosicaoJogador = Number(msgParams.jogadorDaSala.posicao);
    _sala.preencheJogador(msgParams.sala, novaPosicaoJogador, usuario);
    
    if (_posicaoJogador == msgParams.posicaoAntiga) {
        _posicaoJogador = Number(msgParams.jogadorDaSala.posicao);
    }
}

function processarMsg_lobby(msgParams) {
    for (iSala = 0; iSala < msgParams.salas.length; iSala++) { 
        var sala = msgParams.salas[iSala].sala
        var jogadores =  msgParams.salas[iSala].jogadores;
        var estado = msgParams.salas[iSala].estado;
        _sala.adicionaElementoHtml(sala);
        $('#btnEntrarNaSala' + sala).html((estado == 'sala_criada') ? 'Entrar' : 'Assistir');
        for (i=0; i < jogadores.length; i++) {
            if (jogadores[i] != null) {
                var jog = jogadores[i];
                var posicaoJogador = Number(jog.posicao);
                var usuario = jog.usuario;
                _sala.preencheJogador(sala, posicaoJogador, usuario);

                if (usuario == _usuario && estado == 'jogo_em_andamento') {
                    $('#btnEntrarNaSala' + sala).html('Reentrar');
                }
            }
        }
    }
}

function processarMsg_criar_sala(msgParams) {
    _sala.adicionaElementoHtml(msgParams.sala);
    if (_salaDoJogador == null) {
        //$('#sala_content').scrollTop($('#sala_content').prop('scrollHeight'));
        //$('#sala_content').perfectScrollbar('update');
    }
}

function processarMsg_fechar_sala(msgParams) {
    _sala.removeElementoHtml(msgParams.sala);
    //$('#sala_content').scrollTop(0);
    //$('#sala_content').perfectScrollbar('update');
}

/* Funções gerais */
function appwar_alteraPosicaoSala(sala, posicao) {
    msg = comunicacao_alteraPosicaoNaSala(sala, posicao);
    _libwebsocket.enviarObjJson(msg);
}
