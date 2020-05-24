var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Sala = function () {
    this.nomeValido = function (id) {
        if (id == "") return false;
        if (id.length > 10 ||
            id.indexOf('#') != -1 ||
            id.indexOf('/') != -1 ||
            id.indexOf('\\') != -1 ||
            id.indexOf('@') != -1 ||
            id.indexOf(' ') != -1) return false;
        return true;
    };

    this.cria = function (id) {
        id = id.trim();
        id = utilRetiraAcento(id);
        if (!this.nomeValido(id))
            jError(
                "Digite um nome adequando para sua sala de no máximo 10 letras.<br/> Não pode conter os caracteres: [#, /, \\, @, espaço]",
                {
                    autoHide: true,
                    clickOverlay: true,
                    MinWidth: 250,
                    TimeShown: 3000,
                    ShowTimeEffect: 200,
                    HideTimeEffect: 200,
                    LongTrip: 20,
                    HorizontalPosition: 'center',
                    VerticalPosition: 'top',
                    ShowOverlay: true,
                    ColorOverlay: '#493625',
                    OpacityOverlay: 0.8
                }
            );
        else {
            msg = comunicacao_criarSala(id);
            _libwebsocket.enviarObjJson(msg);
        }
    };

    this.limpaPosicao = function (sala, posicao) {
        if (sala == _salaDoJogador)
            $("#jogador" + (posicao + 1)).html("");
        $("#sala" + sala + "_jogador" + (posicao + 1)).html("");
    };

    this.preencheJogador = function (sala, posicao, usuario) {
        if (sala == _salaDoJogador)
            $("#jogador" + (posicao + 1)).html(usuario);
        $("#sala" + sala + "_jogador" + (posicao + 1)).html(usuario);
    };

    this.sai = function () {
        msg = comunicacao_sairDaSala();
        _libwebsocket.enviarObjJson(msg);
    };

    this.criaElementoHtml = function (id) {
        var html = "<div id=\"sala_" + id + "\" class=\"box\">";
        html += "<h3 class=\"box-heading\"><span>#" + id + "</span></h3>";
        html += "<div class=\"sala_posicoes\">";
        html += "<ul>";
        html += "<li><div class=\"jogador_sala_vermelho\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 0);\"></div><span id=\"sala" + id + "_jogador1\"></span></li>";
        html += "<li><div class=\"jogador_sala_azul\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 1);\"></div><span id=\"sala" + id + "_jogador2\"></span></li>";
        html += "<li><div class=\"jogador_sala_verde\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 2);\"></div><span id=\"sala" + id + "_jogador3\"></span></li>";
        html += "<li><div class=\"jogador_sala_preto\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 3);\"></div><span id=\"sala" + id + "_jogador4\"></span></li>";
        html += "<li><div class=\"jogador_sala_branco\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 4);\"></div><span id=\"sala" + id + "_jogador5\"></span></li>";
        html += "<li><div class=\"jogador_sala_amarelo\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 5);\"></div><span id=\"sala" + id + "_jogador6\"></span></li>";
        html += "</ul>";
        html += "</div>";
        html += "<button id=\"btnSairDaSala" + id + "\" class=\"btn_sair\" onclick=\"_sala.sai();\"></button>";
        html += "<button id=\"btnIniciarPartida" + id + "\" class=\"btn_iniciar_partida\" onclick=\"iniciarPartida();\"></button>";
        html += "<div id=\"sc_bloqueador" + id + "\" class=\"sc_bloqueador\">";
        html += "<button id=\"btnEntrarNaSala" + id + "\" class=\"btn_entrar\" onclick=\"appwar_alteraPosicaoSala(\'" + id + "\', 0);\"></button>";
        html += "</div>";
        html += "</div>";

        return html;
    };

    this.atualizaPontuacao = function(ranking) {
        _listaUsuarios.atualizaPontuacao(ranking);
    };

    this.adicionaElementoHtml = function (id) {
        var html = this.criaElementoHtml(id);
        $('#sala_content').append(html);
    };

    this.removeElementoHtml = function (id) {
        $('#sala_' + id).remove();
    };

    this.limpaListaSala = function () {
        $('#sala_content .box').children().each(function (i, elemento) {
            $(elemento).parent().remove();
        });
    };

    this.alteraBtnEntrar = function (acao, sala) {
        $('#btnEntrarNaSala' + sala).attr('class', 'btn_' + acao);
    };

    this.abreBoxCriarSala = function () {
        $('#sala_boxCriarSala').css('visibility', 'visible');
    };

    this.fechaBoxCriarSala = function () {
        $('#sala_boxCriarSala').css('visibility', 'hidden');
    };
};

