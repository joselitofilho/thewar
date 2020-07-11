var _chatJogo = new jogowar.war.ChatJogo($('#cj_mensagens'), $('#lj_mensagens'));
var _sliderMoverTropas = new jogos.war.Slider($('#slider-mover-tropas'));
var _componenteAcaoTurno = new jogos.war.ComponenteAcaoTurno();
var _menuJogadores = new jogos.war.MenuJogadores();

function jogo_preparaElementosHtml() {
    _chatJogo.limpa();
    _chatJogo.boasVindas();
    _chatJogo.ativar();

    _jogadorEstaEmJogo = true;

    $('#googleads').css('left', '-728px');
    $('#sala').css('visibility', 'hidden');
    $('#sala #sala_content .box').children().each(function (i, elemento) {
        $(elemento).css('visibility', 'hidden');
    });
    $('#sala #sala_content').children().each(function (i, elemento) {
        $(elemento).css('visibility', 'hidden');
    });

    appwar_atualizarMenuParaJogo();
    $('#bloqueador_tela').css('visibility', 'hidden');
    $('#geral').css('visibility', 'visible');
    $('#jogo').css('visibility', 'visible');
    $('#dados .dado').each(function (i, elemento) {
        $(elemento).css('visibility', 'visible');
    });

    $(".gm-style").parent().css({"background-color": "rgba(0,0,0,0)"});
}

function animarDados() {
    var da1 = Math.floor(Math.random() * 6);
    var da2 = Math.floor(Math.random() * 6);
    var da3 = Math.floor(Math.random() * 6);
    var dd1 = Math.floor(Math.random() * 6);
    var dd2 = Math.floor(Math.random() * 6);
    var dd3 = Math.floor(Math.random() * 6);

    $('#da1').css('background-position', (da1 * -40) + 'px 0px');
    $('#da2').css('background-position', (da2 * -40) + 'px 0px');
    $('#da3').css('background-position', (da3 * -40) + 'px 0px');

    $('#dd1').css('background-position', (dd1 * -40) + 'px -39px');
    $('#dd2').css('background-position', (dd2 * -40) + 'px -39px');
    $('#dd3').css('background-position', (dd3 * -40) + 'px -39px');
}

function pararAnimacaoDosDados(msgParams) {
    try {
        clearInterval(_animarDadosReferencia);
        _animarDadosReferencia = null;

        jogo_efetuaAtaque(msgParams);
    } catch (ex) {
        console.log("Error in fnTimer:\n" + ex);
    }
}

function jogo_jogaDados(qtdDadosAtaque, qtdDadosDefesa, msgParams) {
    try {
        if (_animarDadosReferencia === null) {
            $('#da2').css('visibility', 'hidden');
            $('#da3').css('visibility', 'hidden');
            if (qtdDadosAtaque >= 2) $('#da2').css('visibility', 'visible');
            if (qtdDadosAtaque >= 3) $('#da3').css('visibility', 'visible');

            $('#dd2').css('visibility', 'hidden');
            $('#dd3').css('visibility', 'hidden');
            if (qtdDadosDefesa >= 2) $('#dd2').css('visibility', 'visible');
            if (qtdDadosDefesa >= 3) $('#dd3').css('visibility', 'visible');

            _animarDadosReferencia = setInterval(animarDados, 50);
            setTimeout(function () {
                pararAnimacaoDosDados(msgParams);
            }, 100);
        }
    } catch (ex) {
        console.log("Error in fnTimer:\n" + ex);
    }
}

