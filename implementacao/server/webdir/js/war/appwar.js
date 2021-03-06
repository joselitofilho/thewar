//
// http://soundbible.com/tags-war.html
//

_painelObjetivo = new gpscheck.war.PainelObjetivo(-1);
_painelVitoria = new jogos.war.PainelVitoria();

_usuario = null;
_posicaoJogador = -1;
_jogadorEstaEmJogo = false;
_salaDoJogador = null;
_turno = null;
_posicaoJogadorDaVez = -1;
_infoJogadorDaVezDoTurno = null;

_territorioAlvoAtaque = null;
_territoriosAtacante = [];
_jaPodeAtacar = true;

_territorioConquistado = null;

_territoriosAtacanteAposConquistar = null;

_territorioAlvoMover = null;
_territorioMovimento = null;
_jaPodeMover = true;

_animarDadosReferencia = null;

_cartasTerritoriosSelecionadas = [];

_quantidadeDeJogadoresNaSala = 0;

_tour = new jogos.war.Tour();

_sala = new jogos.war.Sala();
_chatGeral = new jogos.war.ChatGeral($('#cg_mensagens'), $('#cg_botao_ir_para_baixo'));
_chatGeral.boasVindas();

_desafios = new jogos.war.Desafios();

_lastMessage = "";

window.addEventListener('load', function () {
    $('#logo_carregando').css('display', 'none');
});

function appwar_limparVariaveis() {
    _posicaoJogador = -1;
    _jogadorEstaEmJogo = false;
    _salaDoJogador = null;
    _posicaoJogadorDaVez = -1;

    _territorioAlvoAtaque = null;
    _territoriosAtacante = [];
    _jaPodeAtacar = true;

    _territorioConquistado = null;

    _territoriosAtacanteAposConquistar = null;

    _territorioAlvoMover = null;
    _territorioMovimento = null;
    _jaPodeMover = true;

    _animarDadosReferencia = null;

    _cartasTerritoriosSelecionadas = [];

    _quantidadeDeJogadoresNaSala = 0;
}

function exibirAlerta(tipo, msg) {
    $('#alerta').removeClass('alert-info alert-success alert-warning alert-danger');
    $('#alerta').addClass(tipo);
    $('#alerta_texto').html(msg);
    $('#alerta').css('visibility', 'visible');
    $("#alerta")
        .fadeIn('slow')
        .animate({opacity: 1.0}, 2000)
        .fadeOut('slow', function () {
            $(this).hide();
        });
}

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_registrar(msgParams) {
    if (msgParams.status === 1) {
        exibirAlerta('alert-success', 'Registrado com sucesso.');
        appwar_exibirPainelEntrar();
    } else if (msgParams.status === 0) {
        exibirAlerta('alert-info', 'Você já está registrado.');
    } else {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    }
}

function processarMsg_entrar(msgParams) {
    if (msgParams.status === 1) {
        var cookie = new gpscheck.web.Cookie();
        cookie.cria("usuario", $('#inputUsuario').val());
        var senha = CryptoJS.SHA3($('#inputSenha').val());
        senha = base64_encode(senha.toString());

        this.tocarSom(this, "entrou.mp3");
        appwar_alterarTituloDaPagina(msgParams.usuario);
        _usuario = msgParams.usuario;

        appwar_atualizarMenuParaSala();
        $('#conteudo_principal').css('display', '');
        $('#painelRegistrarOuEntrar').css('display', 'none');
        $('#sala').css('visibility', 'visible');
        $('html,body').css('overflow', 'auto');
    } else {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    }
}

function processaMsg_recuperar_senha(msgParams) {
    $('#btn_recuperar_senha i').css('display', 'none');
    $('#btn_recuperar_senha').prop('disabled', false);
    if (msgParams.status === 0) {
        appwar_exibirPainelNovaSenha();
        exibirAlerta('alert-success', 'Verifique o código que foi enviado para o seu email.');
    } else {
        exibirAlerta('alert-danger', 'Verifique se seu email está correto e tente novamente.');
    }
}

