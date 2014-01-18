var _chatJogo = new jogowar.war.ChatJogo($('#ct_mensagens'));

function jogo_preparaElementosHtml() {
    _chatJogo.limpa();
    $('#sala').css('visibility', 'hidden');
    $('#sala .form-signin').children().each(function(i, elemento) {
        $(elemento).css('visibility', 'hidden');
    });
    $('#bloqueador_tela').css('visibility', 'hidden');
    $('#geral').css('visibility', 'visible');
    $('#jogo').css('visibility', 'visible');
    $('#dados .dado').each(function(i, elemento) {
        $(elemento).css('visibility', 'hidden');
    });
}

function animarDados() {
    var da1 = Math.floor(Math.random()*6);
    var da2 = Math.floor(Math.random()*6);
    var da3 = Math.floor(Math.random()*6);
    var dd1 = Math.floor(Math.random()*6);
    var dd2 = Math.floor(Math.random()*6);
    var dd3 = Math.floor(Math.random()*6);
    
    $('#da1').css('background-position', (da1*-40) + 'px 0px');
    $('#da2').css('background-position', (da2*-40) + 'px 0px');
    $('#da3').css('background-position', (da3*-40) + 'px 0px');
    
    $('#dd1').css('background-position', (dd1*-40) + 'px -40px');
    $('#dd2').css('background-position', (dd2*-40) + 'px -40px');
    $('#dd3').css('background-position', (dd3*-40) + 'px -40px');
}

function pararAnimacaoDosDados(msgParams) {
    try {
        clearInterval(_animarDadosReferencia);
        _animarDadosReferencia = null;
        
        jogo_efetuaAtaque(msgParams);
    } catch(ex) {
        console.log("Error in fnTimer:\n" + ex);
    }
}

function jogo_jogaDados(qtdDadosAtaque, qtdDadosDefesa, msgParams) {
    try {
        if (_animarDadosReferencia == null) {
            $('#da2').css('visibility', 'hidden');
            $('#da3').css('visibility', 'hidden');
            if (qtdDadosAtaque >= 2) $('#da2').css('visibility', 'visible');
            if (qtdDadosAtaque >= 3) $('#da3').css('visibility', 'visible');
            
            $('#dd2').css('visibility', 'hidden');
            $('#dd3').css('visibility', 'hidden');
            if (qtdDadosDefesa >= 2) $('#dd2').css('visibility', 'visible');
            if (qtdDadosDefesa >= 3) $('#dd3').css('visibility', 'visible');
            
            _animarDadosReferencia = setInterval(animarDados, 50);
            setTimeout(function() { pararAnimacaoDosDados(msgParams); }, 2000);
        }
    } catch(ex) {
        console.log("Error in fnTimer:\n" + ex);
    }
}

function jogo_iniciaAnimacaoBatalha(msgParams) {
    this.tocarSom(this, "batalha" + (Math.floor(Math.random()*4)+1) + ".wav");

    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;

    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;
    var codigoTerritorios = [territorioDaDefesa.codigo];
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        codigoTerritorios.push(territoriosDoAtaque[i].codigo);
    }
    if (_posicaoJogador != _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios(codigoTerritorios);
    }
    
    // Iniciar animacao de jogar os dados...
    jogo_jogaDados(dadosAtaque.length, dadosDefesa.length, msgParams);
}

