function processarMsg_jogo_fase_I(msgParams) {
    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.iniciaLabelDosTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }
    
    $('#sala').css('visibility', 'hidden');
    $('#btnIniciarPartida').css('visibility', 'hidden');
    $('#menu_jogadores').css('visibility', 'visible');
    $('#controles').css('visibility', 'visible');
    $('#info_turno').css('visibility', 'visible');
    $('#btnFinalizarTurno').css('visibility', 'visible');
    $('#barra_tempo').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');
}

function processarMsg_carrega_jogo(msgParams) {
    processarMsg_lista_sala(msgParams);

    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }
    
    $('#menu_jogadores').css('visibility', 'visible');
    $('#controles').css('visibility', 'visible');
    $('#btnFinalizarTurno').css('visibility', 'visible');
    $('#barra_tempo').css('visibility', 'visible');
    $('#info_turno').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');

    processarMsg_carta_objetivo(msgParams);
    processarMsg_cartas_territorios(msgParams.cartasTerritorio);

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;

    $('#bloqueador_tela').css('visibility', 'hidden');
}

function processarMsg_carrega_jogo_olheiro(msgParams) {
    processarMsg_lista_sala(msgParams);

    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
        jogo_alteraQuantidadeDeTerritoriosPorJogador(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }
    
    $('#menu_jogadores').css('visibility', 'visible');
    $('#controles').css('visibility', 'visible');
    $('#btnFinalizarTurno').css('visibility', 'visible');
    $('#barra_tempo').css('visibility', 'visible');
    $('#info_turno').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;

    $('#bloqueador_tela').css('visibility', 'hidden');
}

function processarMsg_cartas_territorios(msgParams) {
    if (msgParams.length > 0) {
        this.tocarSom(this, "ganhouCarta.mp3");
        jogo_animacaoGanhouCartaTerritorio();
    }

    appwar_iniciaCartasTerritorios();

    for (i=0; i<msgParams.length; i++) {
        var cartaTerritorio = msgParams[i];
        $('#cartaTerritorio' + (i+1)).attr('class','carta_territorio carta_territorio_' + cartaTerritorio.codigoTerritorio);
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
    this.tocarSom(this, "turnoTrocarCarta.wav");
    
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

    var texto = msgParams.usuario + ": " + msgParams.texto + "\n";
    $('#ct_mensagens').append(texto);
    
    var mensagens = $('#ct_mensagens');
    mensagens.scrollTop(
        mensagens[0].scrollHeight - mensagens.height()
    );
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

    var valor = (100.0 / minutosTotal) * (minutosTotal - tempoTotal);
    var tempo = tempoTotal;
    _loopTempoRestante = setInterval(function() {
        var barra = $('#barra');
        valor += 100.0/minutosTotal;
        barra.width(valor + '%');
        if (valor > 85) barra.css('background-color','#dd514c');
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
