//
// http://soundbible.com/tags-war.html
//

_painelObjetivo = null;

_usuario = null;
_posicaoJogador = -1;
_salaDoJogador = null;
_turno = null;
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

_sala = null;

function appwar_limparVariaveis() {
    _posicaoJogador = -1;
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

    _sala = null;
}

function exibirAlerta(tipo, msg) {
    $('#alerta').removeClass('alert-info alert-success alert-warning alert-danger');
    $('#alerta').addClass(tipo);
    $('#alerta_texto').html(msg);
    $('#alerta').css('visibility', 'visible');
    $("#alerta")
        .fadeIn('slow')
        .animate({opacity : 1.0}, 2000)
        .fadeOut('slow', function() {
            $(this).hide();
        });
}

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_registrar(msgParams) {
    if (msgParams.status == 1) {
        exibirAlerta('alert-success', 'Registrado com sucesso.');
    } else if (msgParams.status == 0) {
        exibirAlerta('alert-info', 'Você já está registrado.');
    } else {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    }
}

function processarMsg_entrar(msgParams) {
    if (msgParams.status == 1) {
        var cookie = new gpscheck.web.Cookie();
        cookie.cria("usuario", $('#inputUsuario').val());
        var senha = CryptoJS.SHA3($('#inputSenha').val());
        senha = senha.toString(CryptoJS.enc.Base64);

        this.tocarSom(this, "entrou.mp3");
        appwar_alterarTituloDaPagina(msgParams.usuario);
        _usuario = msgParams.usuario;

        $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
        $('#sala').css('visibility', 'visible');
	$('html,body').css('overflow','auto');
    } else {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    }
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
    $('#painelRegistrarOuEntrar').css('visibility', 'visible');
}