function jogo_efetuaAtaque(msgParams) {
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
        
        if (territoriosDoAtaque[i].quantidadeDeTropas == 1) temTerritorioInvalido = true;
        if (territoriosDoAtaque[i].quantidadeDeTropas > 1) fazSentidoMoverAposConquistar = true;
    }

    // Usabilidade...
    if (msgParams.conquistouTerritorio) {
        labelTerritorioDefesa.explosao();
        if (!fazSentidoMoverAposConquistar) {
            setTimeout(function() {
                territorioClickFunc(_posicaoJogador, territorioDaDefesa.codigo)
            }, 1000);
        }
    } else if (temTerritorioInvalido) {
        setTimeout(function() {
            territorioClickFunc(_posicaoJogador, territorioDaDefesa.codigo)
        }, 1000);
    }

    // Usabilidade: Dados do ataque.
    var qtdDadosAtaqueVenceu = 0;
    for (i = 0; i < dadosAtaque.length; i++) {
        if (i < dadosDefesa.length) {
            if (dadosAtaque[i] <= dadosDefesa[i])
                $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
            else {
                ++qtdDadosAtaqueVenceu;
                $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px 0px');
            }
        } else
            $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
    }
    
    // Usabilidade: Dados da defesa.
    for (i = 0; i < dadosDefesa.length; i++) {
        if (i < dadosAtaque.length) {
            if (dadosDefesa[i] < dadosAtaque[i])
                $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
            else {
                $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -40px');
            }
        } else
            $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
    }
    
    // Usabilidade: Resultado dos dados.
    if (qtdDadosAtaqueVenceu >= 1) this.tocarSom(this, 'ganhouNosDados.mp3');
    else this.tocarSom(this, 'perdeuNosDados.mp3');
    
    // Computando ações após conquista de territorio. 
    if (msgParams.conquistouTerritorio) {
        _chatJogo.conquistouTerritorio(
            msgParams.jogadorAtaque.usuario,
            msgParams.territorioDaDefesa.codigo);
    
        this.tocarSom(this, 'conquistar_' + (Math.floor(Math.random()*6)+1) + '.wav');

        _territorioAlvoAtaque = null;
        _territorios.alteraDonoTerritorio(territorioDaDefesa.codigo, msgParams.jogadorAtaque.posicao);
        jogo_aumentaQuantidadeDeTerritorioDoJogador(msgParams.jogadorAtaque.posicao);
        jogo_diminuiQuantidadeDeTerritorioDoJogador(msgParams.jogadorDefesa.posicao);

        if (!fazSentidoMoverAposConquistar) {
            finalizarTurno();
        } else {
            _turno = {};
            _turno["tipoAcao"] = TipoAcaoTurno.mover_apos_conquistar_territorio;
            _territorioConquistado = msgParams.territorioDaDefesa.codigo;
        
            if (_posicaoJogador == _posicaoJogadorDaVez) {
                appwar_mudarCursor('mover_para_fora');
            }
        }
    }
    
    _jaPodeAtacar = true;
}

function processarMsg_jogo_fase_I(msgParams) {
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

    for (i=0; i<msgParams.length; i++) {
        var cartaTerritorio = msgParams[i];
        $('#cartaTerritorio' + (i+1)).attr('class','carta_territorio carta_territorio_' + cartaTerritorio.codigoTerritorio);
    }
}

function processarMsg_carta_objetivo(msgParams) {
    _painelObjetivo = new gpscheck.war.PainelObjetivo(Number(msgParams.objetivo) + 1);
    _painelObjetivo.abre();
}

function processarMsg_colocar_tropa(msgParams) {
    _chatJogo.colocaTropa(msgParams.jogador, msgParams.territorio.codigo, msgParams.quantidade);

    this.tocarSom(this, 'colocarTropa.wav');
    
    if (msgParams.jogador != _usuario) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios([msgParams.territorio.codigo]);
    }
    _territorios.piscar(msgParams.territorio.codigo);
    _labelTerritorios[msgParams.territorio.codigo].alteraQuantiadeDeTropas("" + msgParams.territorio.quantidadeDeTropas);
    
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropasRestante);
    
    if ((msgParams.quantidadeDeTropasRestante == 0) && 
        (msgParams.jogador == _usuario)) {
        finalizarTurno();
    }
}

function processarMsg_atacar(msgParams) {
    if (msgParams.jogadorDefesa.usuario == _usuario) {
        this.tocarSom(this, "ohno.mp3");
        var me = this;
        setTimeout(function() {
            me.jogo_iniciaAnimacaoBatalha(msgParams);
        }, 1500);
    }
    else jogo_iniciaAnimacaoBatalha(msgParams);
}