function processaMsg_nova_senha(msgParams) {
    $('#btn_alterar_senha i').css('display', 'none');
    $('#btn_alterar_senha').prop('disabled', false);
    if (msgParams.status === 0) {
        appwar_exibirPainelEntrar();
        exibirAlerta('alert-success', 'Senha alterada com sucesso.');
    } else {
        exibirAlerta('alert-danger', 'Verifique se o código está correto e tente novamente.');
    }
}

function appwar_processaMsg_usuario_conectou(msgParams) {
    var usuario = msgParams.usuario;
    _chatGeral.usuarioConectou(usuario.nome);
    _listaUsuarios.adiciona(usuario);
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "entrou.mp3");
}

function appwar_processaMsg_usuario_desconectou(msgParams) {
    var usuario = msgParams.usuario;
    _chatGeral.usuarioDesconectou(usuario);
    _listaUsuarios.remove(usuario);
    if (!_jogadorEstaEmJogo) this.tocarSom(this, "saindo.wav");
}

function processarMsg_erro() {
    _jaPodeAtacar = true;
    _jaPodeMover = true;
}

////////////////////////////////////////////////////////////////////////////////
// Métodos utilizados na biblioteca de WebSocket
////////////////////////////////////////////////////////////////////////////////

function posAberturaSocket(valor) {
    var cookie = new gpscheck.web.Cookie();
    var usuarioCookie = cookie.le("usuario");

    if (usuarioCookie != null) {
        $('#inputUsuario').val(usuarioCookie);
    }

    appwar_exibirPainelEntrar();
    $('#conteudo_principal').css('display', 'none');
    $('#painelRegistrarOuEntrar').css('display', '');
}

