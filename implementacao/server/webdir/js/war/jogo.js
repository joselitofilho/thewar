function ct_texto_onkeypress(event) {
    if (event.keyCode == 13) {
        jogo_enviaMsgChatDoJogo();
    }
    return true;
}

function jogo_processaMsg_msg_chat_jogo(msgParams) {
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