function processarMsg_mover(msgParams) {
    _chatJogo.moveu(msgParams.jogador, 
        msgParams.doTerritorioObj.codigo, 
        msgParams.paraOTerritorioObj.codigo,
        msgParams.quantidade);

    if (_posicaoJogador == _posicaoJogadorDaVez) {
        appwar_mudarCursor('mover_para_fora');
    }
    
    this.tocarSom(this, 'positivo_' + (Math.floor(Math.random()*4)+1) + '.wav');

    var doTerritorio = msgParams.doTerritorioObj;
    _labelTerritorios[doTerritorio.codigo].alteraQuantiadeDeTropas("" + doTerritorio.quantidadeDeTropas);
    
    var paraOTerritorio = msgParams.paraOTerritorioObj;
    _labelTerritorios[paraOTerritorio.codigo].alteraQuantiadeDeTropas("" + paraOTerritorio.quantidadeDeTropas);
   
    if (_posicaoJogador != _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios([doTerritorio.codigo, paraOTerritorio.codigo]);
    }

    _jaPodeMover = true;

    if (doTerritorio.quantidadeDeTropas == 1 && 
        _posicaoJogador == _posicaoJogadorDaVez &&
        _turno.tipoAcao != TipoAcaoTurno.mover_apos_conquistar_territorio) {
        territorioClickFunc(_posicaoJogador, paraOTerritorio.codigo);
    }
}

function processarMsg_colocar_tropa_na_troca_de_cartas_territorios(msgParams) {
    var territorios = msgParams.territorios;
    for (i = 0; i < territorios.length; i++) {
        _labelTerritorios[territorios[i].codigo].alteraQuantiadeDeTropas("" + territorios[i].quantidadeDeTropas);
    }
}

function processarMsg_entrou_no_jogo(msgParams) {
    var posicaoJogador = Number(msgParams.posicao);
    var usuario = msgParams.usuario;

    if (posicaoJogador > -1) {
        if (usuario != _usuario) _chatJogo.entrouNoJogo(usuario, (posicaoJogador == 7));
        
        if (_posicaoJogador == -1) {
            $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
            $('#painelRegistrarOuEntrar .form-signin').css('visibility', 'hidden');
            _posicaoJogador = posicaoJogador;
            appwar_alterarTituloDaPagina(usuario);
            
            // Olheiro.
            if (posicaoJogador == 7) {
                alert("Este jogo já está em andamento. Você poderá apenas assistí-lo.");
            }
        } else if(posicaoJogador == 7) {
            alert(usuario + " está olhando esta partida.");
        }
        
        $("#jogador" + (posicaoJogador+1)).html(usuario);
    }
}

function processarMsg_saiu_do_jogo(msgParams) {
    this.tocarSom(this, "saindo.wav");
    
    var posicaoJogador = Number(msgParams.posicao) + 1;
    $("#jogador" + posicaoJogador).html("");
    
    _chatJogo.saiuDoJogo(msgParams.usuario, (posicaoJogador == 7));
    
    if (msgParams.usuario == _usuario) {
        _territorios.limpa();
        //appwar_limparVariaveis();
    }
}

function jogo_processaMsg_jogador_destruido(msgParams) {
    setTimeout(function() {
        this.tocarSom(this, "jogadorDestruido.mp3");
        var usuario = msgParams.jogador.usuario;
        if (msgParams.jogador.posicao == _posicaoJogador) usuario = 'Você';
        _painelObjetivo.abreEspecifico(Number(msgParams.jogador.objetivo) + 1,
            usuario + ' foi destruído.');
    }, 2000);
}