function jogo_iniciaAnimacaoBatalha(msgParams) {
    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;

    const qtdDadosAtaque = dadosAtaque.length;
    const qtdDadosDefesa = dadosDefesa.length;
    _componenteAcaoTurno.turnoAtacarExibirDados(qtdDadosAtaque, qtdDadosDefesa);

    this.tocarSom(this, "batalha" + (Math.floor(Math.random() * 4) + 1) + ".wav");

    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;

    _componenteAcaoTurno.turnoAtacarExibeTerritoriosEnvolvidosNoAtaque(territoriosDoAtaque, territorioDaDefesa,
        msgParams.jogadorAtaque, msgParams.jogadorDefesa);

    var codigoTerritorios = [territorioDaDefesa.codigo];
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        codigoTerritorios.push(territoriosDoAtaque[i].codigo);
    }
    if (_posicaoJogador !== _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios(codigoTerritorios);
    }

    // Iniciar animacao de jogar os dados...
    // jogo_jogaDados(dadosAtaque.length, dadosDefesa.length, msgParams);
    jogo_efetuaAtaque(msgParams);
}

function jogo_efetuaAtaque(msgParams) {
    _jaPodeAtacar = true;

    _chatJogo.ataque(
        msgParams.jogadorAtaque.usuario,
        msgParams.territoriosDoAtaque,
        msgParams.jogadorDefesa.usuario,
        msgParams.territorioDaDefesa);

    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;

    var diferencaDeQuantidade = 0;

    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;
    var quantidadeDeTropasDosTerritoriosDoAtaque = 0;

    _territoriosAtacanteAposConquistar = territoriosDoAtaque;

    var labelTerritorioDefesa = _labelTerritorios[territorioDaDefesa.codigo];
    diferencaDeQuantidade = Number(labelTerritorioDefesa.texto) - territorioDaDefesa.quantidadeDeTropas;
    if (!msgParams.conquistouTerritorio)
        labelTerritorioDefesa.perdeuTropas(diferencaDeQuantidade);
    labelTerritorioDefesa.alteraQuantiadeDeTropas("" + territorioDaDefesa.quantidadeDeTropas);

    // Desconta os exércitos que foram perdidos no ataque, se houver perda.
    var temTerritorioInvalido = false;
    var fazSentidoMoverAposConquistar = false;
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        var labelTerritorioAtaque = _labelTerritorios[territoriosDoAtaque[i].codigo];
        diferencaDeQuantidade = Number(labelTerritorioAtaque.texto) - territoriosDoAtaque[i].quantidadeDeTropas;
        if (!msgParams.conquistouTerritorio)
            labelTerritorioAtaque.perdeuTropas(diferencaDeQuantidade);
        labelTerritorioAtaque.alteraQuantiadeDeTropas("" + territoriosDoAtaque[i].quantidadeDeTropas);

        if (territoriosDoAtaque[i].quantidadeDeTropas === 1) temTerritorioInvalido = true;
        if (territoriosDoAtaque[i].quantidadeDeTropas > 1) {
            fazSentidoMoverAposConquistar = true;
            quantidadeDeTropasDosTerritoriosDoAtaque += territoriosDoAtaque[i].quantidadeDeTropas - 1;
        }
    }

    if (_posicaoJogador === _posicaoJogadorDaVez) {
        _componenteAcaoTurno.exibeBtn1Atacar();
        _jaPodeAtacar = true;
    }

    // Usabilidade...
    if (msgParams.conquistouTerritorio) {
        labelTerritorioDefesa.explosao();
        if (!fazSentidoMoverAposConquistar) {
            _componenteAcaoTurno.escondeBtn1Atacar();
            setTimeout(function () {
                _territorios.pintarGruposTerritorios();
                _territorios.escureceTodosOsTerritoriosDoJogador(_posicaoJogador);
            }, 1000);
        }
    } else if (temTerritorioInvalido) {
        setTimeout(function () {
            territorioClickFunc(_posicaoJogador, territorioDaDefesa.codigo)
        }, 1000);
    }

    _componenteAcaoTurno.turnoAtacarExibeResultadoDosDados(dadosAtaque, dadosDefesa);

    // Computando ações após conquista de territorio. 
    if (msgParams.conquistouTerritorio) {
        this.tocarSom(this, 'conquistar_' + (Math.floor(Math.random() * 6) + 1) + '.wav');

        _chatJogo.conquistouTerritorio(
            msgParams.jogadorAtaque.usuario,
            msgParams.territorioDaDefesa.codigo);

        setTimeout(function () {
            _componenteAcaoTurno.turnoAtacarConquistouTerritorio(
                msgParams.jogadorAtaque.usuario,
                msgParams.jogadorAtaque.usuario === _usuario,
                msgParams.territorioDaDefesa.codigo);
        }, 1000);

        _territorioAlvoAtaque = null;
        _territorios.alteraDonoTerritorio(territorioDaDefesa.codigo, msgParams.jogadorAtaque.posicao);
        jogo_aumentaQuantidadeDeTerritorioDoJogador(msgParams.jogadorAtaque.posicao);
        jogo_diminuiQuantidadeDeTerritorioDoJogador(msgParams.jogadorDefesa.posicao);

        if (fazSentidoMoverAposConquistar) {
            _turno = {};
            _turno["tipoAcao"] = TipoAcaoTurno.mover_apos_conquistar_territorio;
            _territorioConquistado = msgParams.territorioDaDefesa.codigo;

            if (_posicaoJogador === _posicaoJogadorDaVez) {
                if (quantidadeDeTropasDosTerritoriosDoAtaque > 2) {
                    quantidadeDeTropasDosTerritoriosDoAtaque = 2;
                }
                _componenteAcaoTurno.escondeBtn1Atacar();
                _sliderMoverTropas.inicia(0, quantidadeDeTropasDosTerritoriosDoAtaque);
                var posicao = _territorios.posicaoHTML(_territorioConquistado);
                _sliderMoverTropas.alteraPosicionamentoNoHTML(posicao);
            }
        }
    }
}

