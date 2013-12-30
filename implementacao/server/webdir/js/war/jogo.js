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
    $('#quantidade_de_tropas').css('visibility', 'visible');

    appwar_alteraInfoTurnoJogador(msgParams.jogadorQueComeca);
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
    $('#quantidade_de_tropas').css('visibility', 'visible');

    processarMsg_carta_objetivo(msgParams);
    processarMsg_cartas_territorios(msgParams.cartasTerritorio);

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;
    appwar_alteraInfoTurnoJogador(msgParams.jogadorDaVez);

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
    $('#quantidade_de_tropas').css('visibility', 'visible');

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;
    appwar_alteraInfoTurnoJogador(msgParams.jogadorDaVez);

    $('#bloqueador_tela').css('visibility', 'hidden');
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

/* Territorios */
function jogo_alteraQuantidadeDeTerritoriosPorJogador(territorios, posicao) {
    $('#qtdTerritorio' + posicao).html(territorios.length);
}

function jogo_diminuiQuantidadeDeTerritorioDoJogador(posicao) {
    var valor = Number($('#qtdTerritorio' + posicao).html()) - 1;
    if (valor > 0) $('#qtdTerritorio' + posicao).html(valor);
}

function jogo_aumentaQuantidadeDeTerritorioDoJogador(posicao) {
    var valor = Number($('#qtdTerritorio' + posicao).html()) + 1;
    if (valor < 42) $('#qtdTerritorio' + posicao).html(valor);
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