function processarMsg_turno(msgParams) {
    _turno = msgParams;
    _posicaoJogadorDaVez = msgParams.vezDoJogador;
    $('#pct_valorDaTroca').html("Valor da troca: " + msgParams.valorDaTroca);
    
    var tempoTotal = Number(msgParams.tempoRestante);
    jogo_iniciaBarraDeProgresso(tempoTotal);
    
    jogo_alteraInfoTurno(TipoAcaoTurno.distribuir_tropas_globais, msgParams);
    
    if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
        processarMsg_turno_distribuir_tropas_globais(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
        processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.trocar_cartas) {
        processarMsg_turno_trocar_cartas(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        processarMsg_turno_distribuir_tropas_globais(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.atacar) {
        processarMsg_turno_atacar(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.mover) {
        processarMsg_turno_mover(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.jogo_terminou) {
        processarMsg_turno_jogo_terminou(msgParams);
    }
}

function processarMsg_turno_distribuir_tropas_globais(msgParams) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        this.tocarSom(this, "buzina.mp3");
        appwar_mudarCursor('colocar_tropa');
    } else {
        appwar_mudarCursor('');
        this.tocarSom(this, "turnoDistribuirTropa.mp3");
    }
    
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
}

function processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        this.tocarSom(this, "turnoDistribuirTropa.mp3");
        appwar_mudarCursor('colocar_tropa');
    } else {
        appwar_mudarCursor('');
    }
    
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.manterFocoNoGrupo(msgParams.grupoTerritorio);
}

function processarMsg_turno_trocar_cartas(msgParams) {
    this.tocarSom(this, "turnoTrocarCarta.mp3");
    
    if (_posicaoJogador == _posicaoJogadorDaVez) 
        appwar_mudarCursor('trocar_cartas');
    else 
        appwar_mudarCursor('');
    
    if (msgParams.obrigatorio && (_posicaoJogador == msgParams.vezDoJogador)) {
        appwar_abrePainelCartasTerritorios();
    }
}

function processarMsg_turno_atacar(msgParams) {
    this.tocarSom(this, 'atacar.wav');
    appwar_alteraQuantidadeDeTropas(0);

    _territorioConquistado = null;
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        appwar_mudarCursor('alvo');
        _territorios.escureceTodosOsTerritoriosDoJogador(msgParams.vezDoJogador);
    } else {
        appwar_mudarCursor('');
    }
}

function processarMsg_turno_mover(msgParams) {
    this.tocarSom(this, 'mover.wav');
    
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        appwar_mudarCursor('mover_para_dentro');
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
    } else {
        appwar_mudarCursor('');
    }
}

function processarMsg_turno_jogo_terminou(msgParams) {
    this.tocarSom(this, 'venceuJogo.wav');
    _painelObjetivo.abreEspecifico(Number(msgParams.objetivo) + 1, 
            msgParams.ganhador + ' venceu o jogo!');
}

function jogo_processaMsg_msg_chat_jogo(msgParams) {
    this.tocarSom(this, 'mensagem.mp3');

    var texto = msgParams.usuario + ": " + msgParams.texto;
    _chatJogo.escreve(texto);
}

/* Informações dos turnos */
function jogo_alteraInfoTurno(tipoAcao, msgParams) {
    $('#it_sub_titulo').css('visibility', 'hidden');
    $('#it_info').css('visibility', 'hidden');

    var posicaoJogador = Number(msgParams.vezDoJogador) + 1;
    if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_tropas' + posicaoJogador);
        $('#it_titulo').html('Distribuir tropas');
        $('#it_sub_titulo').html('Globais');
        $('#it_info').html(msgParams.quantidadeDeTropas);
        $('#it_sub_titulo').css('visibility', 'visible');
        $('#it_info').css('visibility', 'visible');
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_tropas' + posicaoJogador);
        $('#it_titulo').html('Distribuir tropas');
        
        var strGrupoTerritorio = msgParams.grupoTerritorio;
        if (strGrupoTerritorio == "AmericaDoNorte") strGrupoTerritorio = "Am. do Norte";
        else if (strGrupoTerritorio == "AmericaDoSul") strGrupoTerritorio = "Am. do Sul";
        $('#it_sub_titulo').html(strGrupoTerritorio);
        
        $('#it_info').html(msgParams.quantidadeDeTropas);
        $('#it_sub_titulo').css('visibility', 'visible');
        $('#it_info').css('visibility', 'visible');
    } else if (msgParams.tipoAcao == TipoAcaoTurno.trocar_cartas) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_trocar' + posicaoJogador);
        if (msgParams.obrigatorio)
            $('#it_titulo').html('Troca obrigatória');
        else
            $('#it_titulo').html('Trocar?');
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_tropas' + posicaoJogador);
        $('#it_titulo').html('Distribuir tropas');
        $('#it_sub_titulo').html('Globais');
        $('#it_info').html(msgParams.quantidadeDeTropas);
        $('#it_sub_titulo').css('visibility', 'visible');
        $('#it_info').css('visibility', 'visible');
    } else if (msgParams.tipoAcao == TipoAcaoTurno.atacar) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_atacar' + posicaoJogador);
        $('#it_titulo').html('Atacar');
    } else if (msgParams.tipoAcao == TipoAcaoTurno.mover) {
        $('#info_turno').attr('class', '');
        $('#info_turno').addClass('info_turno_mover' + posicaoJogador);
        $('#it_titulo').html('Mover');
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
    if (event.keyCode == 13) {
        jogo_enviaMsgChatDoJogo();
    }
    return true;
}