function processarMsg_jogo_fase_I(msgParams) {
    $('#sala_boxCriarSala').css('visibility', 'hidden');

    _territorios.limpa();
    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.iniciaLabelDosTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }

    jogo_preparaElementosHtml();
}

function processarMsg_carrega_jogo(msgParams) {
    processarMsg_info_sala(msgParams);

    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }

    jogo_preparaElementosHtml();

    processarMsg_carta_objetivo(msgParams);
    processarMsg_cartas_territorios(msgParams.cartasTerritorio);

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;

    for (let i = 0; i < 6; i++) {
        if (i === _posicaoJogadorDaVez) {
            $('#menu_jogador' + i).css({'margin-top': '-7px'});
        } else {
            $('#menu_jogador' + i).css({'margin-top': '0px'});
        }
    }
}

function processarMsg_carrega_jogo_olheiro(msgParams) {
    processarMsg_info_sala(msgParams);

    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }

    jogo_preparaElementosHtml();

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;
}

function processarMsg_cartas_territorios(msgParams) {
    if (msgParams.length > 0) {
        this.tocarSom(this, "ganhouCarta.wav");
        jogo_animacaoGanhouCartaTerritorio();
    }

    appwar_iniciaCartasTerritorios();

    for (i = 0; i < msgParams.length; i++) {
        var cartaTerritorio = msgParams[i];
        $('#cartaTerritorio' + (i + 1)).attr('class', 'carta_territorio carta_territorio_' + cartaTerritorio.codigoTerritorio);
    }
}

function processarMsg_carta_objetivo(msgParams) {
    _painelObjetivo = new gpscheck.war.PainelObjetivo(Number(msgParams.objetivo) + 1);
    _painelObjetivo.abre();
}

