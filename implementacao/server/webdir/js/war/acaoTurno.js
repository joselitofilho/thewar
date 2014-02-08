var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ComponenteAcaoTurno = function() {
    var ehOJogadorDaVez = false;
    var jogadorDaVez = '';
    
    var quantidadeDeTropasAtacante = {};
    

    this.turnoDistribuirTopasGlobais = function(ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        $('#acoes_turno .info #titulo').html('Distribuir tropas');
        
        var conteudo = '<div class="img img-tropas"></div>';
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Distribua os exércitos em seus territorios.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">'+this.jogadorDaVez+' está distribuindo suas tropas globais.</div>';
        }
        conteudo += '<div id="extra"></div>';
        
        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);
        
        this.alteraQuantidadeDistribuirTropas(quantidadeDeTropas);
    };
    
    this.alteraQuantidadeDistribuirTropas = function(quantidadeDeTropas) {
        $('#acoes_turno .info #extra').html("+" + quantidadeDeTropas);
    };
    
    this.turnoAtacar = function(ehOJogadorDaVez, jogadorDaVez) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        this.quantidadeDeTropasAtacante = {};
        
        $('#acoes_turno .info #titulo').html('Atacar');
        
        var conteudo = "";
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="meio" class="meio-geral">Selecione um território para atacar.</div>';
        } else {
            conteudo += '<div id="meio" class="meio-geral">'+this.jogadorDaVez+' está atacando.</div>';
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
    };
    
    this.turnoAtacarEscolheuAlvo = function(nomeDoTerritorio, posicaoJogador, quantidade) {
        if (this.ehOJogadorDaVez) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Selecione os territórios que vão atacar '+nomeDoTerritorio+'.');
        }
        
        this.turnoAtacarAlteraTerritorioAlvo(posicaoJogador);
        
        $('#acoes_turno .info #conteudoDinamico #alvo .nome').html(nomeDoTerritorio);
        $('#acoes_turno .info #conteudoDinamico #alvo .quantidade').html(quantidade);
    };
    
    this.turnoAtacarAlteraTerritorioAlvo = function(posicaoJogador) {
        $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', '');
        switch(posicaoJogador) {
            case 0:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-vermelho');
                break;
            case 1:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-azul');
                break;
            case 2:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-verde');
                break;
            case 3:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-preto');
                break;
            case 4:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-branco');
                break;
            case 5:
                $('#acoes_turno .info #conteudoDinamico #alvo').attr('class', 'terr-amarelo');
                break;
        }
    };
    
    this.turnoAtacarAdicionaAtacante = function(posicaoJogador, 
        nomeDoTerritorio, quantidade) {
        
        this.quantidadeDeTropasAtacante[nomeDoTerritorio] = quantidade;
        
        this.turnoAtacarAlteraTerritorioAtacante(posicaoJogador);
        
        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += i + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());
        
        this.atualizaQuantidadeDeTropasAtacante();
    };
    
    this.turnoAtacarAlteraTerritorioAtacante = function(posicaoJogador) {
        $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', '');
        switch(posicaoJogador) {
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
    
    this.turnoAtacarRemoveAtacante = function(posicaoJogador, 
        nomeDoTerritorio) {
        
        delete this.quantidadeDeTropasAtacante[nomeDoTerritorio];

        this.atualizaNomeDosTerritoriosAtacante();
        this.atualizaQuantidadeDeTropasAtacante();
    };
    
    this.turnoAtacarExibeTerritoriosEnvolvidosNoAtaque = function(
        territoriosDoAtaque, territorioDaDefesa, jogadorAtaque, jogadorDefesa) {
        this.turnoAtacarAlteraTerritorioAlvo(jogadorDefesa.posicao);
        this.turnoAtacarAlteraTerritorioAtacante(jogadorAtaque.posicao);
        
        // Atualizando quantidade de territórios.
        this.quantidadeDeTropasAtacante = {}
        for (i = 0; i < territoriosDoAtaque.length; i++) {
            this.quantidadeDeTropasAtacante[territoriosDoAtaque[i].codigo] = territoriosDoAtaque[i].quantidadeDeTropas;
        }
        this.atualizaNomeDosTerritoriosAtacante();
        this.atualizaQuantidadeDeTropasAtacante();
        
        $('#acoes_turno .info #conteudoDinamico #alvo .nome').html(territorioDaDefesa.codigo);
        $('#acoes_turno .info #conteudoDinamico #alvo .quantidade').html(territorioDaDefesa.quantidadeDeTropas);
    }; 
    
    this.turnoAtacarExibeResultadoDosDados = function(dadosAtaque, dadosDefesa) {
        this.turnoAtacarExibirDados();
        
        // Usabilidade: Dados do ataque.
        var qtdDadosAtaqueVenceu = 0;
        for (i = 0; i < dadosAtaque.length; i++) {
            if (i < dadosDefesa.length) {
                if (dadosAtaque[i] <= dadosDefesa[i])
                    $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
                else {
                    ++qtdDadosAtaqueVenceu;
                    $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px 0px');
                }
            } else
                $('#da' + (i+1)).css('background-position', ((dadosAtaque[i]-1)*-40) + 'px -80px');
        }
        
        // Usabilidade: Dados da defesa.
        for (i = 0; i < dadosDefesa.length; i++) {
            if (i < dadosAtaque.length) {
                if (dadosDefesa[i] < dadosAtaque[i])
                    $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
                else {
                    $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -40px');
                }
            } else
                $('#dd' + (i+1)).css('background-position', ((dadosDefesa[i]-1)*-40) + 'px -120px');
        }
        
        // Usabilidade: Resultado dos dados.
        if (qtdDadosAtaqueVenceu >= 1) tocarSom(this, 'ganhouNosDados.mp3');
        else tocarSom(this, 'perdeuNosDados.mp3');
    };
    
    this.turnoAtacarExibirDados = function() {
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
    
    this.turnoAtacarConquistouTerritorio = function(usuario, seFoiVoceQueConquistou, territorioConquistado) {
        $('#acoes_turno .info #conteudoDinamico #meio').attr('class', 'meio-geral');
        if (foiVoceQueConquistou) {
            $('#acoes_turno .info #conteudoDinamico #meio').html('Você conquistou o território ' + territorioConquistado + '.');
        } else {
            $('#acoes_turno .info #conteudoDinamico #meio').html(usuario + ' conquistou o território ' + territorioConquistado + '.');
        }
    };
    
    this.alteraBotoesDaAcao = function(ehOJogadorDaVez, tipoAcao) {
        $('#btnAcao1').attr('class', '');
        $('#btnAcao2').attr('class', '');

        if (ehOJogadorDaVez) {
            if (tipoAcao == TipoAcaoTurno.distribuir_tropas_globais) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao == TipoAcaoTurno.distribuir_tropas_grupo_territorio) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao == TipoAcaoTurno.trocar_cartas) {
                $('#btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-ver-cartas');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            } else if (tipoAcao == TipoAcaoTurno.distribuir_tropas_troca_de_cartas) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', '');
            } else if (tipoAcao == TipoAcaoTurno.atacar) {
                $('#btnAcao1').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-atacar');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            } else if (tipoAcao == TipoAcaoTurno.mover) {
                $('#btnAcao1').attr('class', '');
                $('#btnAcao2').attr('class', 'sprite-btn-acoes sprite-btn-acoes-turno-prosseguir');
            }
        }
        
        $('#acoes_turno .sprite-btn-acoes-turno-atacar').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-atacar').click(function(){
            if (ehOJogadorDaVez) atacar();
        });

        $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-ver-cartas').click(function(){
            if (ehOJogadorDaVez) appwar_abrePainelCartasTerritorios();
        });

        $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').unbind('click');
        $('#acoes_turno .sprite-btn-acoes-turno-prosseguir').click(function(){
            if (ehOJogadorDaVez) finalizarTurno();
        });
    };
    
    this.atualizaQuantidadeDeTropasAtacante = function() {
        var qtdTotal = 0;
        for (var i in this.quantidadeDeTropasAtacante) qtdTotal += this.quantidadeDeTropasAtacante[i];
        if (qtdTotal == 0) {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html('');
            $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', '');
        } else {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html(qtdTotal);
        }
    };
    
    this.atualizaNomeDosTerritoriosAtacante = function() {
        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += i + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());
    };
};
