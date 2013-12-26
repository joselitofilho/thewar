//
// http://soundbible.com/tags-war.html
//

_posicaoJogador = -1;
_turno = null;
_posicaoJogadorDaVez = -1;

_territorioAlvoAtaque = null;
_territoriosAtacante = [];
_jaPodeAtacar = true;

_territorioConquistado = null;

_territorioAlvoMover = null;
_territorioMovimento = null;
_jaPodeMover = true;

_animarDadosReferencia = null;

_cartasTerritoriosSelecionadas = [];

_quantidadeDeJogadoreNaSala = 0;

function exibirAlerta(tipo, msg) {
    $('#alerta').removeClass('alert-info alert-success alert-warning alert-danger');
    $('#alerta').addClass(tipo);
    $('#alerta_texto').html(msg);
    $('#alerta').css('visibility', 'visible');
    $("#alerta")
        .fadeIn('slow')
        .animate({opacity : 1.0}, 2000)
        .fadeOut('slow', function() {
            $(this).hide();
        });
}

// --------------------------------------------------------------------------------
// Processando mensagens recebidas do servidor.
// --------------------------------------------------------------------------------
function processarMsg_registrar(msgParams) {
    if (msgParams.status == 1) {
        exibirAlerta('alert-success', 'Registrado com sucesso.');
    } else if (msgParams.status == 0) {
        exibirAlerta('alert-info', 'Voce ja esta registrado.');
    }
}

function processarMsg_entrar(msgParams) {
    if (msgParams.status != 1) {
        exibirAlerta('alert-danger', 'Verifique se seus dados estao corretos e tente novamente.');
    } 
}

function processarMsg_jogo_fase_I(msgParams) {
    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.iniciaLabelDosTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }
    
    $('#sala').css('visibility', 'hidden');
    $('#btnIniciarPartida').css('visibility', 'hidden');
    $('#controles').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');

    appwar_alteraInfoTurnoJogador(msgParams.jogadorQueComeca);
}

function processarMsg_carta_objetivo(msgParams) {
    $('#cartaObjetivo').attr('class', 'carta_objetivo carta_objetivo_' + (Number(msgParams.objetivo)+1));
}

function processarMsg_colocar_tropa(msgParams) {
    this.tocarSom(this, 'colocarTropa.mp3');
    _territorios.piscar(msgParams.territorio.codigo);
    _labelTerritorios[msgParams.territorio.codigo].alteraQuantiadeDeTropas("" + msgParams.territorio.quantidadeDeTropas);
    
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropasRestante);
    
    if ((msgParams.quantidadeDeTropasRestante == 0) && 
        (msgParams.posicaoJogador == _posicaoJogador)) {
        finalizarTurno();
    }
}