function processarMsg_colocar_tropa(msgParams) {
    this.tocarSom(this, 'colocarTropa.wav');

    _chatJogo.colocaTropa(msgParams.jogador, msgParams.territorio.codigo, msgParams.quantidade);

    if (msgParams.jogador !== _usuario) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios([msgParams.territorio.codigo]);
    }
    _territorios.piscar(msgParams.territorio.codigo);
    if (_labelTerritorios[msgParams.territorio.codigo]) {
        _labelTerritorios[msgParams.territorio.codigo].alteraQuantiadeDeTropas("" + msgParams.territorio.quantidadeDeTropas);
    }

    if (_componenteAcaoTurno) {
        _componenteAcaoTurno.alteraQuantidadeDistribuirTropas(msgParams.quantidadeDeTropasRestante);
    }

    if ((msgParams.quantidadeDeTropasRestante === 0) &&
        (msgParams.jogador === _usuario)) {
        finalizarTurno();
    }
}

function processarMsg_atacar(msgParams) {
    _componenteAcaoTurno.escondeBtn1Atacar();
    if (msgParams.jogadorDefesa.usuario === _usuario) {
        this.tocarSom(this, "ohno.mp3");

        var me = this;
        setTimeout(function () {
            me.jogo_iniciaAnimacaoBatalha(msgParams);
        }, 750);
    } else jogo_iniciaAnimacaoBatalha(msgParams);
}

function processarMsg_mover(msgParams) {
    this.tocarSom(this, 'positivo_' + (Math.floor(Math.random() * 4) + 1) + '.wav');

    _chatJogo.moveu(msgParams.jogador,
        msgParams.doTerritorioObj.codigo,
        msgParams.paraOTerritorioObj.codigo,
        msgParams.quantidade);

    var doTerritorio = msgParams.doTerritorioObj;
    _labelTerritorios[doTerritorio.codigo].alteraQuantiadeDeTropas("" + doTerritorio.quantidadeDeTropas);

    var paraOTerritorio = msgParams.paraOTerritorioObj;
    _labelTerritorios[paraOTerritorio.codigo].alteraQuantiadeDeTropas("" + paraOTerritorio.quantidadeDeTropas);

    if (_posicaoJogador !== _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios([doTerritorio.codigo, paraOTerritorio.codigo]);
    }

    _jaPodeMover = true;

    if (_posicaoJogador === _posicaoJogadorDaVez &&
        _turno.tipoAcao !== TipoAcaoTurno.mover_apos_conquistar_territorio) {
        _territorios.pintarGruposTerritorios();
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
        _territorioAlvoMover = null;
        _territorioMovimento = null;
    }
}

function processarMsg_colocar_tropa_na_troca_de_cartas_territorios(msgParams) {
    appwar_fechaPainelCartasTerritorios();
    var territorios = msgParams.territorios;
    for (i = 0; i < territorios.length; i++) {
        _labelTerritorios[territorios[i].codigo].alteraQuantiadeDeTropas("" + territorios[i].quantidadeDeTropas);
    }
}

function processarMsg_entrou_no_jogo(msgParams) {
    var posicaoJogador = Number(msgParams.posicao);
    var infos = msgParams;
    var usuario = infos.usuario;

    if (posicaoJogador > -1) {
        if (usuario !== _usuario) _chatJogo.entrouNoJogo(usuario, (posicaoJogador === 7));

        if (_posicaoJogador === -1) {
            $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
            $('#painelRegistrarOuEntrar .form-signin').css('visibility', 'hidden');
            _posicaoJogador = posicaoJogador;
            appwar_alterarTituloDaPagina(usuario);

            // Olheiro.
            if (posicaoJogador === 7) {
                jNotify(
                    "Este jogo já está em andamento. Você poderá apenas assistí-lo.",
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
                        ShowOverlay: false
                    }
                );
            }
        } else if (posicaoJogador === 7) {
            jNotify(
                usuario + " está assistindo a partida.",
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
                    ShowOverlay: false
                }
            );
        }

        $("#jogador" + (posicaoJogador + 1)).removeClass("text_through");
    }
}

function processarMsg_saiu_do_jogo(msgParams) {
    this.tocarSom(this, "saindo.wav");

    const posicaoJogador = Number(msgParams.posicao);
    $("#jogador" + (posicaoJogador + 1)).addClass("text_through");

    _chatJogo.saiuDoJogo(msgParams.usuario, (posicaoJogador === 7));

    if (msgParams.usuario === _usuario) {
        _territorios.limpa();
        appwar_limparVariaveis();
        jogo_removeElementosHtml();
    }
}