function jogo_enviaMsgChatDoJogo() {
    var texto = $('#ct_texto').val();
    if (texto.length > 0) {
        $('#ct_texto').val('');
        msg = comunicacao_MsgChatJogo(texto);
        _libwebsocket.enviarObjJson(msg);
    }
}

/* Barra de progresso */
var _loopTempoRestante = null;
var _timeoutTempoRestante = null;

function jogo_iniciaBarraDeProgresso(tempoTotal) {
    var minutosTotal = 2.0 * 60.0;
    
    if (_loopTempoRestante != null || _timeoutTempoRestante != null) {
        clearInterval(_loopTempoRestante);
        clearTimeout(_timeoutTempoRestante);
        _loopTempoRestante = null;
        _timeoutTempoRestante = null;
    }
    $('#barra').width('0%');
    $('#barra').css('background-color','#5eb95e');
    jogo_alteraTempoRestante(tempoTotal);

    var inc = 100.0/minutosTotal;
    var valor = inc * (minutosTotal - tempoTotal);
    var tempo = tempoTotal;
    _loopTempoRestante = setInterval(function() {
        var barra = $('#barra');
        valor += inc;
        barra.width(valor + '%');
        if (valor > 85) {
            barra.css('background-color','#dd514c');
            tocarSom(this, "alarme.mp3");
        }
        else if (valor > 50) barra.css('background-color','#faa732');
        
        tempo -= 1.0;
        jogo_alteraTempoRestante(tempo);
    }, 1000);

    _timeoutTempoRestante = setTimeout(function() {
        if (_loopTempoRestante != null)
            jogo_finalizaBarraDeProgresso();
    }, tempoTotal * 1000);
}

function jogo_alteraTempoRestante(tempo) {
    var minutos = Math.floor(tempo / 60);
    var segundos =  Math.round(tempo % 60);
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
    $('#barra').css('background-color','#dd514c');
    jogo_alteraTempoRestante(0);
}

function jogo_animacaoGanhouCartaTerritorio() {
    $('#ganhou_carta').css('margin-top', '-100px');
    $('#ganhou_carta').css('opacity', '1.0');
    $('#ganhou_carta').css('visibility', 'visible');
    $('#ganhou_carta').animate({
        'margin-top': '132px'
    }, 600, function() {
        $(this).animate({
            opacity: 0.0
        }, 600, function() {
            $('#ganhou_carta').css('visibility', 'hidden');
        });
    });
}

function jogo_sair() {
    msg = comunicacao_sairDaSala();
    _libwebsocket.enviarObjJson(msg);
}

function jogo_removeElementosHtml() {
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#painelRegistrarOuEntrar .form-signin').css('visibility', 'hidden');
    $('#geral').css('visibility', 'hidden');
    $('#jogo').css('visibility', 'hidden');
    $('#it_sub_titulo').css('visibility', 'hidden');
    $('#it_info').css('visibility', 'hidden');
    clearInterval(_loopTempoRestante);
    clearTimeout(_timeoutTempoRestante);   
}