function processarMsg_atacar(msgParams) {
    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;

    var diferencaDeQuantidade = 0;

    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;i

    var labelTerritorioDefesa = _labelTerritorios[territorioDaDefesa.codigo];
    diferencaDeQuantidade = Number(labelTerritorioDefesa.texto) - territorioDaDefesa.quantidadeDeTropas;
    if (!msgParams.conquistouTerritorio)
        labelTerritorioDefesa.perdeuTropas(diferencaDeQuantidade);
    labelTerritorioDefesa.alteraQuantiadeDeTropas("" + territorioDaDefesa.quantidadeDeTropas);
    
    var temTerritorioInvalido = false;
    var fazSentidoMoverAposConquistar = false;
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        var labelTerritorioAtaque = _labelTerritorios[territoriosDoAtaque[i].codigo];
        diferencaDeQuantidade = Number(labelTerritorioAtaque.texto) - territoriosDoAtaque[i].quantidadeDeTropas;
        if (!msgParams.conquistouTerritorio)
            labelTerritorioAtaque.perdeuTropas(diferencaDeQuantidade);
        labelTerritorioAtaque.alteraQuantiadeDeTropas("" + territoriosDoAtaque[i].quantidadeDeTropas);
        
        if (territoriosDoAtaque[i].quantidadeDeTropas == 1) temTerritorioInvalido = true;
        if (territoriosDoAtaque[i].quantidadeDeTropas > 1) fazSentidoMoverAposConquistar = true;
    }

    if (msgParams.conquistouTerritorio) {
        labelTerritorioDefesa.explosao();
        if (!fazSentidoMoverAposConquistar) {
            setTimeout(function() {
                territorioClickFunc(_posicaoJogador, territorioDaDefesa.codigo)
            }, 1000);
        }
    } else if (temTerritorioInvalido) {
        setTimeout(function() {
            territorioClickFunc(_posicaoJogador, territorioDaDefesa.codigo)
        }, 1000);
    }

    for (i = 0; i < dadosAtaque.length; i++) {
        if (i < dadosDefesa.length) {
            if (dadosAtaque[i] <= dadosDefesa[i])
                $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
            else
                $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px 0px');
        } else
            $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
    }
    
    for (i = 0; i < dadosDefesa.length; i++) {
        if (i < dadosAtaque.length) {
            if (dadosDefesa[i] < dadosAtaque[i])
                $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
            else
                $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -40px');    
        } else
            $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
    }
    
    if (msgParams.conquistouTerritorio) {
        this.tocarSom(this, 'conquistar_' + (Math.floor(Math.random()*6)+1) + '.wav');

        _territorioAlvoAtaque = null;
        _territorios.alteraDonoTerritorio(territorioDaDefesa.codigo, msgParams.posicaoJogador);

        if (!fazSentidoMoverAposConquistar) {
            finalizarTurno();
        } else {
            _turno = {};
            _turno["tipoAcao"] = TipoAcaoTurno.mover_apos_conquistar_territorio;
            _territorioConquistado = msgParams.territorioDaDefesa.codigo;
        
            if (_posicaoJogador == _posicaoJogadorDaVez) {
                appwar_mudarCursor('mover_para_fora');
            }
        }
    }
    
    _jaPodeAtacar = true;
}

function processarMsg_atacar_comDados(msgParams) {
    var dadosAtaque = msgParams.dadosAtaque;
    var dadosDefesa = msgParams.dadosDefesa;

    var territorioDaDefesa = msgParams.territorioDaDefesa;
    var territoriosDoAtaque = msgParams.territoriosDoAtaque;
    var codigoTerritorios = [territorioDaDefesa.codigo];
    for (i = 0; i < territoriosDoAtaque.length; i++) {
        codigoTerritorios.push(territoriosDoAtaque[i].codigo);
    }
    if (_posicaoJogador != _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios(codigoTerritorios);
    }

    this.tocarSom(this, "jogarDados.mp3");
    
    // Iniciar animacao de jogar os dados...
    jogarDados(dadosAtaque.length, dadosDefesa.length, msgParams);
}

function processarMsg_mover(msgParams) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        appwar_mudarCursor('mover_para_fora');
    }
    
    this.tocarSom(this, 'positivo_' + (Math.floor(Math.random()*4)+1) + '.wav');

    var doTerritorio = msgParams.doTerritorioObj;
    _labelTerritorios[doTerritorio.codigo].alteraQuantiadeDeTropas("" + doTerritorio.quantidadeDeTropas);
    
    var paraOTerritorio = msgParams.paraOTerritorioObj;
    _labelTerritorios[paraOTerritorio.codigo].alteraQuantiadeDeTropas("" + paraOTerritorio.quantidadeDeTropas);
   
    if (_posicaoJogador != _posicaoJogadorDaVez) {
        _territorios.pintarGruposTerritorios();
        _territorios.focaNosTerritorios([doTerritorio.codigo, paraOTerritorio.codigo]);
    }

    _jaPodeMover = true;

    if (doTerritorio.quantidadeDeTropas == 1 && 
        _posicaoJogador == _posicaoJogadorDaVez &&
        _turno.tipoAcao != TipoAcaoTurno.mover_apos_conquistar_territorio) {
        territorioClickFunc(_posicaoJogador, paraOTerritorio.codigo);
    }
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

