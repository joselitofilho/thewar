// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    var listaJogadores = msgParams.lista;
    for (i=0; i < listaJogadores.length; i++) {
        var posicaoJogador = Number(listaJogadores[i]) + 1;
        var divJogador = document.getElementById("jogador" + posicaoJogador);
        divJogador.innerHTML = "Jogador " + posicaoJogador;
    }
}

function processarMsg_entrou_na_sala(msgParams) {
    var divJogador = document.getElementById("idJogador");
    divJogador.innerHTML = "Jogador " + (Number(msgParams.posicao) + 1);

    var btnIniciarPartida = document.getElementById("btnIniciarPartida");
    btnIniciarPartida.style.visibility = (msgParams.dono) ? "visible" : "hidden";
}

function processarMsg_saiu_da_sala(msgParams) {
    var posicaoJogador = Number(msgParams.posicao) + 1;
    var divJogador = document.getElementById("jogador" + posicaoJogador);
    divJogador.innerHTML = "-";
}

function processarMsg_jogo_fase_I(msgParams) {
    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.iniciaLabelDosTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }

    $('#controles').css('visibility', 'visible');

    appwar_alteraInfoTurnoJogador(msgParams.jogadorQueComeca);
}

function processarMsg_carta_objetivo(msgParams) {
    var btnIniciarPartida = document.getElementById("btnIniciarPartida");
    btnIniciarPartida.style.visibility = "hidden";

    var cartaObjetivo = document.getElementById("cartaObjetivo");
    cartaObjetivo.style.visibility = "visible";
    cartaObjetivo.setAttribute('class', 'carta_objetivo carta_objetivo_' + (Number(msgParams.objetivo)+1));
}

function processarMsg_colocar_tropa(msgParams) {
    _labelTerritorios[msgParams.territorio.codigo].alteraQuantiadeDeTropas("" + msgParams.territorio.quantidadeDeTropas);
    $('#quantidade_de_tropas').html('Quantidade de tropas a colocar: ' + msgParams.quantidadeDeTropasRestante);
}

function processarMsg_turno(msgParams) {
    appwar_alteraInfoTurnoJogador(msgParams.vezDoJogador);
    if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
        processarMsg_turno_distribuir_tropas_globais(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
        processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.atacar) {
        processarMsg_turno_atacar(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.mover) {
        processarMsg_turno_mover(msgParams);
    }
}

function processarMsg_turno_distribuir_tropas_globais(msgParams) {
    $('#info_turno_texto').html('Distribuir tropas globais');
    $('#quantidade_de_tropas').html('Quantidade de tropas a colocar: ' + msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
}

function processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams) {
    var strGrupoTerritorio = msgParams.grupoTerritorio;
    if (strGrupoTerritorio == "AmericaDoNorte") strGrupoTerritorio = "Am. do Norte";
    else if (strGrupoTerritorio == "AmericaDoSul") strGrupoTerritorio = "Am. do Sul";
    $('#info_turno_texto').html('Distribuir tropas na ' + strGrupoTerritorio);
    $('#quantidade_de_tropas').html('Quantidade de tropas a colocar: ' + msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.manterFocoNoGrupo(msgParams.grupoTerritorio);
}

function processarMsg_turno_atacar(msgParams) {
    $('#info_turno_texto').html('Atacar');
    _territorios.pintarGruposTerritorios();
}

function processarMsg_turno_mover(msgParams) {
    $('#info_turno_texto').html('Mover');
}

////////////////////////////////////////////////////////////////////////////////
// Métodos utilizados na biblioteca de WebSocket
////////////////////////////////////////////////////////////////////////////////

function posAberturaSocket(valor) {
    //console.log('Conexão socket iniciada.');
}

function posRecebimentoMensagemServidor(valor) {
    console.log('Recebeu msg ' + valor);
    var jsonMensagem = JSON.parse(valor);
    if (jsonMensagem.tipo == TipoMensagem.lista_sala) {
        processarMsg_lista_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.entrou_na_sala) {
        processarMsg_entrou_na_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.saiu_da_sala) {
        processarMsg_saiu_da_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.jogo_fase_I) {
        processarMsg_jogo_fase_I(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carta_objetivo) {
        processarMsg_carta_objetivo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.colocar_tropa) {
        processarMsg_colocar_tropa(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.turno) {
        processarMsg_turno(jsonMensagem.params);
    }
}

function posFechamentoSocket(valor) {
    alert("Voce perdeu a conexao com o servidor. Reinicie o browser.");
}

function iniciarPartida() {
    var btnIniciarPartida = document.getElementById("btnIniciarPartida");
    btnIniciarPartida.disabled = true;
    iniciarPartidaMsg = new Mensagem(TipoMensagem.iniciar_partida, null);
    _libwebsocket.enviarObjJson(iniciarPartidaMsg);
}

function finalizarTurno() {
    finalizarPartidaMsg = new Mensagem(TipoMensagem.finalizar_turno, null);
    _libwebsocket.enviarObjJson(finalizarPartidaMsg);
}

function atacar() {
    atacarMsg = new Mensagem(TipoMensagem.atacar,
    {
        posicaoJogador: 0,
        dosTerritorios: ["Brasil"],
        paraOTerritorio: "Chile"
    });
    _libwebsocket.enviarObjJson(atacarMsg);
}

function mover() {
    moverMsg = new Mensagem(TipoMensagem.mover,
    {
        posicaoJogador: 0,
        doTerritorio: "Brasil",
        paraOTerritorio: "Chile",
        quantidade: 1
    }); 
    _libwebsocket.enviarObjJson(moverMsg);
}

function adicionaExercitoNoClickDo(poligono) {
    google.maps.event.addListener(poligono, 'click', function (event) {
        var markermap = new google.maps.Marker({
            position: event.latLng,
            map: _mapaGoogle,
            title: "Exercitos: "
        });
    });
}

function appwar_alteraInfoTurnoJogador(posicaoJogador) {
    var divInfoTurnoJogador = $('#info_turno_jogador');
    switch (posicaoJogador) {
        case 0:
            divInfoTurnoJogador.css('background-position', '0px 0px');
            break;
        case 1:
            divInfoTurnoJogador.css('background-position', '-60px 0px');
            break;
        case 2:
            divInfoTurnoJogador.css('background-position', '-120px 0px');
            break;
        case 3:
            divInfoTurnoJogador.css('background-position', '-180px 0px');
            break;
        case 4:
            divInfoTurnoJogador.css('background-position', '-240px 0px');
            break;
        case 5:
            divInfoTurnoJogador.css('background-position', '-300px 0px');
            break;
    }
}

function iniciarApp() {
    _libwebsocket = new gpscheck.comunicacao.GPSWebSocket(9002);
    _libwebsocket.FOnOpen(posAberturaSocket);
    _libwebsocket.FOnMessage(posRecebimentoMensagemServidor);
    _libwebsocket.FOnClose(posFechamentoSocket);
    _libwebsocket.iniciar();

    var divMapa = document.getElementById("mapa");
    mapa = new gpscheck.mapa.Mapa();
    mapa.inicia(divMapa, 10.0, 10.0);
    _territorios = new gpscheck.mapa.Territorios(_mapaGoogle);
    _territorios.desenha();
}

(function(){
    iniciarApp();
})();
