function iniciarApp() {
    _libwebsocket = new gpscheck.comunicacao.GPSWebSocket(8080);
    _libwebsocket.FOnOpen(posAberturaSocket);
    _libwebsocket.FOnMessage(posRecebimentoMensagemServidor);
    _libwebsocket.FOnClose(posFechamentoSocket);
    _libwebsocket.iniciar();

    var divMapa = document.getElementById("mapa");
    mapa = new jogowar.mapa.Mapa();
    mapa.inicia(divMapa, 25.0, 10.0, 2);

    var estiloDoMapa = [
        {
            "featureType": "water",
            "stylers": [{"visibility": "off"}]
        },
        {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [{"visibility": "off"}]
        },
        {
            "featureType": "landscape.natural.landcover",
            "elementType": "geometry",
            "stylers": [{"visibility": "off"}]
        },
        {
            "featureType": "administrative",
            "stylers": [{"visibility": "off"}]
        }
    ];
    mapa.alteraEstilo(estiloDoMapa);

    _territorios = new jogos.war.Territorios(_mapaGoogle);
    _territorios.inicia(territorioClickFunc, territorioMouseMoveFunc, territorioMouseOutFunc);

    _mapaGoogle.setOptions({draggableCursor: "url(../../../imagens/mouse/padrao.png), auto"})
}

(function () {
    iniciarApp();
})();