_listaUsuarios = new jogos.war.ListaUsuarios($('#lista_usuarios'));

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
    _sala.alteraBtnEntrar((estado == 'sala_criada') ? 'entrar' : 'assistir', sala);

    if (listaJogadores.length == 0) {
        for (i = 0; i < 6; i++) {
            _sala.limpaPosicao(sala, i);
        }
    }

    for (i = 0; i < listaJogadores.length; i++) {
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
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "entrou.mp3");

    if (_usuario == jogadorDaSala.usuario) {
        _salaDoJogador = sala;
        _posicaoJogador = Number(jogadorDaSala.posicao);
        $('#sc_bloqueador' + sala).css('visibility', 'hidden');
        $('#btnSairDaSala' + sala).css('visibility', 'visible');
    }
}

function saiuDaSala(sala, jogadorDaSala) {
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "saindo.wav");

    _sala.limpaPosicao(sala, Number(jogadorDaSala.posicao));

    if (_usuario == jogadorDaSala.usuario) {
        _posicaoJogador = -1;
        _salaDoJogador = null;
        $('#sc_bloqueador' + sala).css('visibility', 'visible');
        $('#btnSairDaSala' + sala).css('visibility', 'hidden');
    }
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "entrou.mp3");

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
    jogo_removeElementosHtml();
    _jogadorEstaEmJogo = false;

    $('#googleads').css('left', '34px');

    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#painelRegistrarOuEntrar .form-signin').css('visibility', 'hidden');
    $('#sala').css('visibility', 'visible');
    $('#sala .form-signin').children().each(function (i, elemento) {
        $(elemento).css('visibility', 'visible');
    });
    _sala.limpaListaSala();
    document.getElementById('geral').style.cursor = 'auto';

    for (iSala = 0; iSala < msgParams.salas.length; iSala++) {
        var sala = msgParams.salas[iSala].sala;
        var jogadores = msgParams.salas[iSala].jogadores;
        var estado = msgParams.salas[iSala].estado;
        _sala.adicionaElementoHtml(sala);
        _sala.alteraBtnEntrar((estado == 'sala_criada') ? 'entrar' : 'assistir', sala);
        $('#btnIniciarPartida' + sala).css('visibility', 'hidden');
        for (i = 0; i < jogadores.length; i++) {
            if (jogadores[i] != null) {
                var jog = jogadores[i];
                var posicaoJogador = Number(jog.posicao);
                var usuario = jog.usuario;
                _sala.preencheJogador(sala, posicaoJogador, usuario);

                if (usuario == _usuario && estado == 'jogo_em_andamento') {
                    _sala.alteraBtnEntrar('reentrar', sala);
                }

                if (jog.dono && _usuario == usuario && estado == 'sala_criada') {
                    $('#btnIniciarPartida' + sala).css('visibility', 'visible');
                }
            }
        }
    }

    _listaUsuarios.carrega(msgParams.usuarios);
}

function processarMsg_criar_sala(msgParams) {
    _sala.adicionaElementoHtml(msgParams.sala);
    if (_salaDoJogador == null) {
        $('#sala_nomeParaCriar').val('');
        $('#sala_content').scrollTop($('#sala_content').prop('scrollHeight'));
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

/* Chat */
function cg_texto_onkeypress(event) {
    if (event.keyCode == 13) {
        jogo_enviaMsgChatGeral();
    }
    return true;
}

function jogo_enviaMsgChatGeral() {
    var texto = $('#cg_texto').val();
    if (texto.length > 0) {
        $('#cg_texto').val('');
        msg = comunicacao_MsgChatGeral(texto);
        _libwebsocket.enviarObjJson(msg);
    }
}
