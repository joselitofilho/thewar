_posicaoJogador = -1;
_turno = null;
_posicaoJogadorDaVez = -1;

_territorioAlvoAtaque = null;
_territoriosAtacante = [];
_jaPodeAtacar = true;

_territorioAlvoMover = null;
_territorioMovimento = null;
_jaPodeMover = true;

_animarDadosReferencia = null;

_cartasTerritoriosSelecionadas = [];

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
    
    if ((msgParams.quantidadeDeTropasRestante == 0) && 
        (msgParams.posicaoJogador == _posicaoJogador)) {
        finalizarTurno();
    }
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
    
    _jaPodeAtacar = true;
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
    
    _jaPodeMover = true;
}

function processarMsg_cartas_territorios(msgParams) {
    appwar_iniciaCartasTerritorios();

    for (i=0; i<msgParams.length; i++) {
        var cartaTerritorio = msgParams[i];
        $('#cartaTerritorio' + (i+1)).attr('class','carta_territorio carta_territorio_' + cartaTerritorio.codigoTerritorio);
    }
}

function processarMsg_colocar_tropa_na_troca_de_cartas_territorios(msgParams) {
    var territorios = msgParams.territorios;
    for (i = 0; i < territorios.length; i++) {
        _labelTerritorios[territorios[i].codigo].alteraQuantiadeDeTropas("" + territorios[i].quantidadeDeTropas);
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
    } else if (msgParams.tipoAcao == TipoAcaoTurno.trocar_cartas) {
        processarMsg_turno_trocar_cartas(msgParams);
    } else if (msgParams.tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        processarMsg_turno_distribuir_tropas_globais(msgParams);
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

function processarMsg_turno_trocar_cartas(msgParams) {
    $('#info_turno_texto').html('Trocar cartas');
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
    } else if (jsonMensagem.tipo == TipoMensagem.colocar_tropa_na_troca_de_cartas_territorios) {
        processarMsg_colocar_tropa_na_troca_de_cartas_territorios(jsonMensagem.params);
    }
}

function posFechamentoSocket(valor) {
    //alert("Você perdeu a conexao com o servidor. Reinicie o browser.");
    $('#bloqueador_tela').css('visibility', 'visible');
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#botao_recarregar').css('visibility', 'visible');
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
        
        if (qtdDadosDefesa > 0 && qtdDadosAtaque > 0 && _jaPodeAtacar) {
            _jaPodeAtacar = false;
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

function selecionarCartaTerritorio(num) {
    var nomeDoElemento = '#cartaTerritorio' + num;
    var classesDoElemento = $(nomeDoElemento).attr('class').split(' ');
    
    if (classesDoElemento.length > 1 && 
        classesDoElemento[1] != 'carta_territorio_vazia') {
        var nomeDividido = classesDoElemento[1].split('_');
        if (_cartasTerritoriosSelecionadas.length < 3 && nomeDividido.length == 3) {
            // Carta não estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(classesDoElemento[1] + '_selecionado');
            
            _cartasTerritoriosSelecionadas.push(nomeDividido[2]);
        } else if (_cartasTerritoriosSelecionadas.length > 0 && nomeDividido.length == 4) {
            // Carta estava selecionada.
            $(nomeDoElemento).removeClass(classesDoElemento[1]);
            $(nomeDoElemento).addClass(nomeDividido[0] + '_' + nomeDividido[1] + '_' + nomeDividido[2]);
            
            _cartasTerritoriosSelecionadas.splice(_cartasTerritoriosSelecionadas.indexOf(nomeDividido[2]), 1);
        }
    }
}

function trocarCartasTerritorios() {
    if (_cartasTerritoriosSelecionadas.length == 3) {
        var msg = comunicacao_trocar_cartas_territorio(_posicaoJogador, _cartasTerritoriosSelecionadas);
        _libwebsocket.enviarObjJson(msg);
    }
}

function appwar_iniciaCartasTerritorios() {
    _cartasTerritoriosSelecionadas = [];

    for (i=1; i<=5; i++) {
        $('#cartaTerritorio' + i).attr('class','carta_territorio carta_territorio_vazia');
    }
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
            if (_territorioAlvoAtaque == nomeDoTerritorio) {
                finalizarTurno();
            } else {
                var moverMsg = comunicacao_mover(_posicaoJogador, nomeDoTerritorio, 
                    _territorioAlvoAtaque, 1);
                _libwebsocket.enviarObjJson(moverMsg);
                _jaPodeMover = false;
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
            if (!_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                if (nomeDoTerritorio == _territorioAlvoMover) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = null;
                    _territorioMovimento = null;
                } else if (_territorioAlvoMover == null) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                } else if (_territorioMovimento == null && _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1) {
                    _territorioMovimento = nomeDoTerritorio;
                    _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                } else if(_territorioMovimento == nomeDoTerritorio) {
                    var moverMsg = comunicacao_mover(_posicaoJogadorDaVez, nomeDoTerritorio, 
                        _territorioAlvoMover, 1);
                    _libwebsocket.enviarObjJson(moverMsg);
                    _jaPodeMover = false;
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

function appwar_entrar() {
    var entrarMsg = comunicacao_entrar($('#inputUsuario').val(), $('#inputSenha').val());
    _libwebsocket.enviarObjJson(entrarMsg);
}

function appwar_registrar() {
    var registrarMsg = comunicacao_registrar($('#inputUsuario').val(), $('#inputSenha').val());
    _libwebsocket.enviarObjJson(registrarMsg);
}

function appwar_recarregarPagina() {
    location.reload();
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
