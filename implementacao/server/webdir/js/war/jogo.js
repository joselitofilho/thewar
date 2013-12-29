function ct_texto_onkeypress(event) {
    if (event.keyCode == 13) {
        jogo_enviaMsgChatDoJogo();
    }
    return true;
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

function jogo_enviaMsgChatDoJogo() {
    var texto = $('#ct_texto').val();
    if (texto.length > 0) {
        $('#ct_texto').val('');
        msg = comunicacao_MsgChatJogo(texto);
        _libwebsocket.enviarObjJson(msg);
    }
}


/* Barra de progresso */
function jogo_iniciaBarraDeProgresso() {
    var tempoTotal = 1.0*60.0;
    var valor = 0.0;
    loopTempoRestante = setInterval(function() {
        var barra = $('#barra');
        valor += 100.0/tempoTotal;
        barra.width(valor + '%');
        if (valor > 85) barra.css('background-color','#dd514c');
        else if (valor > 50) barra.css('background-color','#faa732');
        
        var tempo = tempoTotal - (tempoTotal*valor / 100.0);
        if (tempo > 60)
            $('#tempo_restante').html(Math.round(tempo / 60) + ' min');
        else 
            $('#tempo_restante').html(Math.round(tempo) + ' seg');
    }, 1000);

    setTimeout(function(){
        clearInterval(loopTempoRestante);
        $('#barra').width('100%');
        $('#barra').css('background-color','#dd514c');
        $('#tempo_restante').html('0 seg');
    }, tempoTotal * 1000);
}
