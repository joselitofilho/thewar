_posicaoJogador = -1;
_turno = null;
_posicaoJogadorDaVez = -1;
_territorioAlvoAtaque = null;
_territoriosAtacante = [];

_territorioAlvoMover = null;
_territorioMovimento = null;

_animarDadosReferencia = null;

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_lista_sala(msgParams) {
    var listaJogadores = msgParams.lista;
    for (i=0; i < listaJogadores.length; i++) {
        var posicaoJogador = Number(listaJogadores[i]) + 1;
        $("#jogador" + posicaoJogador).html(posicaoJogador);
    }
}

function processarMsg_entrou_na_sala(msgParams) {
    $("#idJogador").html(Number(msgParams.posicao) + 1);
    
    _posicaoJogador = Number(msgParams.posicao);

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
    
    $('#btnIniciarPartida').css('visibility', 'hidden');
    $('#controles').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');

    appwar_alteraInfoTurnoJogador(msgParams.jogadorQueComeca);
}

function processarMsg_carta_objetivo(msgParams) {
    $('#cartaObjetivo').attr('class', 'carta_objetivo carta_objetivo_' + (Number(msgParams.objetivo)+1));
}

function processarMsg_colocar_tropa(msgParams) {
    _labelTerritorios[msgParams.territorio.codigo].alteraQuantiadeDeTropas("" + msgParams.territorio.quantidadeDeTropas);
    $('#quantidade_de_tropas').html(msgParams.quantidadeDeTropasRestante);
}

function processarMsg_atacar(msgParams) {
    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;
    
    _territorios.pintarGruposTerritorios();
        
    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;
    var codigoTerritorios = [territorioDaDefesa.codigo];
            
    _labelTerritorios[territorioDaDefesa.codigo].alteraQuantiadeDeTropas("" + territorioDaDefesa.quantidadeDeTropas);
    
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        codigoTerritorios.push(territoriosDoAtaque[i].codigo);
        _labelTerritorios[territoriosDoAtaque[i].codigo].alteraQuantiadeDeTropas("" + territoriosDoAtaque[i].quantidadeDeTropas);
    }
    _territorios.focaNosTerritorios(codigoTerritorios);
    
    for (i = 0; i < dadosAtaque.length; i++) {
        $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px 0px');
    }
    
    for (i = 0; i < dadosDefesa.length; i++) {
        $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -40px');
    }
    
    if (msgParams.conquistouTerritorio) {
        _turno = {};
        _turno["tipoAcao"] = TipoAcaoTurno.mover_apos_conquistar_territorio;
        
        _territorios.alteraDonoTerritorio(territorioDaDefesa.codigo, msgParams.posicaoJogador);
    }
}

function processarMsg_atacar_comDados(msgParams) {
    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;
    
    // Iniciar animacao de jogar os dados...
    jogarDados(dadosAtaque.length, dadosDefesa.length, msgParams);
}

function processarMsg_mover(msgParams) {
    var doTerritorio = msgParams.doTerritorioObj;
    _labelTerritorios[doTerritorio.codigo].alteraQuantiadeDeTropas("" + doTerritorio.quantidadeDeTropas);
    
    var paraOTerritorio = msgParams.paraOTerritorioObj;
    _labelTerritorios[paraOTerritorio.codigo].alteraQuantiadeDeTropas("" + paraOTerritorio.quantidadeDeTropas);
}

function processarMsg_cartas_territorios(msgParams) {
    for (i=0; i<msgParams.length; i++) {
        var cartaTerritorio = msgParams[i];
        $('#cartaTerritorio' + (i+1)).attr('class','carta_territorio carta_territorio_' + cartaTerritorio.codigoTerritorio);
    }
}

function processarMsg_turno(msgParams) {
    _turno = msgParams;
    _posicaoJogadorDaVez = msgParams.vezDoJogador;
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
    $('#quantidade_de_tropas').html(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
}

function processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams) {
    var strGrupoTerritorio = msgParams.grupoTerritorio;
    if (strGrupoTerritorio == "AmericaDoNorte") strGrupoTerritorio = "Am. do Norte";
    else if (strGrupoTerritorio == "AmericaDoSul") strGrupoTerritorio = "Am. do Sul";
    $('#info_turno_texto').html('Distribuir tropas na ' + strGrupoTerritorio);
    $('#quantidade_de_tropas').html(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.manterFocoNoGrupo(msgParams.grupoTerritorio);
}

function processarMsg_turno_atacar(msgParams) {
    $('#info_turno_texto').html('Atacar');
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        _territorios.escureceTodosOsTerritoriosDoJogador(msgParams.vezDoJogador);
    }
}