function processarMsg_entrou_no_jogo(msgParams) {
    var posicaoJogador = Number(msgParams.posicao);
    var usuario = msgParams.usuario;

    if (posicaoJogador > -1) {
        if (_posicaoJogador == -1) {
            $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
            _posicaoJogador = posicaoJogador;
            appwar_alterarTituloDaPagina(usuario);
            
            // Olheiro.
            if (posicaoJogador == 7) {
                alert("Este jogo já está em andamento. Você poderá apenas assistí-lo.");
            }
        } else if(posicaoJogador == 7) {
            alert(usuario + " está olhando esta partida.");
        }
        
        $("#jogador" + (posicaoJogador+1)).html(usuario);
    }
}

function processarMsg_saiu_do_jogo(msgParams) {
    var posicaoJogador = Number(msgParams.posicao) + 1;
    var divJogador = document.getElementById("jogador" + posicaoJogador);
    divJogador.innerHTML = "-";

    // TODO: Exibir algum aviso de que o jogador foi embora....
}

function processarMsg_carrega_jogo(msgParams) {
    processarMsg_lista_sala(msgParams);

    for (i = 0; i < msgParams.territoriosDosJogadores.length; i++) {
        var territorioDosJogadores = msgParams.territoriosDosJogadores[i];
        _territorios.atualizaTerritorios(territorioDosJogadores.territorios, territorioDosJogadores.posicao);
    }
    
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
    }
    
    $('#controles').css('visibility', 'visible');
    $('#quantidade_de_tropas').css('visibility', 'visible');

    _posicaoJogadorDaVez = msgParams.jogadorDaVez;
    appwar_alteraInfoTurnoJogador(msgParams.jogadorDaVez);

    $('#bloqueador_tela').css('visibility', 'hidden');
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
    } else if (msgParams.tipoAcao == TipoAcaoTurno.jogo_terminou) {
        processarMsg_turno_jogo_terminou(msgParams);
    }
}

function processarMsg_turno_distribuir_tropas_globais(msgParams) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        this.tocarSom(this, "buzina.mp3");
        appwar_mudarCursor('colocar_tropa');
    } else {
        appwar_mudarCursor('');
    }

    $('#info_turno_texto').html('Distribuir tropas globais');
    appwar_alteraIconeAcaoTurno(TipoAcaoTurno.distribuir_tropas_globais);
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
}

function processarMsg_turno_distribuir_tropas_grupo_territorio(msgParams) {
    var strGrupoTerritorio = msgParams.grupoTerritorio;
    if (strGrupoTerritorio == "AmericaDoNorte") strGrupoTerritorio = "Am. do Norte";
    else if (strGrupoTerritorio == "AmericaDoSul") strGrupoTerritorio = "Am. do Sul";
    $('#info_turno_texto').html('Distribuir tropas na ' + strGrupoTerritorio);
    appwar_alteraIconeAcaoTurno(TipoAcaoTurno.distribuir_tropas_grupo_territorio);
    appwar_alteraQuantidadeDeTropas(msgParams.quantidadeDeTropas);
    
    _territorios.pintarGruposTerritorios();
    _territorios.manterFocoNoGrupo(msgParams.grupoTerritorio);
}

function processarMsg_turno_trocar_cartas(msgParams) {
    $('#info_turno_texto').html('Trocar cartas');
    appwar_alteraIconeAcaoTurno(TipoAcaoTurno.trocar_cartas);
}

function processarMsg_turno_atacar(msgParams) {
    this.tocarSom(this, 'atacar.wav');

    _territorioConquistado = null;
    $('#info_turno_texto').html('Atacar');
    appwar_alteraIconeAcaoTurno(TipoAcaoTurno.atacar);
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        appwar_mudarCursor('alvo');
        _territorios.escureceTodosOsTerritoriosDoJogador(msgParams.vezDoJogador);
    } else {
        appwar_mudarCursor('');
    }
}