function jogo_processaMsg_jogador_destruido(msgParams) {
    setTimeout(function () {
        const posicaoJogador = msgParams.jogador.posicao;
        this.tocarSom(this, "jogadorDestruido.mp3");
        var usuario = msgParams.jogador.usuario;
        if (posicaoJogador === _posicaoJogador) usuario = 'Você';
        _painelObjetivo.abreEspecifico(Number(msgParams.jogador.objetivo) + 1,
            usuario + ' foi destruído.');
    }, 2000);
}

function jogo_processaMsg_jogo_interrompido(msgParams) {
    _territorios.limpa();
    appwar_limparVariaveis();
    jogo_removeElementosHtml();
}

function processarMsg_turno(msgParams) {
    _turno = msgParams;
    _infoJogadorDaVezDoTurno = msgParams.vezDoJogador;
    _posicaoJogadorDaVez = msgParams.vezDoJogador.posicao;
    $('#pct_valorDaTroca').html("Valor da troca: " + msgParams.valorDaTroca);

    const tempoTotal = Number(msgParams.tempoRestante);
    const timeoutSemTolerancia = Number(msgParams.timeoutSemTolerancia);
    jogo_iniciaBarraDeProgresso(tempoTotal, timeoutSemTolerancia);

    jogo_alteraInfoTurno(msgParams);

    if (msgParams.tipoAcao === TipoAcaoTurno.distribuir_tropas_globais) {
        _chatJogo.distrubuirTropasGlobais(msgParams.vezDoJogador.usuario, msgParams.quantidadeDeTropas);
        processarMsg_turno_distribuir_tropas_globais(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
        processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.trocar_cartas) {
        processarMsg_turno_trocar_cartas(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        _chatJogo.trocouCartasTerritorio(msgParams.vezDoJogador.usuario, msgParams.quantidadeDeTropas);
        processarMsg_turno_distribuir_tropas_globais(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.atacar) {
        processarMsg_turno_atacar(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.mover) {
        processarMsg_turno_mover(msgParams);
    } else if (msgParams.tipoAcao === TipoAcaoTurno.jogo_terminou) {
        processarMsg_turno_jogo_terminou(msgParams);
    }
}

function processarMsg_turno_distribuir_tropas_globais(msgParams) {
    if (_posicaoJogador === _posicaoJogadorDaVez) {
        this.tocarSom(this, "buzina.mp3", true);
    } else {
        this.tocarSom(this, "turnoDistribuirTropa.mp3");
    }

    if (msgParams.territoriosDosJogadores) {
        for (let i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
            const territorioDosJogadores = msgParams.territoriosDosJogadores[i];
            _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        }
    }

    _componenteAcaoTurno.alteraQuantidadeDistribuirTropas(msgParams.quantidadeDeTropas);

    _territorios.pintarGruposTerritorios();
    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador.posicao);
}

function processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams) {
    if (_posicaoJogador === _posicaoJogadorDaVez) {
        this.tocarSom(this, "turnoDistribuirTropa.mp3");
    }

    _componenteAcaoTurno.alteraQuantidadeDistribuirTropas(msgParams.quantidadeDeTropas);

    _territorios.pintarGruposTerritorios();
    _territorios.manterFocoNoGrupo(msgParams.grupoTerritorio);

    _chatJogo.distrubuirTropasGrupoTerritorio(msgParams.vezDoJogador.usuario, msgParams.grupoTerritorio, msgParams.quantidadeDeTropas);
}

function processarMsg_turno_trocar_cartas(msgParams) {
    this.tocarSom(this, "turnoTrocarCarta.mp3");

    if (msgParams.obrigatorio && (_posicaoJogador === msgParams.vezDoJogador.posicao)) {
        _componenteAcaoTurno.btnVerCartasClick(true);
    }

    _chatJogo.verificandoTroca(msgParams.vezDoJogador.usuario);
}

function processarMsg_turno_atacar(msgParams) {
    this.tocarSom(this, 'atacar.wav');
    _componenteAcaoTurno.alteraQuantidadeDistribuirTropas(0);

    _territorioConquistado = null;
    _territorios.pintarGruposTerritorios();

    if (_posicaoJogador === msgParams.vezDoJogador.posicao) {
        _territorios.escureceTodosOsTerritoriosDoJogador(msgParams.vezDoJogador.posicao);
    }

    _chatJogo.estaAtacando(msgParams.vezDoJogador.usuario);
}

function processarMsg_turno_mover(msgParams) {
    _componenteAcaoTurno.escondeBtn1Atacar();
    this.tocarSom(this, 'mover.wav');

    _territorios.pintarGruposTerritorios();

    if (_posicaoJogador === msgParams.vezDoJogador.posicao) {
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador.posicao);
    }

    _chatJogo.estaMovendo(msgParams.vezDoJogador.usuario);
}

function processarMsg_turno_jogo_terminou(msgParams) {
    this.tocarSom(this, 'venceuJogo.wav');
    var textoVencedor = msgParams.ganhador.usuario;
    if (msgParams.ganhador.usuario === _usuario) textoVencedor = "Você";
    _painelVitoria.abre(textoVencedor, msgParams.ganhador.pontos, msgParams.objetivo);
}

function jogo_processaMsg_msg_chat_jogo(msgParams) {
    this.tocarSom(this, 'mensagem.mp3');
    let indiceCor = msgParams.jogador.posicao;
    if (indiceCor === -1) {
        indiceCor = 999;
    }
    _chatJogo.escreve({usuario: msgParams.jogador.usuario, texto: msgParams.texto}, indiceCor);
}

/* Informações dos turnos */
function jogo_alteraInfoTurno(msgParams) {
    const tipoAcao = msgParams.tipoAcao;

    $('#it_sub_titulo').css('visibility', 'hidden');
    $('#acoes_turno .info #extra').css('visibility', 'hidden');

    var posicaoJogador = Number(msgParams.vezDoJogador.posicao) + 1;
    var ehOJogadorDaVez = msgParams.vezDoJogador.posicao === _posicaoJogador;

    _componenteAcaoTurno.alteraTimelineJogadorDaVez(tipoAcao, posicaoJogador);
    _componenteAcaoTurno.alteraBotoesDaAcao(ehOJogadorDaVez, tipoAcao);

    if (tipoAcao === TipoAcaoTurno.distribuir_tropas_globais) {
        _componenteAcaoTurno.turnoDistribuirTopasGlobais(ehOJogadorDaVez, msgParams.vezDoJogador.usuario, msgParams.quantidadeDeTropas);
    } else if (tipoAcao === TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
        var strGrupoTerritorio = msgParams.grupoTerritorio;
        if (strGrupoTerritorio === "AmericaDoNorte") strGrupoTerritorio = "Am. do Norte";
        else if (strGrupoTerritorio === "AmericaDoSul") strGrupoTerritorio = "Am. do Sul";

        _componenteAcaoTurno.turnoDistribuirTopasContinente(ehOJogadorDaVez,
            msgParams.vezDoJogador.usuario,
            msgParams.quantidadeDeTropas,
            strGrupoTerritorio);
    } else if (tipoAcao === TipoAcaoTurno.trocar_cartas) {
        _componenteAcaoTurno.turnoTrocarCartas(ehOJogadorDaVez,
            msgParams.vezDoJogador.usuario, msgParams.obrigatorio);
    } else if (tipoAcao === TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        _componenteAcaoTurno.turnoDistribuirTopasPorTroca(ehOJogadorDaVez, msgParams.vezDoJogador.usuario, msgParams.quantidadeDeTropas);
    } else if (tipoAcao === TipoAcaoTurno.atacar) {
        _componenteAcaoTurno.turnoAtacar(ehOJogadorDaVez, msgParams.vezDoJogador.usuario);
    } else if (tipoAcao === TipoAcaoTurno.mover) {
        _componenteAcaoTurno.turnoMover(ehOJogadorDaVez, msgParams.vezDoJogador.usuario);
    }

    _menuJogadores.posicionaElementos(msgParams.jogadorQueComecou, msgParams.ordemJogadores, msgParams.infoJogadores);
    for (let i = 0; i < msgParams.infoJogadores.length; i++) {
        const infos = msgParams.infoJogadores[i];
        const title = "Nome: " + infos.usuario + '\n' +
            "Total de território: " + infos.total_territorios + "\n" +
            "Total de cartas território: " + infos.total_cartas_territorio;
        $('#menu_jogador' + infos.posicao).prop('title', title);
        if (infos.posicao === msgParams.vezDoJogador.posicao) {
            $('#menu_jogador' + infos.posicao).css({'margin-top': '-7px'});
        } else {
            $('#menu_jogador' + infos.posicao).css({'margin-top': '0px'});
        }
    }
}

/* Territorios */
function jogo_alteraQuantidadeDeTerritoriosPorJogador(territorios, posicao) {
    $('#qtdTerritorio' + posicao).html(territorios.length);
}

function jogo_diminuiQuantidadeDeTerritorioDoJogador(posicao) {
    var valor = Number($('#qtdTerritorio' + posicao).html()) - 1;
    if (valor >= 0) $('#qtdTerritorio' + posicao).html(valor);
}

function jogo_aumentaQuantidadeDeTerritorioDoJogador(posicao) {
    var valor = Number($('#qtdTerritorio' + posicao).html()) + 1;
    if (valor <= 42) $('#qtdTerritorio' + posicao).html(valor);
}

/* Chat */
function ct_texto_onkeypress(event) {
    if (event.keyCode === 13) {
        jogo_enviaMsgChatDoJogo();
    }
    return true;
}

function jogo_enviaMsgChatDoJogo() {
    jogo_enviaMsg($('#ct_texto').val());
}

function jogo_enviaMsg(texto) {
    if (texto.length > 0) {
        $('#ct_texto').val('');
        msg = comunicacao_MsgChatJogo(texto);
        _libwebsocket.enviarObjJson(msg);
    }
}

/* Barra de progresso */
var _loopTempoRestante = null;
var _timeoutTempoRestante = null;

function jogo_iniciaBarraDeProgresso(tempoTotal, timeoutSemTolerancia) {
    const minutosTotal = timeoutSemTolerancia;

    if (_loopTempoRestante != null || _timeoutTempoRestante != null) {
        clearInterval(_loopTempoRestante);
        clearTimeout(_timeoutTempoRestante);
        _loopTempoRestante = null;
        _timeoutTempoRestante = null;
    }
    jogo_alteraTempoRestante(tempoTotal);

    var inc = 100.0 / minutosTotal;
    var valor = inc * (minutosTotal - tempoTotal);
    var tempo = tempoTotal;
    _loopTempoRestante = setInterval(function () {
        var barra = $('#barra');
        valor += inc;
        barra.width(valor + '%');
        if (valor > 85) {
            barra.css('background-color', '#dd514c');
            tocarSom(this, "alarme.mp3");
        } else if (valor > 50) {
            barra.css('background-color', '#faa732');
        } else {
            $('#barra').css('background-color', '#5eb95e');
        }

        tempo -= 1.0;
        jogo_alteraTempoRestante(tempo);
    }, 1000);

    _timeoutTempoRestante = setTimeout(function () {
        if (_loopTempoRestante != null)
            jogo_finalizaBarraDeProgresso();
    }, tempoTotal * 1000);
}

function jogo_alteraTempoRestante(tempo) {
    var minutos = Math.floor(tempo / 60);
    var segundos = Math.round(tempo % 60);
    if (minutos < 10) minutos = "0" + minutos;
    if (segundos < 10) segundos = "0" + segundos;
    $('#tempo_restante').html(minutos + ":" + segundos);
}

function jogo_finalizaBarraDeProgresso() {
    clearInterval(_loopTempoRestante);
    clearTimeout(_timeoutTempoRestante);
    _loopTempoRestante = null;
    _timeoutTempoRestante = null;
    $('#barra').width('100%');
    $('#barra').css('background-color', '#dd514c');
    jogo_alteraTempoRestante(0);
}

function jogo_animacaoGanhouCartaTerritorio() {
    $('#ganhou_carta').css('margin-top', '-100px');
    $('#ganhou_carta').css('opacity', '1.0');
    $('#ganhou_carta').css('visibility', 'visible');
    $('#ganhou_carta').animate({
        'margin-top': '132px'
    }, 600, function () {
        $(this).animate({
            opacity: 0.0
        }, 600, function () {
            $('#ganhou_carta').css('visibility', 'hidden');
        });
    });
}

function jogo_moveTropas() {
    _jaPodeMover = false;
    var qtd = _sliderMoverTropas.quantidade();
    if (_turno.tipoAcao === TipoAcaoTurno.mover_apos_conquistar_territorio) {
        var moverMsg = comunicacao_moverAposConquistarTerritorio(qtd);
        _libwebsocket.enviarObjJson(moverMsg);
    } else if (_turno.tipoAcao === TipoAcaoTurno.mover) {
        var moverMsg = comunicacao_mover(_posicaoJogador,
            _territorioMovimento,
            _territorioAlvoMover, qtd);
        _libwebsocket.enviarObjJson(moverMsg);
    }

    _sliderMoverTropas.fechar();
    if (_turno.tipoAcao == TipoAcaoTurno.mover) _componenteAcaoTurno.turnoMoverLimpar();
}

function jogo_cancelaMoverTropas() {
    if (_turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio) {
        finalizarTurno();
    } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
        _territorios.pintarGruposTerritorios();
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
        _territorioAlvoMover = null;
        _territorioMovimento = null;
    }
    _sliderMoverTropas.fechar();
    _componenteAcaoTurno.turnoMoverLimpar();
}

