var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ComponenteAcaoTurno = function () {
    this.ehOJogadorDaVez = false;
    this.jogadorDaVez = '';
    this.quantidadeDeTropasAtacante = {};
    this.obrigatorio = false;

    this.alteraTimelineJogadorDaVez = function (tipoAcao, jogadorDaVez) {
        $('#acoes_turno .timeline #turno1').attr('class', 'turno turno-padrao');
        $('#acoes_turno .timeline #turno2').attr('class', 'turno turno-padrao');
        $('#acoes_turno .timeline #turno3').attr('class', 'turno turno-padrao');
        $('#acoes_turno .timeline #turno4').attr('class', 'turno turno-padrao');
        if (tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
            $('#acoes_turno .timeline #turno1').attr('class', 'turno turno-j' + jogadorDaVez);
        } else if (tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
            $('#acoes_turno .timeline #turno1').attr('class', 'turno turno-j' + jogadorDaVez);
        } else if (tipoAcao == TipoAcaoTurno.trocar_cartas) {
            $('#acoes_turno .timeline #turno2').attr('class', 'turno turno-j' + jogadorDaVez);
        } else if (tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
            $('#acoes_turno .timeline #turno2').attr('class', 'turno turno-j' + jogadorDaVez);
        } else if (tipoAcao == TipoAcaoTurno.atacar) {
            $('#acoes_turno .timeline #turno3').attr('class', 'turno turno-j' + jogadorDaVez);
        } else if (tipoAcao == TipoAcaoTurno.mover) {
            $('#acoes_turno .timeline #turno4').attr('class', 'turno turno-j' + jogadorDaVez);
        }
    };

    this.turnoDistribuirTopasGlobais = function (ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        $('#acoes_turno .info #titulo').html('Distribuir tropas');

        var conteudo = '<div class="img-tropas"></div>';
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Distribua os exércitos em seus territorios.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está distribuindo suas tropas globais.</div>';
        }
        conteudo += '<div id="extra"></div>';

        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);

        this.alteraQuantidadeDistribuirTropas(quantidadeDeTropas);
    };

    this.turnoDistribuirTopasContinente = function (ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas, grupo) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        $('#acoes_turno .info #titulo').html('Distribuir tropas');

        var conteudo = '<div class="img img-tropas"></div>';
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Distribua os exércitos em seus territorios na ' + grupo + '.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está distribuindo suas tropas na ' + grupo + '.</div>';
        }
        conteudo += '<div id="extra"></div>';

        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);

        this.alteraQuantidadeDistribuirTropas(quantidadeDeTropas);
    };

    this.turnoDistribuirTopasPorTroca = function (ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        $('#acoes_turno .info #titulo').html('Distribuir tropas');

        var conteudo = '<div class="img img-tropas"></div>';
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Distribua os exércitos em seus territorios.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está distribuindo suas tropas pela troca.</div>';
        }
        conteudo += '<div id="extra"></div>';

        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);

        this.alteraQuantidadeDistribuirTropas(quantidadeDeTropas);
    };

    this.alteraQuantidadeDistribuirTropas = function (quantidadeDeTropas) {
        $('#acoes_turno .info #extra').html("+" + quantidadeDeTropas);
    };

    this.turnoTrocarCartas = function (ehOJogadorDaVez, jogadorDaVez, obrigatorio) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        this.obrigatorio = obrigatorio;
        if (this.obrigatorio) {
            $('#acoes_turno .info #titulo').html('Troca obrigatória');
        } else {
            $('#acoes_turno .info #titulo').html('Trocar?');
        }

        var conteudo = '<div class="img-trocar"></div>';
        if (this.ehOJogadorDaVez) {
            if (this.obrigatorio) {
                conteudo += '<div id="meio" class="meio-geral">Você está com 5 cartas. É obrigatório fazer uma troca.</div>';
            } else {
                conteudo += '<div id="meio" class="meio-geral">Faça troca de suas cartas por exércitos, se desejar.</div>';
            }
        } else {
            if (this.obrigatorio) {
                conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está fazendo uma troca.</div>';
            } else {
                conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está verificando se vai fazer uma troca.</div>';
            }
        }

        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);
    };

    this.turnoAtacar = function (ehOJogadorDaVez, jogadorDaVez) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        this.quantidadeDeTropasAtacante = {};

        $('#acoes_turno .info #titulo').html('Atacar');

        var conteudo = "";
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Selecione o território alvo.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está atacando.</div>';
        }
        conteudo +=
            '<div id="alvo">' +
            '<div class="nome"></div>' +
            '<div class="quantidade"></div>' +
            '</div>' +
            '<div id="atacante">' +
            '<div class="nome"></div>' +
            '<div class="quantidade"></div>' +
            '</div>';
        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);

        this.escondeBtn1Atacar();
    };

    this.turnoAtacarEscolheuAlvo = function (codigoDoTerritorio, posicaoJogador, quantidade) {
        if (this.ehOJogadorDaVez) {
            var nomeDoTerritorio = _nomeDosTerritoriosPeloCodigo[codigoDoTerritorio];
            this.turnoAtacarLimparAtacante();
            $('#acoes_turno .info #conteudoDinamico #meio').attr('class', 'meio-geral');
            $('#acoes_turno .info #conteudoDinamico #meio').html('Selecione os territórios que vão atacar ' + nomeDoTerritorio + '.');
        }

        this.turnoAlteraTerritorioAlvo(posicaoJogador, '#alvo');

        $('#acoes_turno .info #conteudoDinamico #alvo .nome').html(nomeDoTerritorio);
        $('#acoes_turno .info #conteudoDinamico #alvo .quantidade').html(quantidade);
        this.escondeBtn1Atacar();
    };

    this.turnoAtacarAdicionaAtacante = function (posicaoJogador,
                                                 codigoDoTerritorio, quantidade) {
        var nomeDoTerritorio = _nomeDosTerritoriosPeloCodigo[codigoDoTerritorio];
        this.quantidadeDeTropasAtacante[codigoDoTerritorio] = quantidade;

        this.turnoAtacarAlteraTerritorioAtacante(posicaoJogador);

        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += _nomeDosTerritoriosPeloCodigo[i] + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());

        this.atualizaQuantidadeDeTropasAtacante();
        this.exibeBtn1Atacar();
    };

    this.turnoAtacarAlteraTerritorioAtacante = function (posicaoJogador) {
        $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', '');
        switch (posicaoJogador) {
            case 0:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-vermelho');
                break;
            case 1:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-azul');
                break;
            case 2:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-verde');
                break;
            case 3:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-preto');
                break;
            case 4:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-branco');
                break;
            case 5:
                $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', 'terr-amarelo');
                break;
        }
    };

    this.turnoAtacarLimparAtacante = function () {
        this.quantidadeDeTropasAtacante = {};

        this.atualizaNomeDosTerritoriosAtacante();
        this.atualizaQuantidadeDeTropasAtacante();
    };

    this.turnoAtacarRemoveAtacante = function (posicaoJogador, codigoDoTerritorio) {

        delete this.quantidadeDeTropasAtacante[codigoDoTerritorio];

        this.atualizaNomeDosTerritoriosAtacante();
        this.atualizaQuantidadeDeTropasAtacante();

        if (Object.keys(this.quantidadeDeTropasAtacante).length == 0) {
            this.escondeBtn1Atacar();
        }
    };

    this.turnoAtacarExibeTerritoriosEnvolvidosNoAtaque = function (
        territoriosDoAtaque, territorioDaDefesa, jogadorAtaque, jogadorDefesa) {
        this.turnoAlteraTerritorioAlvo(jogadorDefesa.posicao, '#alvo');
        this.turnoAtacarAlteraTerritorioAtacante(jogadorAtaque.posicao);

        // Atualizando quantidade de territórios.
        this.quantidadeDeTropasAtacante = {};
        for (i = 0; i < territoriosDoAtaque.length; i++) {
            this.quantidadeDeTropasAtacante[territoriosDoAtaque[i].codigo] = territoriosDoAtaque[i].quantidadeDeTropas;
        }
        this.atualizaNomeDosTerritoriosAtacante();
        this.atualizaQuantidadeDeTropasAtacante();

        $('#acoes_turno .info #conteudoDinamico #alvo .nome').html(_nomeDosTerritoriosPeloCodigo[territorioDaDefesa.codigo]);
        $('#acoes_turno .info #conteudoDinamico #alvo .quantidade').html(territorioDaDefesa.quantidadeDeTropas);
    };

    this.turnoAtacarExibeResultadoDosDados = function (dadosAtaque, dadosDefesa) {
        this.turnoAtacarExibirDados();

        // Usabilidade: Dados do ataque.
        var qtdDadosAtaqueVenceu = 0;
        for (i = 0; i < dadosAtaque.length; i++) {
            if (i < dadosDefesa.length) {
                if (dadosAtaque[i] <= dadosDefesa[i])
                    $('#da' + (i + 1)).css('background-position', ((dadosAtaque[i] - 1) * -40) + 'px -78px');
                else {
                    ++qtdDadosAtaqueVenceu;
                    $('#da' + (i + 1)).css('background-position', ((dadosAtaque[i] - 1) * -40) + 'px 0px');
                }
            } else
                $('#da' + (i + 1)).css('background-position', ((dadosAtaque[i] - 1) * -40) + 'px -78px');
        }

        // Usabilidade: Dados da defesa.
        for (i = 0; i < dadosDefesa.length; i++) {
            if (i < dadosAtaque.length) {
                if (dadosDefesa[i] < dadosAtaque[i])
                    $('#dd' + (i + 1)).css('background-position', ((dadosDefesa[i] - 1) * -40) + 'px -118px');
                else {
                    $('#dd' + (i + 1)).css('background-position', ((dadosDefesa[i] - 1) * -40) + 'px -39px');
                }
            } else
                $('#dd' + (i + 1)).css('background-position', ((dadosDefesa[i] - 1) * -40) + 'px -118px');
        }

        // Usabilidade: Resultado dos dados.
        if (qtdDadosAtaqueVenceu >= 1) tocarSom(this, 'ganhouNosDados.mp3');
        else tocarSom(this, 'perdeuNosDados.mp3');
    };

    this.turnoAtacarExibirDados = function () {
        if ($('#acoes_turno .info #conteudoDinamico #meio').attr('class') == 'meio-geral') {
            $('#acoes_turno .info #conteudoDinamico #meio').attr('class', 'meio-dados');

            var divDados =
                '<div id="dados">' +
                '<div id="dadosAtaque">' +
                '<div id="da1" class="dado dado_ataque"></div>' +
                '<div id="da2" class="dado dado_ataque"></div>' +
                '<div id="da3" class="dado dado_ataque"></div>' +
                '</div>' +
                '<div id="dadosDefesa">' +
                '<div id="dd1" class="dado dado_defesa"></div>' +
                '<div id="dd2" class="dado dado_defesa"></div>' +
                '<div id="dd3" class="dado dado_defesa"></div>' +
                '</div>' +
                '</div>';
            $('#acoes_turno .info #conteudoDinamico #meio').html(divDados);
        }
    };

    this.turnoAtacarConquistouTerritorio = function (usuario, foiVoceQueConquistou, codigoTerritorioConquistado) {
        $('#acoes_turno .info #conteudoDinamico #meio').attr('class', 'meio-geral');
        $('#acoes_turno .info #conteudoDinamico #meio').empty();
        if (foiVoceQueConquistou) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Você conquistou o território ' + _nomeDosTerritoriosPeloCodigo[codigoTerritorioConquistado] + '.');
        } else {
            $('#acoes_turno .info #conteudoDinamico #meio').html(usuario + ' conquistou o território ' + _nomeDosTerritoriosPeloCodigo[codigoTerritorioConquistado] + '.');
        }
    };

    this.turnoMover = function (ehOJogadorDaVez, jogadorDaVez) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        this.quantidadeDeTropasAtacante = {};

        $('#acoes_turno .info #titulo').html('Mover');

        var conteudo = "";
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Selecione um território de onde sairão os exércitos.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">' + this.jogadorDaVez + ' está movendo os exércitos.</div>';
        }
        conteudo +=
            '<div id="entrada">' +
            '<div class="nome"></div>' +
            '</div>' +
            '<div id="saida">' +
            '<div class="nome"></div>' +
            '</div>';
        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);
    };

    this.turnoMoverEscolheuSaida = function (codigoDoTerritorio, posicaoJogador) {
        if (this.ehOJogadorDaVez) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Selecione um território para onde os exércitos irão.');
        }
        this.turnoAlteraTerritorioAlvo(posicaoJogador, '#saida');
        $('#acoes_turno .info #conteudoDinamico #saida .nome').html(_nomeDosTerritoriosPeloCodigo[codigoDoTerritorio]);
    };

    this.turnoMoverEscolheuEntrada = function (codigoDoTerritorio, posicaoJogador) {
        if (this.ehOJogadorDaVez) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Agora escolha a quantidade de exércitos à movimentar.');
        }
        this.turnoAlteraTerritorioAlvo(posicaoJogador, '#entrada');
        $('#acoes_turno .info #conteudoDinamico #entrada .nome').html(_nomeDosTerritoriosPeloCodigo[codigoDoTerritorio]);
    };

    this.turnoMoverLimpar = function () {
        if (this.ehOJogadorDaVez) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Selecione um território de onde sairão os exércitos.');
        } else {
            $('#acoes_turno .info #conteudoDinamico #meio').html(this.jogadorDaVez + ' está movendo os exércitos.');
        }
        $('#acoes_turno .info #conteudoDinamico #saida .nome').html('');
        $('#acoes_turno .info #conteudoDinamico #saida').attr('class', '');
        $('#acoes_turno .info #conteudoDinamico #entrada .nome').html('');
        $('#acoes_turno .info #conteudoDinamico #entrada').attr('class', '');
    };

    this.turnoAlteraTerritorioAlvo = function (posicaoJogador, elemento) {
        $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', '');
        switch (posicaoJogador) {
            case 0:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-vermelho');
                break;
            case 1:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-azul');
                break;
            case 2:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-verde');
                break;
            case 3:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-preto');
                break;
            case 4:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-branco');
                break;
            case 5:
                $('#acoes_turno .info #conteudoDinamico ' + elemento).attr('class', 'terr-amarelo');
                break;
        }
    };

    this.btnVerCartasClick = function (ehOJogadorDaVez) {
        if (ehOJogadorDaVez) {
            $('#acoes_turno').css('z-index', '9001');
            $('#acoes_turno .info #conteudoDinamico #meio').html('Escolha 3 cartas de forma iguais ou 3 cartas de formas diferentes.');
            this.alteraFuncaoBtnVerCartasParaTrocar(ehOJogadorDaVez);
            this.alteraFuncaoBtnProsseguirParaCancelar(ehOJogadorDaVez);
            $('#painel_cartas_territorios').css('visibility', 'visible');
            $('#pct_fundo').css('visibility', 'visible');
        }
    };

    this.alteraBotoesDaAcao = function (ehOJogadorDaVez, tipoAcao) {
        $('#btnAcao1').attr('class', '');
        $('#btnAcao2').attr('class', '');

        if (ehOJogadorDaVez) {
            if (tipoAcao === TipoAcaoTurno.distribuir_tropas_globais ||
                tipoAcao === TipoAcaoTurno.distribuir_tropas_grupo_territorio ||
                tipoAcao === TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
                this.exibeQuantidadeTropas();
            } else {
                this.escondeQuantidadeTropas();
            }
        } else {
            this.escondeQuantidadeTropas();
        }

        if (ehOJogadorDaVez) {
            if (tipoAcao === TipoAcaoTurno.distribuir_tropas_globais) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao === TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao === TipoAcaoTurno.trocar_cartas) {
                $('#btnAcao1').css('visibility', 'visible');
                $('#btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-ver-cartas');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            } else if (tipoAcao === TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao === TipoAcaoTurno.atacar) {
                //$('#btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-atacar');
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            } else if (tipoAcao === TipoAcaoTurno.mover) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            }
        }

        $('#acoes_turno .sprite-btn-acoes-turno-atacar').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-atacar').click(function () {
            if (ehOJogadorDaVez) atacar();
        });

        var me = this;
        $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').click(function () {
            me.btnVerCartasClick(ehOJogadorDaVez);
        });

        $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').click(function () {
            if (ehOJogadorDaVez) {
                if (tipoAcao === TipoAcaoTurno.atacar) {
                    Swal.fire({
                        title: 'Gostaria de encerrar o ataque?',
                        text: "",
                        icon: 'question',
                        showCancelButton: true,
                        confirmButtonColor: '#453122',
                        cancelButtonColor: '#888',
                        confirmButtonText: 'Sim',
                        cancelButtonText: 'Cancelar',
                        timerProgressBar: true,
                        timer: 5000,
                    }).then((result) => {
                        if (result.value) {
                            finalizarTurno();
                        }
                    });
                } else {
                    finalizarTurno();
                }
            }
        });
    };

    this.atualizaQuantidadeDeTropasAtacante = function () {
        var qtdTotal = 0;
        for (var i in this.quantidadeDeTropasAtacante) qtdTotal += this.quantidadeDeTropasAtacante[i];
        if (qtdTotal == 0) {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html('');
            $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', '');
        } else {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html(qtdTotal);
        }
    };

    this.atualizaNomeDosTerritoriosAtacante = function () {
        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += _nomeDosTerritoriosPeloCodigo[i] + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());
    };

    this.alteraFuncaoBtnVerCartasParaTrocar = function (ehOJogadorDaVez) {
        if (ehOJogadorDaVez) {
            $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').unbind('click');
            $('#acoes_turno #btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-trocar');
            $('#acoes_turno .sprite-btn-acoes-turno-trocar').unbind('click');
            var me = this;
            $('#acoes_turno .sprite-btn-acoes-turno-trocar').click(function () {
                if (ehOJogadorDaVez) {
                    appwar_trocaCartasTerritorios();
                }
            });
        }
    };

    this.alteraFuncaoBtnTrocarParaVerCartas = function (ehOJogadorDaVez) {
        if (ehOJogadorDaVez) {
            $('#acoes_turno .sprite-btn-acoes-turno-trocar').unbind('click');
            $('#acoes_turno #btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-ver-cartas');
            $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').unbind('click');
            var me = this;
            $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').click(function () {
                me.btnVerCartasClick(ehOJogadorDaVez);
            });
        }
    };

    this.alteraFuncaoBtnProsseguirParaCancelar = function (ehOJogadorDaVez) {
        if (ehOJogadorDaVez) {
            $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').unbind('click');
            $('#acoes_turno #btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-cancelar');
            $('#acoes_turno .sprite-btn-acoes-turno-cancelar').unbind('click');
            var me = this;
            $('#acoes_turno .sprite-btn-acoes-turno-cancelar').click(function () {
                if (ehOJogadorDaVez) {
                    var texto = "";
                    if (me.obrigatorio) {
                        texto = 'Você está com 5 cartas. É obrigatório fazer uma troca.';
                    } else {
                        texto = 'Faça troca de suas cartas por exércitos, se desejar.';
                    }
                    $('#acoes_turno .info #conteudoDinamico #meio').html(texto);
                    me.alteraFuncaoBtnCancelarParaProsseguir(ehOJogadorDaVez);
                    me.alteraFuncaoBtnTrocarParaVerCartas(ehOJogadorDaVez);
                    appwar_fechaPainelCartasTerritorios();
                }
            });
        }
    };

    this.alteraFuncaoBtnCancelarParaProsseguir = function (ehOJogadorDaVez) {
        if (ehOJogadorDaVez) {
            $('#acoes_turno').css('z-index', '999');
            $('#acoes_turno .sprite-btn-acoes-turno-cancelar').unbind('click');
            $('#acoes_turno #btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').unbind('click');
            $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').click(function () {
                if (ehOJogadorDaVez) {
                    finalizarTurno();
                }
            });
        }
    };

    this.escondeBtn1Atacar = function () {
        //$('.sprite-btn-acoes-turno-atacar').css('visibility', 'hidden');
        $('#popupBtnAtacar').css('visibility', 'hidden');
    };

    this.exibeBtn1Atacar = function () {
        //$('.sprite-btn-acoes-turno-atacar').css('visibility', 'visible');
        $('#popupBtnAtacar').css('visibility', 'visible');
    };

    this.escondeQuantidadeTropas = function () {
        $('#quantidade_tropas').css('visibility', 'hidden');
        $("#quantidade_tropas").find(".rb-tab-active").removeClass("rb-tab-active");
        $("#quantidade_tropa1").addClass("rb-tab-active");
    };

    this.exibeQuantidadeTropas = function () {
        $('#quantidade_tropas').css('visibility', 'visible');
        $("#quantidade_tropas").find(".rb-tab-active").removeClass("rb-tab-active");
        $("#quantidade_tropa1").addClass("rb-tab-active");
    };
};
