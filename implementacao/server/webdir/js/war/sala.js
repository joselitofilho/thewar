var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Sala = function () {
    this.nomeValido = function (id) {
        if (id === "") return true;
        if (id.length > 10 ||
            id.indexOf('#') !== -1 ||
            id.indexOf('/') !== -1 ||
            id.indexOf('\\') !== -1 ||
            id.indexOf('@') !== -1 ||
            id.indexOf(' ') !== -1) return false;
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
        if (sala === _salaDoJogador)
            $("#jogador" + (posicao + 1)).html("");
        $("#sala" + sala + "_jogador" + (posicao + 1)).html("-");
    };

    this.limpaSVGsDoJogador = function (sala, posicao) {
        $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_human_svg').removeClass("hidden_player_kind");
        $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_cpu_svg').attr("class", "hidden_player_kind");
        $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_disable_svg').attr("class", "hidden_player_kind");
    };

    this.preencheJogador = function (sala, posicao, usuario, tipo, dono) {
        if (sala === _salaDoJogador) {
            $("#jogador" + (posicao + 1)).html(usuario);
        }
        $("#sala" + sala + "_jogador" + (posicao + 1)).html(usuario);

        if (dono) {
            $('#sala' + sala + '_jogador' + (posicao + 1)).css('text-decoration', 'underline');
        } else {
            $('#sala' + sala + '_jogador' + (posicao + 1)).css('text-decoration', '');
        }

        if (tipo === 'disable') {
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_human_svg').addClass("hidden_player_kind");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_cpu_svg').attr("class", "hidden_player_kind");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_disable_svg').attr("class", "");
        } else if (tipo === 'cpu') {
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_human_svg').addClass("hidden_player_kind");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_cpu_svg').attr("class", "");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_disable_svg').attr("class", "hidden_player_kind");
            $('#sala_' + sala + '_titulo_info').css('display', '');
        } else {
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_human_svg').removeClass("hidden_player_kind");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_cpu_svg').attr("class", "hidden_player_kind");
            $('#sala_' + sala + ' #sala_' + sala + '_jogador' + posicao + '_disable_svg').attr("class", "hidden_player_kind");
        }
    };

    this.sai = function () {
        msg = comunicacao_sairDaSala();
        _libwebsocket.enviarObjJson(msg);
    };

    this.criaElementoHtml = function (id) {
        let html = '';
        html += '<div id="sala_' + id + '" class="sala_box">';
        html += '    <div class="sala_header">';
        html += '        <div class="sala_titulo">#' + id + '&nbsp;<p id="sala_' + id + '_titulo_info">Jogar com o computador reduz a pontuação de vitória.</p></div>';
        html += '        <div class="sala_menu">';
        html += '            <button id="btnIniciarPartida' + id + '" class="btn_iniciar_partida" onclick="iniciarPartida();"></button>';
        // html += '            <button>Pronto</button>';
        html += '            <button id="btnSairDaSala' + id + '" class="btn_sair" onclick="_sala.sai();"></button>';
        html += '            <button id="btnEntrarNaSala' + id + '" class="btn_entrar" onclick="appwar_alteraPosicaoSala(\'' + id + '\', 0);"></button>';
        html += '        </div>';
        html += '    </div>';
        html += '    <div class="sala_content_grid">';
        const cores = ['cor_vermelha', 'cor_azul', 'cor_verde', 'cor_preto', 'cor_branco', 'cor_amarelo'];
        const cores_svg = ['sala_jogador_tipo_humano_branco', 'sala_jogador_tipo_humano_branco', 'sala_jogador_tipo_humano_branco', 'sala_jogador_tipo_humano_branco', 'sala_jogador_tipo_humano_preto', 'sala_jogador_tipo_humano_preto'];
        for (let i = 0; i <= 5; ++i) {
            html += '    <div id="sala_jogador' + i + '" class="sala_jogador_box">';
            html += '        <div class="sala_jogador_tipo ' + cores[i] + '" onclick="sala_alteraTipoJogador(\'' + id + '\',' + i + ');">';
            html += '            <svg viewBox="0 0 24 24" transform="rotate(180)"><path fill="currentColor" d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"/></svg>';
            html += '            <div id="sala_' + id + '_jogador' + i + '_human_svg" class="sala_jogador_tipo_humano ' + cores_svg[i] + '"></div>';
            // html += '            <svg id="sala_' + id + '_jogador' + i + '_human_svg" viewBox="0 0 24 24"><path fill="currentColor" d="M141 353 c-8 -8 -14 -31 -13 -50 1 -28 -4 -37 -28 -51 -40 -23 -55 -53 -41 -80 6 -11 11 -36 11 -56 0 -60 6 -66 71 -66 l59 0 -6 30 c-4 16 -3 41 0 55 5 21 12 25 42 25 24 0 43 8 60 25 14 14 36 28 49 31 39 10 29 24 -17 25 -24 1 -47 0 -53 -1 -5 -2 -25 -5 -44 -8 -32 -4 -33 -3 -27 22 3 14 8 36 12 49 3 14 -2 31 -14 45 -23 26 -41 27 -61 5z"/></svg>';
            html += '            <svg id="sala_' + id + '_jogador' + i + '_cpu_svg" viewBox="0 0 24 24"><path fill="currentColor" d="M4,6H20V16H4M20,18A2,2 0 0,0 22,16V6C22,4.89 21.1,4 20,4H4C2.89,4 2,4.89 2,6V16A2,2 0 0,0 4,18H0V20H24V18H20Z" /></svg>';
            html += '            <svg id="sala_' + id + '_jogador' + i + '_disable_svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,0A12,12 0 0,1 24,12A12,12 0 0,1 12,24A12,12 0 0,1 0,12A12,12 0 0,1 12,0M12,2A10,10 0 0,0 2,12C2,14.4 2.85,16.6 4.26,18.33L18.33,4.26C16.6,2.85 14.4,2 12,2M12,22A10,10 0 0,0 22,12C22,9.6 21.15,7.4 19.74,5.67L5.67,19.74C7.4,21.15 9.6,22 12,22Z" /></svg>';
            html += '            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"/></svg>';
            html += '        </div>';
            html += '        <div id="sala' + id + '_jogador' + (i + 1) + '" class="sala_jogador_box_name" onclick="appwar_alteraPosicaoSala(\'' + id + '\',' + i + ');">-</div>';
            html += '    </div>';
        }
        html += '    </div>';
        html += '    <div id="sc_bloqueador' + id + '" class="sc_bloqueador">';
        html += '</div>';

        return html;
    };

    this.atualizaPontuacao = function (ranking) {
        _listaUsuarios.atualizaPontuacao(ranking);
    };

    this.atualizaDoadores = function (doadores) {
        _listaUsuarios.atualizaDoadores(doadores);
    };

    this.adicionaElementoHtml = function (id) {
        var html = this.criaElementoHtml(id);
        $('#sala_content').append(html);
    };

    this.removeElementoHtml = function (id) {
        $('#sala_' + id).remove();
    };

    this.limpaListaSala = function () {
        $('#sala_content').children().each(function (i, elemento) {
            $(elemento).remove();
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

_listaUsuarios = new jogos.war.ListaUsuarios();

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_info_sala(msgParams) {
    if (msgParams) {
        var listaJogadores = msgParams.jogadores || [];
        var sala = msgParams.sala;
        var estado = msgParams.estado;

        if (typeof msgParams.extra != 'undefined' && msgParams.extra != null) {
            var extra = msgParams.extra;
            if (extra.entrou_ou_saiu === 1) {
                entrouNaSala(msgParams.sala, extra.jogador);
            } else {
                saiuDaSala(msgParams.sala, extra.jogador);
            }
        }

        $('#btnIniciarPartida' + sala).css('visibility', 'hidden');
        _sala.alteraBtnEntrar((estado === 'sala_criada') ? 'entrar' : 'assistir', sala);

        if (listaJogadores.length === 0) {
            for (let i = 0; i <= 5; i++) {
                _sala.limpaPosicao(sala, i);
            }
        }

        for (let i = 0; i <= 5; i++) {
            _sala.limpaSVGsDoJogador(sala, i);
        }

        $('#sala_' + sala + '_titulo_info').css('display', 'none');
        for (let i = 0; i <= 5; i++) {
            if (listaJogadores[i] != null) {
                let jog = listaJogadores[i];
                let posicaoJogador = Number(jog.posicao);
                let usuario = jog.usuario;
                let tipo = jog.tipo;
                _sala.preencheJogador(sala, posicaoJogador, usuario, tipo, jog.dono);

                if (jog.dono && _usuario === usuario && estado === 'sala_criada') {
                    $('#btnIniciarPartida' + sala).css('visibility', 'visible');
                }
            }
        }

        if (_salaDoJogador === sala) {
            let quantidadeHumanos = 0;
            for (let i = 0; i < listaJogadores.length; ++i) {
                if (listaJogadores[i].tipo !== 'disable') {
                    ++quantidadeHumanos;
                }
            }
            _quantidadeDeJogadoresNaSala = quantidadeHumanos;
        }
    }
}

function entrouNaSala(sala, jogadorDaSala) {
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "entrou.mp3");

    if (_usuario === jogadorDaSala.usuario) {
        _salaDoJogador = sala;
        _posicaoJogador = Number(jogadorDaSala.posicao);
        $('#sc_bloqueador' + sala).css('visibility', 'hidden');
        $('#btnSairDaSala' + sala).css('visibility', 'visible');
        $('#btnEntrarNaSala' + sala).css('display', 'none');
    }
}

function saiuDaSala(sala, jogadorDaSala) {
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "saindo.wav");

    _sala.limpaPosicao(sala, Number(jogadorDaSala.posicao));

    if (_usuario === jogadorDaSala.usuario) {
        _posicaoJogador = -1;
        _salaDoJogador = null;
        $('#sc_bloqueador' + sala).css('visibility', 'visible');
        $('#btnSairDaSala' + sala).css('visibility', 'hidden');
        $('#btnEntrarNaSala' + sala).css('display', '');
    }
}

function processarMsg_altera_posicao_na_sala(msgParams) {
    if (msgParams) {
        if (!_jogadorEstaEmJogo) this.tocarSom(this, "entrou.mp3");

        const sala = msgParams.sala;
        const posicaoAntigaJogador = Number(msgParams.posicaoAntiga);
        _sala.limpaPosicao(sala, posicaoAntigaJogador);

        const usuario = msgParams.jogadorDaSala.usuario;
        const novaPosicaoJogador = Number(msgParams.jogadorDaSala.posicao);
        const tipo = msgParams.jogadorDaSala.tipo;
        const dono = msgParams.jogadorDaSala.dono;
        $('#sala' + sala + '_jogador' + (posicaoAntigaJogador + 1)).css('text-decoration', '');
        _sala.preencheJogador(msgParams.sala, novaPosicaoJogador, usuario, tipo, dono);

        if (_posicaoJogador === msgParams.posicaoAntiga) {
            _posicaoJogador = Number(msgParams.jogadorDaSala.posicao);
        }
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
        _sala.alteraBtnEntrar((estado === 'sala_criada') ? 'entrar' : 'assistir', sala);
        $('#btnIniciarPartida' + sala).css('visibility', 'hidden');

        $('#sala_' + sala + '_titulo_info').css('display', 'none');
        for (let i = 0; i <= 5; i++) {
            if (jogadores[i] != null) {
                var jog = jogadores[i];
                var posicaoJogador = Number(jog.posicao);
                var usuario = jog.usuario;
                var tipo = jog.tipo;
                _sala.preencheJogador(sala, posicaoJogador, usuario, tipo, jog.dono);

                if (usuario === _usuario && estado === 'jogo_em_andamento') {
                    _sala.alteraBtnEntrar('reentrar', sala);
                }

                if (jog.dono && _usuario === usuario && estado === 'sala_criada') {
                    $('#btnIniciarPartida' + sala).css('visibility', 'visible');
                }
            } else {
                _sala.limpaSVGsDoJogador(sala, i);
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

function sala_alteraTipoJogador(sala, posicao) {
    msg = comunicacao_alteraTipoPosicaoSala(sala, posicao);
    _libwebsocket.enviarObjJson(msg);
}

/* Chat */
function cg_texto_onkeypress(event) {
    if (event.keyCode === 13) {
        sala_enviaMsgChatGeral();
    }
    return true;
}

function sala_enviaMsgChatGeral() {
    var texto = $('#cg_texto').val();
    sala_enviaMsg(texto);
}

function sala_enviaMsg(texto) {
    if (texto.length > 0) {
        if (texto.length > 0) {
            $('#cg_texto').val('');
            msg = comunicacao_MsgChatGeral(texto);
            _libwebsocket.enviarObjJson(msg);
        }
    }
}