function posRecebimentoMensagemServidor(valor) {
    console.log('Recebeu msg ' + valor);
    var jsonMensagem = JSON.parse(valor);
    if (jsonMensagem.tipo == TipoMensagem.registrar) {
        processarMsg_registrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.entrar) {
        processarMsg_entrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.lobby) {
        processarMsg_lobby(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.criar_sala) {
        processarMsg_criar_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.info_sala) {
        processarMsg_info_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.fechar_sala) {
        processarMsg_fechar_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.altera_posicao_na_sala) {
        processarMsg_altera_posicao_na_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.jogo_fase_I) {
        processarMsg_jogo_fase_I(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carta_objetivo) {
        processarMsg_carta_objetivo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.colocar_tropa) {
        processarMsg_colocar_tropa(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.turno) {
        processarMsg_turno(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.atacar) {
        processarMsg_atacar(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.mover) {
        processarMsg_mover(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.cartas_territorios) {
        processarMsg_cartas_territorios(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios) {
        processarMsg_colocar_tropa_na_troca_de_cartas_territorios(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.entrou_no_jogo) {
        processarMsg_entrou_no_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.saiu_do_jogo) {
        processarMsg_saiu_do_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carrega_jogo) {
        processarMsg_carrega_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carrega_jogo_olheiro) {
        processarMsg_carrega_jogo_olheiro(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.msg_chat_jogo) {
        jogo_processaMsg_msg_chat_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.jogador_destruido) {
        jogo_processaMsg_jogador_destruido(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.erro) {
        processarMsg_erro();
    }
}

function posFechamentoSocket(valor) {
    $('#bloqueador_tela').css('visibility', 'visible');
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#botao_recarregar').css('visibility', 'visible');
}

function iniciarPartida() {
    if (_quantidadeDeJogadoresNaSala >= 3) {
        iniciarPartidaMsg = comunicacao_iniciarPartida();
        _libwebsocket.enviarObjJson(iniciarPartidaMsg);
    } else {
        alert('Para iniciar o jogo é preciso pelo menos 3 jogadores na sala.');
    }
}

function finalizarTurno() {
    finalizarPartidaMsg = comunicacao_finalizarTurno();
    _libwebsocket.enviarObjJson(finalizarPartidaMsg);
}

function atacar() {
    if (_posicaoJogadorDaVez == _posicaoJogador) {
        var territorios = [];
        var qtdDadosDefesa = _territorios.quantidadeDeTropaDoTerritorio(_territorioAlvoAtaque);
        var qtdDadosAtaque = 0;
        territorios.push(_territorioAlvoAtaque);
        
        $.each(_territoriosAtacante, function(i, codigoTerritorio) {
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
    $('#painel_cartas_territorios').css('visibility', 'visible');
    $('#pct_fundo').css('visibility', 'visible');
}

function appwar_fechaPainelCartasTerritorios() {
    $('#painel_cartas_territorios').css('visibility', 'hidden');
    $('#pct_fundo').css('visibility', 'hidden');
}

function appwar_alteraQuantidadeDeTropas(valor) {
    $('#quantidade_de_tropas').html(valor);
    $('#it_info').html(valor);
}

function selecionarCartaTerritorio(num) {
    var nomeDoElemento = '#cartaTerritorio' + num;
    var classesDoElemento = $(nomeDoElemento).attr('class').split(' ');
    
    if (classesDoElemento.length > 1 && 
        classesDoElemento[1] != 'carta_territorio_vazia') {
        var nomeDividido = classesDoElemento[1].split('_');
        if (_cartasTerritoriosSelecionadas.length < 3 && nomeDividido.length == 3) {
            // Carta não estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(classesDoElemento[1] + '_selecionado');
            
            _cartasTerritoriosSelecionadas.push(nomeDividido[2]);
        } else if (_cartasTerritoriosSelecionadas.length > 0 && nomeDividido.length == 4) {
            // Carta estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(nomeDividido[0] + '_' + nomeDividido[1] + '_' + nomeDividido[2]);
            
            _cartasTerritoriosSelecionadas.splice(_cartasTerritoriosSelecionadas.indexOf(nomeDividido[2]), 1);
        }
    }
}

function appwar_trocaCartasTerritorios() {
    if (_cartasTerritoriosSelecionadas.length == 3) {
        var msg = comunicacao_trocar_cartas_territorio(_posicaoJogador, _cartasTerritoriosSelecionadas);
        _libwebsocket.enviarObjJson(msg);
    }
}

function appwar_iniciaCartasTerritorios() {
    _cartasTerritoriosSelecionadas = [];

    for (i=1; i<=5; i++) {
        $('#cartaTerritorio' + i).attr('class','carta_territorio carta_territorio_vazia');
    }
}

function territorioMouseMoveFunc(evento, posicaoJogador, nomeDoTerritorio) {
    if (!isNaN(evento.edge) || !isNaN(evento.vertex)) {
        document.getElementById("mapa").className = '';
    } else if (_posicaoJogadorDaVez == _posicaoJogador) {
        if (_turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
            $('#mapa').attr('class', 'mouse_colocar_tropa');
        } else if (_turno.tipoAcao == TipoAcaoTurno.atacar) {
            if (_territorioAlvoAtaque == null) {
                $('#mapa').attr('class', 'mouse_alvo');
            } else {
                $('#mapa').attr('class', 'mouse_atacar');
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
            if (_territorioAlvoMover == null) {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_dentro');
            } else {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_fora');
            }
        }
    } else {
        document.getElementById("mapa").className = '';
    }
}

function territorioMouseOutFunc(posicaoJogador, nomeDoTerritorio) {
    document.getElementById("mapa").className = '';
}

function territorioClickFunc(posicaoJogador, nomeDoTerritorio) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        if (_turno.tipoAcao == TipoAcaoTurno.atacar) {
            if (nomeDoTerritorio == _territorioAlvoAtaque) {
                _territorios.pintarGruposTerritorios();
                _territorios.escureceTodosOsTerritoriosDoJogador(_posicaoJogador);
                _territorioAlvoAtaque = null;
                _territoriosAtacante = [];
                appwar_mudarCursor('alvo');
            }
            else if (_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                _territorios.pintarGruposTerritorios();
                _territorioAlvoAtaque = nomeDoTerritorio;
                _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                _territoriosAtacante = [];
                appwar_mudarCursor('atacar');
                this.tocarSom(this, 'alvo.mp3');
            }
            else if (_territorioAlvoAtaque != null) {
                if (_territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1 &&
                    _territorios.temFronteira(nomeDoTerritorio, _territorioAlvoAtaque)) {
                    var indiceTerritorio = _territoriosAtacante.indexOf(nomeDoTerritorio);
                    if (indiceTerritorio == -1) {
                        this.tocarSom(this, 'simSenhor_' + (Math.floor(Math.random()*4)+1) + '.wav');
                        _territoriosAtacante.push(nomeDoTerritorio);
                        _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                    } else {
                        _territoriosAtacante.splice(indiceTerritorio, 1);
                        _territorios.diminuiBrilhoTerritorio(nomeDoTerritorio);
                    }
                }
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
            if (!_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                if (nomeDoTerritorio == _territorioAlvoMover) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = null;
                    _territorioMovimento = null;
                    appwar_mudarCursor('mover_para_dentro');
                    _sliderMoverTropas.fechar();
                } else if (_territorioAlvoMover == null) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                    appwar_mudarCursor('mover_para_fora');
                    this.tocarSom(this, 'vamosLa.wav');
                } else if (_territorioMovimento == null && 
                           _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1 &&
                           _territorios.temFronteira(nomeDoTerritorio, _territorioAlvoMover)) {
                    _territorioMovimento = nomeDoTerritorio;
                    _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                } else {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                    _territorioMovimento = null;
                    appwar_mudarCursor('mover_para_fora');
                    this.tocarSom(this, 'vamosLa.wav');
                }
                
                if (_territorioAlvoMover != null) {
                    _sliderMoverTropas.inicia(1, _territorios.quantidadeDeTropaDoTerritorio(_territorioMovimento)-1);
                } else {
                    _sliderMoverTropas.fechar();
                }
            }
        } else {
            var colocarTropaMsg = comunicacao_colocarTropa(posicaoJogador, nomeDoTerritorio, 1);
            _libwebsocket.enviarObjJson(colocarTropaMsg);
        }
    }
}

function appwar_exibirPainelEntrar() {
    var html = "<input id=\"inputUsuario\" type=\"text\"";
    html += "class=\"input-block-level\"";
    html += "placeholder=\"Usu&aacute;rio\" />";
    
    html += "<input id=\"inputSenha\" type=\"password\"";
    html += "class=\"input-block-level\"";
    html += "placeholder=\"Senha\" />";
    
    html += "<button class=\"btn btn-large btn-default\" onclick=\"appwar_entrar();\">Entrar</button>";
    
    $('#pre_content').html(html);
    $('#abaEntrar').attr('class', 'active');
    $('#abaRegistrar').attr('class', '');
}

function appwar_exibirPainelRegistrar() {
    var html = "<input id=\"inputUsuario\" type=\"text\"";
    html += "class=\"input-block-level\"";
    html += "placeholder=\"Usu&aacute;rio\" />";
    
    html += "<input id=\"inputSenha\" type=\"password\"";
    html += "class=\"input-block-level\"";
    html += "placeholder=\"Senha\" />";
    
    html += "<input id=\"inputEmail\" type=\"text\"";
    html += "class=\"input-block-level\"";
    html += "placeholder=\"Email\" />";
    
    html += "<button class=\"btn btn-large btn-default\" onclick=\"appwar_registrar();\">Registrar</button>";
    
    $('#pre_content').html(html);
    $('#abaEntrar').attr('class', '');
    $('#abaRegistrar').attr('class', 'active');
}

function emailValido(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if( !emailReg.test(email)) return false;
    else return true;
}

function appwar_entrar() {
    var senha = CryptoJS.SHA3($('#inputSenha').val());
    senha = senha.toString(CryptoJS.enc.Base64);
    var entrarMsg = comunicacao_entrar($('#inputUsuario').val(), senha);
    _libwebsocket.enviarObjJson(entrarMsg);
}

function appwar_registrar() {
    var usuario = $('#inputUsuario').val();
    var senha = $('#inputSenha').val();
    var email = $('#inputEmail').val();
    if (usuario.length == 0 || senha.length == 0 || email.length == 0 || !emailValido(email)) {
        exibirAlerta('alert-danger', 'Verifique se seus dados estão corretos e tente novamente.');
    } else {
        senha = CryptoJS.SHA3(senha);
        senha = senha.toString(CryptoJS.enc.Base64);
        var registrarMsg = comunicacao_registrar(usuario, senha, email);
        _libwebsocket.enviarObjJson(registrarMsg);
    }
}

function appwar_recarregarPagina() {
    location.reload();
}

function iniciarControleDeAudio() {
    var audioSlider  = $('#audioSlider');
    var audioSliderTooltip = $('.audioSliderTooltip');
    var audioPlayer = $('#audioPlayer').get(0);

    audioSliderTooltip.hide();

    audioSlider.slider({
            value: 20,
            min: 0,
            max: 100,
            range: 'min',
            animate: true,
            step: 1,
            start: function(e, ui) {
                audioSliderTooltip.fadeIn('fast');
            },
            slide: function(e, ui) {
                var valor = ui.value;
                var volume = $('.audioPlayerVolume');

                audioSliderTooltip.css('left', valor).text(valor);
                if (valor <= 5) { 
                    volume.css('background-position', '0 0');
                } else if (valor <= 25) {
                    volume.css('background-position', '0 -25px');
                } else if (valor <= 75) {
                    volume.css('background-position', '0 -50px');
                } else {
                    volume.css('background-position', '0 -75px');
                }

                audioPlayer.volume = ui.value / 100.0;
            },
            stop: function(e, ui) {
                audioSliderTooltip.fadeOut('fast');
            }
    });
}

function appwar_mudarCursor(tipo) {
    if (tipo == 'colocar_tropa') {
        $('body').attr('class', 'mouse_colocar_tropa');
    }  else if (tipo == 'alvo') {
        $('body').attr('class', 'mouse_alvo');
    } else if (tipo == 'trocar_cartas') {
        $('body').attr('class', 'mouse_trocar_cartas');
    }  else if (tipo == 'atacar') {
        $('body').attr('class', 'mouse_atacar');
    } else if (tipo == 'mover_para_fora') {
        $('body').attr('class', 'mouse_mover_tropas_para_fora');
    } else if (tipo == 'mover_para_dentro') {
        $('body').attr('class', 'mouse_mover_tropas_para_dentro');
    } else {
        $('body').attr('class', '');
    } 
}

function appwar_alterarTituloDaPagina(str) {
    document.title = str + ' | JogoWar';
}

function tocarSom(el, soundfile) {
    var el = $('#audioPlayer').get(0);
    var volume = $('#audioSlider').slider('value') / 100.0;

    console.log('Tocando som: ' + soundfile);

    //if (el.mp3) {
    //    if(el.mp3.paused) el.mp3.play();
    //    else el.mp3.pause();
    //} else {
        el.mp3 = new Audio("http://war.jogowar.com.br:9092/sons/" + soundfile);
        el.mp3.volume = volume;
        el.mp3.play();
    //}
}

function tocarSomDeFundo(el) {
    if (el.mp3) {
        if(el.mp3.paused) el.mp3.play();
        else el.mp3.pause();
    } else {
        el.mp3 = new Audio("http://war.jogowar.com.br:9092/sons/lux_aeterna.mp3");
        el.mp3.addEventListener('ended', function() {
            this.currentTime = 0;
            this.play();
        }, false);
        el.mp3.volume = 0.1;
        el.mp3.play();
    }
}

function appwar_abrirRegras() {
    var win=window.open('https://docs.google.com/document/d/1mWxAj06aMWTXOR57s69zaMAr5K31YZiqBAlGW2oThng/pub', '_blank');
    win.focus();
}