function posRecebimentoMensagemServidor(valor) {
    // console.log('[DEBUG]', 'Recebeu MSG ' + valor);
    const jsonMensagem = JSON.parse(valor);
    _lastMsg = jsonMensagem;
    if (jsonMensagem.tipo === TipoMensagem.registrar) {
        processarMsg_registrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.entrar) {
        processarMsg_entrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.recuperar_senha) {
        processaMsg_recuperar_senha(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.nova_senha) {
        processaMsg_nova_senha(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.lobby) {
        processarMsg_lobby(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.criar_sala) {
        processarMsg_criar_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.info_sala) {
        processarMsg_info_sala(jsonMensagem.params);
        _tour.start_creation_room();
    } else if (jsonMensagem.tipo === TipoMensagem.fechar_sala) {
        processarMsg_fechar_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.altera_posicao_na_sala) {
        processarMsg_altera_posicao_na_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.jogo_fase_I) {
        processarMsg_jogo_fase_I(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.carta_objetivo) {
        processarMsg_carta_objetivo(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.colocar_tropa) {
        processarMsg_colocar_tropa(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.turno) {
        processarMsg_turno(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.atacar) {
        processarMsg_atacar(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.mover) {
        processarMsg_mover(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.cartas_territorios) {
        processarMsg_cartas_territorios(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios) {
        processarMsg_colocar_tropa_na_troca_de_cartas_territorios(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.entrou_no_jogo) {
        processarMsg_entrou_no_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.saiu_do_jogo) {
        processarMsg_saiu_do_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.carrega_jogo) {
        processarMsg_carrega_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.carrega_jogo_olheiro) {
        processarMsg_carrega_jogo_olheiro(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.msg_chat_jogo) {
        jogo_processaMsg_msg_chat_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.msg_chat_geral) {
        appwar_processaMsg_msg_chat_geral(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.usuario_conectou) {
        appwar_processaMsg_usuario_conectou(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.usuario_desconectou) {
        appwar_processaMsg_usuario_desconectou(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.jogador_destruido) {
        jogo_processaMsg_jogador_destruido(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.jogo_interrompido) {
        jogo_processaMsg_jogo_interrompido(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.ranking) {
        ranking_processaMsg(jsonMensagem.params);
        _sala.atualizaPontuacao(_ranking);
    } else if (jsonMensagem.tipo === TipoMensagem.doacoes) {
        doacoes_processaMsg(jsonMensagem.params);
        _sala.atualizaDoadores(_doadores);
    } else if (jsonMensagem.tipo === TipoMensagem.desafios_em_andamento) {
        _desafios.processaMsg(jsonMensagem.params);
    } else if (jsonMensagem.tipo === TipoMensagem.erro) {
        processarMsg_erro();
    }
}

function posFechamentoSocket(valor) {
    $('#bloqueador_tela').css('visibility', 'visible');
    $('#conteudo_principal').css('display', 'none');
    $('#painelRegistrarOuEntrar').css('display', 'none');
    $('#botao_recarregar').css('visibility', 'visible');
}

function iniciarPartida() {
    if (_quantidadeDeJogadoresNaSala >= 3) {
        iniciarPartidaMsg = comunicacao_iniciarPartida();
        _libwebsocket.enviarObjJson(iniciarPartidaMsg);
    } else {
        jError(
            'Para iniciar o jogo é preciso pelo menos 3 jogadores na sala.',
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
    }
}

function finalizarTurno() {
    finalizarPartidaMsg = comunicacao_finalizarTurno();
    _libwebsocket.enviarObjJson(finalizarPartidaMsg);
    _sliderMoverTropas.fechar();
}

function atacar() {
    if (_posicaoJogadorDaVez === _posicaoJogador) {
        var territorios = [];
        var qtdDadosDefesa = _territorios.quantidadeDeTropaDoTerritorio(_territorioAlvoAtaque);
        var qtdDadosAtaque = 0;
        territorios.push(_territorioAlvoAtaque);

        $.each(_territoriosAtacante, function (i, codigoTerritorio) {
            var qtdTropas = _territorios.quantidadeDeTropaDoTerritorio(codigoTerritorio);
            if (qtdTropas <= 3 && qtdTropas > 0) {
                qtdDadosAtaque += qtdTropas - 1;
            } else {
                qtdDadosAtaque += qtdTropas;
            }
            territorios.push(codigoTerritorio);
        });

        var bounds = _territorios.barreiraDosTerritorios(territorios);
        // TODO: Desabilitar quando a idéia estiver mais amadurecida...
        //_mapaGoogle.fitBounds(bounds);

        if (qtdDadosDefesa > 0 && qtdDadosAtaque > 0 && _jaPodeAtacar) {
            _jaPodeAtacar = false;
            var atacarMsg = comunicacao_atacar(_posicaoJogador, _territorioAlvoAtaque, _territoriosAtacante);
            _libwebsocket.enviarObjJson(atacarMsg);
        }
    }
}

function appwar_abrePainelCartasTerritorios() {
    if (_posicaoJogador === _posicaoJogadorDaVez &&
        _turno.tipoAcao === TipoAcaoTurno.trocar_cartas) {
        _componenteAcaoTurno.btnVerCartasClick(true);
    } else {
        $('#painel_cartas_territorios').css('visibility', 'visible');
        $('#pct_fundo').css('visibility', 'visible');
    }
}

function appwar_fechaPainelCartasTerritorios() {
    $('#acoes_turno').css('z-index', '999');
    $('#painel_cartas_territorios').css('visibility', 'hidden');
    $('#pct_fundo').css('visibility', 'hidden');
    if (_turno.tipoAcao === TipoAcaoTurno.trocar_cartas) {
        _componenteAcaoTurno.alteraFuncaoBtnTrocarParaVerCartas(_posicaoJogadorDaVez === _posicaoJogador);
        _componenteAcaoTurno.alteraFuncaoBtnCancelarParaProsseguir(_posicaoJogadorDaVez === _posicaoJogador);
    }
}

function selecionarCartaTerritorio(num) {
    var nomeDoElemento = '#cartaTerritorio' + num;
    var classesDoElemento = $(nomeDoElemento).attr('class').split(' ');

    if (classesDoElemento.length > 1 &&
        classesDoElemento[1] !== 'carta_territorio_vazia') {
        var nomeDividido = classesDoElemento[1].split('_');
        if (_cartasTerritoriosSelecionadas.length < 3 && nomeDividido.length === 3) {
            // Carta não estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(classesDoElemento[1] + '_selecionado');

            _cartasTerritoriosSelecionadas.push(nomeDividido[2]);
        } else if (_cartasTerritoriosSelecionadas.length > 0 && nomeDividido.length === 4) {
            // Carta estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(nomeDividido[0] + '_' + nomeDividido[1] + '_' + nomeDividido[2]);

            _cartasTerritoriosSelecionadas.splice(_cartasTerritoriosSelecionadas.indexOf(nomeDividido[2]), 1);
        }
    }
}

function appwar_trocaCartasTerritorios() {
    if (_cartasTerritoriosSelecionadas.length === 3) {
        var msg = comunicacao_trocar_cartas_territorio(_posicaoJogador, _cartasTerritoriosSelecionadas);
        _libwebsocket.enviarObjJson(msg);
    }
}

function appwar_iniciaCartasTerritorios() {
    _cartasTerritoriosSelecionadas = [];

    for (i = 1; i <= 5; i++) {
        $('#cartaTerritorio' + i).attr('class', 'carta_territorio carta_territorio_vazia');
    }
}

function territorioMouseMoveFunc(evento, posicaoJogador, codigoDoTerritorio) {
    if (!isNaN(evento.edge) || !isNaN(evento.vertex)) {
        document.getElementById("mapa").className = 'mouse_padrao';
    } else if (_posicaoJogadorDaVez === _posicaoJogador) {
        if (_turno.tipoAcao === TipoAcaoTurno.distribuir_tropas_globais ||
            _turno.tipoAcao === TipoAcaoTurno.distribuir_tropas_grupo_territorio ||
            _turno.tipoAcao === TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
            $('#mapa').attr('class', 'mouse_colocar_tropa');
        } else if (_turno.tipoAcao === TipoAcaoTurno.atacar) {
            if (_territorioAlvoAtaque == null) {
                $('#mapa').attr('class', 'mouse_alvo');
            } else {
                $('#mapa').attr('class', 'mouse_atacar');
            }
        } else if (_turno.tipoAcao === TipoAcaoTurno.mover) {
            // TODO: Verificar se o território é do jogador.
            if (_territorioMovimento != null) {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_dentro');
            } else {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_fora');
            }
        }
    } else {
        document.getElementById("mapa").className = 'mouse_padrao';
    }

    $('#legenda').html(_nomeDosTerritoriosPeloCodigo[codigoDoTerritorio]);
    $('#legenda').css('visibility', 'visible');
}

function territorioMouseOutFunc(posicaoJogador, codigoDoTerritorio) {
    document.getElementById("mapa").className = 'mouse_padrao';
    $('#legenda').html('');
    $('#legenda').css('visibility', 'hidden');
}

function territorioClickMover(posicaoJogador, nomeDoTerritorio) {
    if (nomeDoTerritorio === _territorioMovimento) {
        _territorios.pintarGruposTerritorios();
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
        _territorioAlvoMover = null;
        _territorioMovimento = null;
        _sliderMoverTropas.fechar();
        _componenteAcaoTurno.turnoMover(_posicaoJogador === _posicaoJogadorDaVez, posicaoJogador);
    } else if (_territorioMovimento === null &&
        _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1) {
        _territorios.pintarGruposTerritorios();
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
        _territorioMovimento = nomeDoTerritorio;
        _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
        var indiceCor = _labelTerritorios[nomeDoTerritorio].posicaoJogador;
        _componenteAcaoTurno.turnoMoverEscolheuSaida(nomeDoTerritorio, indiceCor);
        this.tocarSom(this, 'vamosLa.wav');
    } else if (_territorioAlvoMover === null &&
        _territorios.temFronteira(nomeDoTerritorio, _territorioMovimento)) {
        _territorioAlvoMover = nomeDoTerritorio;
        _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
        var indiceCor = _labelTerritorios[nomeDoTerritorio].posicaoJogador;
        _componenteAcaoTurno.turnoMoverEscolheuEntrada(nomeDoTerritorio, indiceCor);
    } else {
        _territorios.pintarGruposTerritorios();
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
        _territorioAlvoMover = null;
        _territorioMovimento = null;
        _sliderMoverTropas.fechar();
        _componenteAcaoTurno.turnoMover(_posicaoJogador === _posicaoJogadorDaVez, posicaoJogador);
    }

    if (_territorioAlvoMover != null && _territorioMovimento != null) {
        _sliderMoverTropas.inicia(1, _territorios.quantidadeDeTropaDoTerritorio(_territorioMovimento) - 1);
        var posicao = _territorios.posicaoHTML(_territorioAlvoMover);
        _sliderMoverTropas.alteraPosicionamentoNoHTML(posicao);
    } else {
        _sliderMoverTropas.fechar();
    }
}

function territorioClickFunc(posicaoJogador, nomeDoTerritorio) {
    if (_posicaoJogador === _posicaoJogadorDaVez) {
        if (_turno.tipoAcao === TipoAcaoTurno.atacar) {
            if (nomeDoTerritorio === _territorioAlvoAtaque) {
                _territorios.pintarGruposTerritorios();
                _territorios.escureceTodosOsTerritoriosDoJogador(_posicaoJogador);
                _territorioAlvoAtaque = null;
                _territoriosAtacante = [];
                // TODO: Nome do jogador.
                _componenteAcaoTurno.turnoAtacar(_posicaoJogador === _posicaoJogadorDaVez, posicaoJogador);
                _componenteAcaoTurno.escondeBtn1Atacar();
            } else if (_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                _territorios.pintarGruposTerritorios();
                _territorioAlvoAtaque = nomeDoTerritorio;
                _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                _territoriosAtacante = [];
                this.tocarSom(this, 'alvo.mp3');
                var indiceCor = _labelTerritorios[nomeDoTerritorio].posicaoJogador;
                _componenteAcaoTurno.turnoAtacarEscolheuAlvo(nomeDoTerritorio, indiceCor,
                    _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio));

                var posicao = _territorios.posicaoHTML(_territorioAlvoAtaque);
                $('#popupBtnAtacar').offset({top: posicao.top + 21, left: posicao.left - 10});
            } else if (_territorioAlvoAtaque !== null) {
                var quantidadeDeTropasNoTerritorio = _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio);
                if (quantidadeDeTropasNoTerritorio > 1 &&
                    _territorios.temFronteira(nomeDoTerritorio, _territorioAlvoAtaque)) {
                    var indiceTerritorio = _territoriosAtacante.indexOf(nomeDoTerritorio);
                    if (indiceTerritorio === -1) {
                        this.tocarSom(this, 'simSenhor_' + (Math.floor(Math.random() * 4) + 1) + '.wav');
                        _territoriosAtacante.push(nomeDoTerritorio);
                        _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                        _componenteAcaoTurno.turnoAtacarAdicionaAtacante(_posicaoJogador,
                            nomeDoTerritorio,
                            quantidadeDeTropasNoTerritorio);
                    } else {
                        _territoriosAtacante.splice(indiceTerritorio, 1);
                        _territorios.diminuiBrilhoTerritorio(nomeDoTerritorio);
                        _componenteAcaoTurno.turnoAtacarRemoveAtacante(_posicaoJogador,
                            nomeDoTerritorio);
                    }
                }
            }
        } else if (_turno.tipoAcao === TipoAcaoTurno.mover) {
            if (!_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                territorioClickMover(posicaoJogador, nomeDoTerritorio);
            }
        } else {
            var qtd_disponivel = parseInt($('#acoes_turno .info').find("#extra").text().replace("+", ""));
            var qtd_escolhida = parseInt($("#quantidade_tropas").find(".rb-tab-active").attr("data-value"));
            var qtd = Math.min(qtd_disponivel, qtd_escolhida);
            var colocarTropaMsg = comunicacao_colocarTropa(posicaoJogador, nomeDoTerritorio, qtd);
            _libwebsocket.enviarObjJson(colocarTropaMsg);
        }
    }
}

function appwar_exibirPainelEntrar() {
    $(function () {
        $("#painelRegistrarOuEntrar #pre_content").load("../../login/entrar.html");
    });
}

function appwar_exibirPainelRegistrar() {
    $(function () {
        $("#painelRegistrarOuEntrar #pre_content").load("../../login/registrar.html");
    });
}

function appwar_exibirPainelRecuperarSenha() {
    $(function () {
        $("#painelRegistrarOuEntrar #pre_content").load("../../login/recuperar_senha.html");
    });
}

function appwar_exibirPainelNovaSenha() {
    $(function () {
        $("#painelRegistrarOuEntrar #pre_content").load("../../login/nova_senha.html");
    });
}

function emailValido(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!emailReg.test(email)) return false;
    else return true;
}

function appwar_entrar(usuario, senha) {
    if (!senha) {
        senha = $('#inputSenha').val();
    }
    if (!usuario) {
        usuario = $('#inputUsuario').val();
    }

    senha = CryptoJS.SHA3(senha);
    senha = base64_encode(senha.toString());
    var entrarMsg = comunicacao_entrar(usuario, senha);
    _libwebsocket.enviarObjJson(entrarMsg);
}

function appwar_registrar(usuario, senha, email) {
    if (!senha) {
        senha = $('#inputSenha').val();
    }
    if (!usuario) {
        usuario = $('#inputUsuario').val();
    }
    if (!email) {
        usuario = $('#inputEmail').val();
    }
    if (usuario.length === 0 || senha.length === 0 || email.length === 0 || !emailValido(email)) {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    } else {
        senha = CryptoJS.SHA3(senha);
        senha = base64_encode(senha.toString());
        const registrarMsg = comunicacao_registrar(usuario, senha, email);
        _libwebsocket.enviarObjJson(registrarMsg);
    }
}

function appwar_recuperarSenha(email) {
    $('#btn_recuperar_senha i').css('display', '');
    $('#btn_recuperar_senha').prop('disabled', true);
    if (!email) {
        email = $('#inputRSEmail').val();
    }
    if (email && emailValido(email)) {
        const msg = comunicacao_recuperarSenha(email);
        _libwebsocket.enviarObjJson(msg);
    } else {
        exibirAlerta('alert-danger', 'Verifique se seu email está correto e tente novamente.');
        $('#btn_recuperar_senha i').css('display', 'none');
        $('#btn_recuperar_senha').prop('disabled', false);
    }
}

function appwar_novaSenha(codigo, email, senha) {
    $('#btn_alterar_senha i').css('display', '');
    $('#btn_alterar_senha').prop('disabled', true);
    if (!codigo) {
        codigo = $('#inputCodigo').val();
    }
    if (!email) {
        email = $('#inputNSEmail').val();
    }
    if (!senha) {
        senha = $('#inputNovaSenha').val();
    }
    if (codigo.length === 0 || senha.length === 0 || email.length === 0 || !emailValido(email)) {
        exibirAlerta('alert-danger', 'Verifique se o código está correto ou senha tem mais que 4 dígitos e tente novamente.');
        $('#btn_alterar_senha i').css('display', 'none');
        $('#btn_alterar_senha').prop('disabled', false);
    } else {
        senha = CryptoJS.SHA3(senha);
        senha = base64_encode(senha.toString());
        const msg = comunicacao_novaSenha(codigo, email, senha);
        _libwebsocket.enviarObjJson(msg);
    }
}

function appwar_recarregarPagina() {
    location.reload(true);
}

function appwar_processaMsg_msg_chat_geral(msgParams) {
    if (!_jogadorEstaEmJogo) this.tocarSom(this, 'mensagem.mp3');

    _chatGeral.escreve(msgParams);
}

function appwar_alterarTituloDaPagina(str) {
    document.title = str + ' | Guerra';
}

function appwar_abrirRanking() {
    var win = window.open('/ranking.html?sorts%5BposicaoNoRanking%5D=1', '_blank');
    win.focus();
}

function appwar_abrirRegras() {
    // var win = window.open('https://docs.google.com/document/d/1mWxAj06aMWTXOR57s69zaMAr5K31YZiqBAlGW2oThng/pub', '_blank');
    var win = window.open('/regras.html', '_blank');
    win.focus();
}

function inputFormLogin_onkeypress(event) {
    if (event.keyCode === 13) {
        appwar_entrar();
    }
    return true;
}

function appwar_atualizarMenuParaSala() {
    appwar_atualizarMenu('sala');
    audio_paraSomDeFundo();
    // audio_escolheSomDeFundo('/sons/loop_war-drums-95-bpm.wav');
    audio_escolheSomDeFundo('/sons/loop_civil-war-music.wav');
    // escolheSomDeFundo('/sons/lux_aeterna.mp3');
    // escolheSomDeFundo('http://emilcarlsson.se/assets/Avicii%20-%20The%20Nights.mp3');
    audio_tocarSomDeFundo();
}

function appwar_atualizarMenuParaJogo() {
    appwar_atualizarMenu('jogo');
    audio_paraSomDeFundo();
    audio_escolheSomDeFundo('');
    // tocarSomDeFundo();
}

function appwar_atualizarMenu(contexto) {
    if (contexto === 'sala') {
        $('#botao_criar_sala').css('display', '');
        $('#botao_sair').css('display', 'none');
    } else if (contexto === 'jogo') {
        $('#botao_criar_sala').css('display', 'none');
        $('#botao_sair').css('display', '');
    }
    $('#menu_principal').css('visibility', 'visible');
}

function appwar_alteraConfiguracaoAudio() {
    const value = $('#botao_conf_audio .material-icons').html();
    if (value === 'volume_up') {
        $('#botao_conf_audio .material-icons').html('volume_off');
    } else {
        $('#botao_conf_audio .material-icons').html('volume_up');
    }
}

function appwar_alteraConfiguracaoMusica() {
    const value = $('#botao_conf_musica .material-icons').html();
    if (value === 'music_note') {
        $('#botao_conf_musica .material-icons').html('music_off');
        audio_paraSomDeFundo();
    } else {
        $('#botao_conf_musica .material-icons').html('music_note');
        audio_tocarSomDeFundo();
    }
}

function appwar_mostrarEsconderConfiguracoes() {
    if ($('#menu_configuracoes').css('visibility') === 'visible') {
        $('#menu_configuracoes').css('visibility', 'hidden');
    } else {
        $('#menu_configuracoes').css('visibility', 'visible');
    }
}

function tocarSom(el, soundfile, force) {
    var el = $('#audioPlayer').get(0);
    var volume = (force || $('#botao_conf_audio .material-icons').html() === 'volume_up') ? 0.5 : 0;
    el.mp3 = new Audio("/sons/" + soundfile);
    el.mp3.volume = volume;
    el.mp3.play();
}

function audio_escolheSomDeFundo(filename) {
    var bgMusicPlayer = document.getElementById('bgMusicPlayer');
    if (filename !== '') {
        bgMusicPlayer.src = filename;
        bgMusicPlayer.setAttribute('loop', 'loop');
        bgMusicPlayer.pause();
        bgMusicPlayer.currentTime = 0;
    } else {
        bgMusicPlayer.removeAttribute('src')
    }
}

function audio_tocarSomDeFundo() {
    var bgMusicPlayer = document.getElementById('bgMusicPlayer');
    bgMusicPlayer.setAttribute('loop', 'loop');
    bgMusicPlayer.volume = $('#botao_conf_musica .material-icons').html() === 'music_note' ? 0.3 : 0;
    bgMusicPlayer.play();
}

function audio_paraSomDeFundo() {
    var bgMusicPlayer = document.getElementById('bgMusicPlayer');
    bgMusicPlayer.pause();
    bgMusicPlayer.currentTime = 0;
}