function processarMsg_turno_mover(msgParams) {
    $('#info_turno_texto').html('Mover');
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
    }
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
    } else if (jsonMensagem.tipo == TipoMensagem.atacar) {
        processarMsg_atacar_comDados(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.mover) {
        processarMsg_mover(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.cartas_territorios) {
        processarMsg_cartas_territorios(jsonMensagem.params);
    }
}

function posFechamentoSocket(valor) {
    alert("Voce perdeu a conexao com o servidor. Reinicie o browser.");
}

function iniciarPartida() {
    var btnIniciarPartida = document.getElementById("btnIniciarPartida");
    btnIniciarPartida.disabled = true;
    iniciarPartidaMsg = comunicacao_iniciarPartida();
    _libwebsocket.enviarObjJson(iniciarPartidaMsg);
}

function finalizarTurno() {
    finalizarPartidaMsg = comunicacao_finalizarTurno();
    _libwebsocket.enviarObjJson(finalizarPartidaMsg);
}

function atacar() {
    if (_posicaoJogadorDaVez == _posicaoJogador) {
        var territorios = [];
        var qtdDadosDefesa = _territorios.quantidadeDeTropaDoTerritorio(_territorioAlvoAtaque);
        var qtdDadosAtaque = 0;
        territorios.push(_territorioAlvoAtaque);
        
        $.each(_territoriosAtacante, function(i, codigoTerritorio) {
            var qtdTropas = _territorios.quantidadeDeTropaDoTerritorio(codigoTerritorio);
            if (qtdTropas <= 3 && qtdTropas > 0) {
                qtdDadosAtaque += qtdTropas - 1;
            } else {
                qtdDadosAtaque += qtdTropas;
            }
            territorios.push(codigoTerritorio);
        });
        
        var bounds = _territorios.barreiraDosTerritorios(territorios);
        // TODO: Desabilitar quando a idéia estiver mais amadurecida...
        //_mapaGoogle.fitBounds(bounds);
        
        if (qtdDadosDefesa > 0 && qtdDadosAtaque > 0) {     
            var atacarMsg = comunicacao_atacar(_posicaoJogador, _territorioAlvoAtaque, _territoriosAtacante);
            _libwebsocket.enviarObjJson(atacarMsg);
        }
    }
}

function mostrarCartaObjetivo() {
    if ($('#cartaObjetivo').css("visibility") == 'visible') {
        $('#cartaObjetivo').css('visibility', 'hidden');
    } else {
        $('#cartaObjetivo').css('visibility', 'visible');
    }
}

function mostrarCartasTerritorios() {
    if ($('#cartasTerritorios').css("visibility") == 'visible') {
        $('#cartasTerritorios').css('visibility', 'hidden');
    } else {
        $('#cartasTerritorios').css('visibility', 'visible');
    }
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

function territorioClickFunc(posicaoJogador, nomeDoTerritorio, quantidade) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        if (_turno.tipoAcao == TipoAcaoTurno.atacar) {
            if (nomeDoTerritorio == _territorioAlvoAtaque) {
                _territorios.pintarGruposTerritorios();
                _territorios.escureceTodosOsTerritoriosDoJogador(_posicaoJogador);
                _territorioAlvoAtaque = null;
                _territoriosAtacante = [];
            }
            else if (_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                _territorios.pintarGruposTerritorios();
                _territorioAlvoAtaque = nomeDoTerritorio;
                _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                _territoriosAtacante = [];
            }
            else if (_territorioAlvoAtaque != null) {
                if (_territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1) {
                    var indiceTerritorio = _territoriosAtacante.indexOf(nomeDoTerritorio);
                    if (indiceTerritorio == -1) {
                        _territoriosAtacante.push(nomeDoTerritorio);
                        _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                    } else {
                        _territoriosAtacante.splice(indiceTerritorio, 1);
                        _territorios.diminuiBrilhoTerritorio(nomeDoTerritorio);
                    }
                }
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio) {
            var moverMsg = comunicacao_mover(_posicaoJogador, nomeDoTerritorio, 
                _territorioAlvoAtaque, 1);
            _libwebsocket.enviarObjJson(moverMsg);
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
            if (!_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                if (nomeDoTerritorio == _territorioAlvoMover) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = null;
                    _territorioMovimento = null;
                }
                else if (_territorioAlvoMover == null) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                } else if (_territorioMovimento == null) {
                    _territorioMovimento = nomeDoTerritorio;
                    _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                } else if(_territorioMovimento == nomeDoTerritorio) {
                    var moverMsg = comunicacao_mover(_posicaoJogadorDaVez, nomeDoTerritorio, 
                        _territorioAlvoMover, 1);
                    _libwebsocket.enviarObjJson(moverMsg);
                } else {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                    _territorioMovimento = null;
                }
            }
        } else {
            var colocarTropaMsg = comunicacao_colocarTropa(posicaoJogador, nomeDoTerritorio, quantidade);
            _libwebsocket.enviarObjJson(colocarTropaMsg);
        }
    }
}

function jogarDados(qtdDadosAtaque, qtdDadosDefesa, msgParams) {
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
            setTimeout(function() { pararAnimacaoDosDados(msgParams); }, 1500);
        }
    } catch(ex) {
        console.log("Error in fnTimer:\n" + ex);
    }
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
        
        processarMsg_atacar(msgParams);
    } catch(ex) {
        console.log("Error in fnTimer:\n" + ex);
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
    _territorios.inicia(territorioClickFunc);
}

(function(){
    iniciarApp();
})();
