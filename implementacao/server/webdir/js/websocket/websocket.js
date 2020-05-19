var gpscheck = gpscheck || {};
gpscheck.comunicacao = gpscheck.comunicacao || {};

/**
 * Classe que implementa as funções do websocket.  o websocket.
 *
 * @param porta de comunicação websocket.
 */
gpscheck.comunicacao.GPSWebSocket = function (porta) {
    _fOnOpen = null;
    _fOnClose = null;
    _fOnMessage = null;
    _fOnError = null;
    _ws = null;
    _porta = porta;

    this.FOnOpen = function (val) {
        _fOnOpen = val;
    };

    this.FOnClose = function (val) {
        _fOnClose = val;
    };

    this.FOnMessage = function (val) {
        _fOnMessage = val;
    };

    this.FOnError = function (val) {
        _fOnError = val;
    };

    this.iniciar = function () {
        var wsuri;

        if (window.location.protocol === "file:") {
            wsuri = "ws://localhost:" + _porta;
        } else {
            wsuri = "ws://" + window.location.hostname + ":" + _porta;
        }

        if ("WebSocket" in window) {
            _ws = new WebSocket(wsuri);
        } else if ("MozWebSocket" in window) {
            _ws = new MozWebSocket(wsuri);
        } else {
            console.log("Browser does not support WebSocket!");
            if (_fOnError != null) this.fOnError("Browser does not support WebSocket!");
        }

        if (_ws) {
            _ws.onopen = function () {
                console.log("Conectado em: " + wsuri);
                if (_fOnOpen != null) _fOnOpen();
            };

            _ws.onclose = function (e) {
                console.log("Conexão fechou (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
                _ws = null;
                if (_fOnClose != null) _fOnClose(e.data);
            };

            _ws.onmessage = function (e) {
                if (_fOnMessage != null) _fOnMessage(e.data);
            }
        }
    };

    /**
     * Envia uma mensagem para o servidor.
     */
    this.enviar = function (msg) {
        if (_ws) _ws.send(msg);
    };

    /**
     * Envia um objeto no formato JSON para o servidor.
     */
    this.enviarObjJson = function (obj) {
        this.enviar(JSON.stringify(obj));
    }
};