function jogo_sair() {
    msg = comunicacao_sairDaSala();
    _libwebsocket.enviarObjJson(msg);
}

function jogo_fechaPainelVitoria() {
    _painelVitoria.fecha();
}

function jogo_removeElementosHtml() {
    _chatJogo.desativar();

    _componenteAcaoTurno.escondeBtn1Atacar();
    $('#dados .dado').each(function (i, elemento) {
        $(elemento).css('visibility', 'hidden');
    });
    $('#menu_jogadores li span').each(function (i, elemento) {
        $(elemento).html('0');
    });
    $('#menu_jogadores li a').each(function (i, elemento) {
        $(elemento).html('');
    });
    $('.carta_territorio').each(function (i, elemento) {
        $(elemento).attr('class', 'carta_territorio carta_territorio_vazia');
    });
    appwar_atualizarMenuParaSala();
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#painelRegistrarOuEntrar .form-signin').css('visibility', 'hidden');
    $('#slider-mover-tropas').css('visibility', 'hidden');
    $('#quantidade_tropas').css('visibility', 'hidden');
    $('#geral').css('visibility', 'hidden');
    $('#jogo').css('visibility', 'hidden');
    $('#it_sub_titulo').css('visibility', 'hidden');
    $('#acoes_turno .info #extra').css('visibility', 'hidden');
    clearInterval(_loopTempoRestante);
    clearTimeout(_timeoutTempoRestante);
}

//Quantidade de tropas - switcher function:
$(".rb-tab").click(function () {
    $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
    $(this).addClass("rb-tab-active");
});