function processarMsg_turno_mover(msgParams) {
    this.tocarSom(this, 'mover.wav');
    
    $('#info_turno_texto').html('Mover');
    appwar_alteraIconeAcaoTurno(TipoAcaoTurno.mover);
    _territorios.pintarGruposTerritorios();
    
    if (_posicaoJogador == msgParams.vezDoJogador) {
        appwar_mudarCursor('mover_para_dentro');
        _territorios.escureceTodosOsTerritoriosExcetoDoJogador(msgParams.vezDoJogador);
    } else {
        appwar_mudarCursor('');
    }
}

function processarMsg_turno_jogo_terminou(msgParams) {
    alert(msgParams.ganhador + ' venceu o jogo!');
}

function processarMsg_erro() {
    _jaPodeAtacar = true;
    _jaPodeMover = true;
}

////////////////////////////////////////////////////////////////////////////////
// Métodos utilizados na biblioteca de WebSocket
////////////////////////////////////////////////////////////////////////////////

function posAberturaSocket(valor) {
    $('#painelRegistrarOuEntrar').css('visibility', 'visible');
}

function posRecebimentoMensagemServidor(valor) {
    console.log('Recebeu msg ' + valor);
    var jsonMensagem = JSON.parse(valor);
    if (jsonMensagem.tipo == TipoMensagem.registrar) {
        processarMsg_registrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.entrar) {
        processarMsg_entrar(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.lista_sala) {
        processarMsg_lista_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.entrou_na_sala) {
        processarMsg_entrou_na_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.saiu_da_sala) {
        processarMsg_saiu_da_sala(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.altera_posicao_na_sala) {
        processarMsg_altera_posicao_na_sala(jsonMensagem.params);
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
    } else if (jsonMensagem.tipo == TipoMensagem.entrou_no_jogo) {
        processarMsg_entrou_no_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.saiu_do_jogo) {
        processarMsg_saiu_do_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carrega_jogo) {
        processarMsg_carrega_jogo(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.carrega_jogo_olheiro) {
        processarMsg_carrega_jogo_olheiro(jsonMensagem.params);
    } else if (jsonMensagem.tipo == TipoMensagem.erro) {
        processarMsg_erro();
    }
}

function posFechamentoSocket(valor) {
    $('#bloqueador_tela').css('visibility', 'visible');
    $('#painelRegistrarOuEntrar').css('visibility', 'hidden');
    $('#botao_recarregar').css('visibility', 'visible');
}

function iniciarPartida() {
    if (_quantidadeDeJogadoreNaSala >= 3) {
        iniciarPartidaMsg = comunicacao_iniciarPartida();
        _libwebsocket.enviarObjJson(iniciarPartidaMsg);
    } else {
        alert('Para iniciar o jogo é preciso pelo menos 3 jogadores na sala.');
    }
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

function appwar_abrePainelObjetivo() {
    $('#painel_objetivo').css('visibility', 'visible');
    $('#po_fundo').css('visibility', 'visible');
}

function appwar_fechaPainelObjetivo() {
    $('#painel_objetivo').css('visibility', 'hidden');
    $('#po_fundo').css('visibility', 'hidden');
}

function appwar_abrePainelCartasTerritorios() {
    $('#painel_cartas_territorios').css('visibility', 'visible');
    $('#pct_fundo').css('visibility', 'visible');
}

function appwar_fechaPainelCartasTerritorios() {
    $('#painel_cartas_territorios').css('visibility', 'hidden');
    $('#pct_fundo').css('visibility', 'hidden');
}

function appwar_alteraQuantidadeDeTropas(valor) {
    $('#quantidade_de_tropas').html(valor);
    $('#ac_info').html('Tropas restantes: ' + valor);
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

function appwar_trocaCartasTerritorios() {
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

function territorioMouseMoveFunc(evento, posicaoJogador, nomeDoTerritorio) {
    if (!isNaN(evento.edge) || !isNaN(evento.vertex)) {
        document.getElementById("mapa").className = '';
    } else if (_posicaoJogadorDaVez == _posicaoJogador) {
        if (_turno.tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
            $('#mapa').attr('class', 'mouse_colocar_tropa');
        } else if (_turno.tipoAcao == TipoAcaoTurno.atacar) {
            if (_territorioAlvoAtaque == null) {
                $('#mapa').attr('class', 'mouse_alvo');
            } else {
                $('#mapa').attr('class', 'mouse_atacar');
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover) {
            if (_territorioAlvoMover == null) {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_dentro');
            } else {
                $('#mapa').attr('class', 'mouse_mover_tropas_para_fora');
            }
        }
    } else {
        document.getElementById("mapa").className = '';
    }
}

function territorioMouseOutFunc(posicaoJogador, nomeDoTerritorio) {
    document.getElementById("mapa").className = '';
}

function territorioClickFunc(posicaoJogador, nomeDoTerritorio) {
    if (_posicaoJogador == _posicaoJogadorDaVez) {
        if (_turno.tipoAcao == TipoAcaoTurno.atacar) {
            if (nomeDoTerritorio == _territorioAlvoAtaque) {
                _territorios.pintarGruposTerritorios();
                _territorios.escureceTodosOsTerritoriosDoJogador(_posicaoJogador);
                _territorioAlvoAtaque = null;
                _territoriosAtacante = [];
                appwar_mudarCursor('alvo');
            }
            else if (_territorios.territorioNaoEhDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez)) {
                _territorios.pintarGruposTerritorios();
                _territorioAlvoAtaque = nomeDoTerritorio;
                _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                _territoriosAtacante = [];
                appwar_mudarCursor('atacar');
                this.tocarSom(this, 'alvo.mp3');
            }
            else if (_territorioAlvoAtaque != null) {
                if (_territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1 &&
                    _territorios.temFronteira(nomeDoTerritorio, _territorioAlvoAtaque)) {
                    var indiceTerritorio = _territoriosAtacante.indexOf(nomeDoTerritorio);
                    if (indiceTerritorio == -1) {
                        this.tocarSom(this, 'simSenhor_' + (Math.floor(Math.random()*4)+1) + '.wav');
                        _territoriosAtacante.push(nomeDoTerritorio);
                        _territorios.aumentaBrilhoTerritorio(nomeDoTerritorio);
                    } else {
                        _territoriosAtacante.splice(indiceTerritorio, 1);
                        _territorios.diminuiBrilhoTerritorio(nomeDoTerritorio);
                    }
                }
            }
        } else if (_turno.tipoAcao == TipoAcaoTurno.mover_apos_conquistar_territorio) {
            if (_territorioConquistado == nomeDoTerritorio) {
                finalizarTurno();
            } else {
                var moverMsg = comunicacao_mover(_posicaoJogador, nomeDoTerritorio, 
                    _territorioConquistado, 1);
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
                    appwar_mudarCursor('mover_para_dentro');
                } else if (_territorioAlvoMover == null) {
                    _territorios.pintarGruposTerritorios();
                    _territorios.escureceTodosOsTerritoriosExcetoDoJogador(_posicaoJogadorDaVez);
                    _territorioAlvoMover = nomeDoTerritorio;
                    _territorios.focaNoTerritorioAlvoEAdjacentesDoJogador(nomeDoTerritorio, _posicaoJogadorDaVez);
                    appwar_mudarCursor('mover_para_fora');
                    this.tocarSom(this, 'vamosLa.wav');
                } else if (_territorioMovimento == null && 
                           _territorios.quantidadeDeTropaDoTerritorio(nomeDoTerritorio) > 1 &&
                           _territorios.temFronteira(nomeDoTerritorio, _territorioAlvoMover)) {
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
                    appwar_mudarCursor('mover_para_fora');
                    this.tocarSom(this, 'vamosLa.wav');
                }
            }
        } else {
            var colocarTropaMsg = comunicacao_colocarTropa(posicaoJogador, nomeDoTerritorio, 1);
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

function appwar_alteraTodosOsIconesParaCinza() {
    $('#ac_1').removeClass('ac_1');
    $('#ac_2').removeClass('ac_2');
    $('#ac_3').removeClass('ac_3');
    $('#ac_4').removeClass('ac_4');
    $('#ac_1').addClass('ac_1_cinza');
    $('#ac_2').addClass('ac_2_cinza');
    $('#ac_3').addClass('ac_3_cinza');
    $('#ac_4').addClass('ac_4_cinza');
}

function appwar_alteraIconeAcaoTurno(acao) {
    appwar_alteraTodosOsIconesParaCinza();
    if (acao == TipoAcaoTurno.distribuir_tropas_globais ||
        acao == TipoAcaoTurno.distribuir_tropas_grupo_territorio ||
        acao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
        $('#ac_1').removeClass('ac_1_cinza');
        $('#ac_1').addClass('ac_1');
    } else if (acao == TipoAcaoTurno.trocar_cartas) {
        $('#ac_2').removeClass('ac_2_cinza');
        $('#ac_2').addClass('ac_2');
    } else if (acao == TipoAcaoTurno.atacar) {
        $('#ac_3').removeClass('ac_3_cinza');
        $('#ac_3').addClass('ac_3');
    } else if (acao == TipoAcaoTurno.mover) {
        $('#ac_4').removeClass('ac_4_cinza');
        $('#ac_4').addClass('ac_4');
    }
}

function iniciarControleDeAudio() {
    var audioSlider  = $('#audioSlider');
    var audioSliderTooltip = $('.audioSliderTooltip');
    var audioPlayer = $('#audioPlayer').get(0);

    audioSliderTooltip.hide();

    audioSlider.slider({
            value: 20,
            min: 0,
            max: 100,
            range: 'min',
            animate: true,
            step: 1,
            start: function(e, ui) {
                audioSliderTooltip.fadeIn('fast');
            },
            slide: function(e, ui) {
                var valor = ui.value;
                var volume = $('.audioPlayerVolume');

                audioSliderTooltip.css('left', valor).text(valor);
                if (valor <= 5) { 
                    volume.css('background-position', '0 0');
                } else if (valor <= 25) {
                    volume.css('background-position', '0 -25px');
                } else if (valor <= 75) {
                    volume.css('background-position', '0 -50px');
                } else {
                    volume.css('background-position', '0 -75px');
                }

                audioPlayer.volume = ui.value / 100.0;
            },
            stop: function(e, ui) {
                audioSliderTooltip.fadeOut('fast');
            }
    });
}

function appwar_mudarCursor(tipo) {
    if (tipo == 'colocar_tropa') {
        $('body').attr('class', 'mouse_colocar_tropa');
    }  else if (tipo == 'alvo') {
        $('body').attr('class', 'mouse_alvo');
    }  else if (tipo == 'atacar') {
        $('body').attr('class', 'mouse_atacar');
    } else if (tipo == 'mover_para_fora') {
        $('body').attr('class', 'mouse_mover_tropas_para_fora');
    } else if (tipo == 'mover_para_dentro') {
        $('body').attr('class', 'mouse_mover_tropas_para_dentro');
    } else {
        $('body').attr('class', '');
    } 
}

function appwar_alterarTituloDaPagina(str) {
    document.title = str + ' | JogoWar';
}

function tocarSom(el, soundfile) {
    var el = $('#audioPlayer').get(0);
    var volume = $('#audioSlider').slider('value') / 100.0;

    //if (el.mp3) {
    //    if(el.mp3.paused) el.mp3.play();
    //    else el.mp3.pause();
    //} else {
        el.mp3 = new Audio("http://war.jogowar.com.br:9092/sons/" + soundfile);
        el.mp3.volume = volume;
        el.mp3.play();
    //}
}

function tocarSomDeFundo(el) {
    if (el.mp3) {
        if(el.mp3.paused) el.mp3.play();
        else el.mp3.pause();
    } else {
        el.mp3 = new Audio("http://war.jogowar.com.br:9092/sons/lux_aeterna.mp3");
        el.mp3.addEventListener('ended', function() {
            this.currentTime = 0;
            this.play();
        }, false);
        el.mp3.volume = 0.1;
        el.mp3.play();
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
    _territorios.inicia(territorioClickFunc, territorioMouseMoveFunc, territorioMouseOutFunc);
    
    //this.tocarSomDeFundo(divMapa);
    
    iniciarControleDeAudio();
}

(function(){
    iniciarApp();
})();
