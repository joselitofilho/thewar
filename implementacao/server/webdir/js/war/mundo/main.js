function iniciarApp() {
    _libwebsocket = new gpscheck.comunicacao.GPSWebSocket(8080);
    _libwebsocket.FOnOpen(posAberturaSocket);
    _libwebsocket.FOnMessage(posRecebimentoMensagemServidor);
    _libwebsocket.FOnClose(posFechamentoSocket);
    _libwebsocket.iniciar();

    var divMapa = document.getElementById("mapa");
    mapa = new jogowar.mapa.Mapa();
    mapa.inicia(divMapa, 10.0, 10.0, 2);
    //this.tocarSomDeFundo(divMapa);

    _territorios = new jogos.war.Territorios(_mapaGoogle);
    _territorios.inicia(territorioClickFunc, territorioMouseMoveFunc, territorioMouseOutFunc);
        
    iniciarControleDeAudio();

    _sala = new jogos.war.Sala();
}

(function(){
    iniciarApp();
})();
