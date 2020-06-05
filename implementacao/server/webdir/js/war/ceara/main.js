function iniciarApp() {
    _libwebsocket = new gpscheck.comunicacao.GPSWebSocket(8080);
    _libwebsocket.FOnOpen(posAberturaSocket);
    _libwebsocket.FOnMessage(posRecebimentoMensagemServidor);
    _libwebsocket.FOnClose(posFechamentoSocket);
    _libwebsocket.iniciar();

    var divMapa = document.getElementById("mapa");
    mapa = new jogowar.mapa.Mapa();
    mapa.inicia(divMapa, -6.14707264239706, -38.7278609210449, 7);

    _territorios = new jogos.war.Territorios(_mapaGoogle);
    _territorios.inicia(territorioClickFunc, territorioMouseMoveFunc, territorioMouseOutFunc);

    audio_iniciarControleDeAudio();

    _sala = new jogos.war.Sala();
}

(function () {
    iniciarApp();
})();
