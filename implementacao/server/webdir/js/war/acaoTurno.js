var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ComponenteAcaoTurno = function() {
    var ehOJogadorDaVez = false;
    var jogadorDaVez = '';
    
    var quantidadeDeTropasAtacante = {};
    

    this.preparaDistribuirTopasGlobais = function(ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        $('#acoes_turno .info #titulo').html('Distribuir tropas');
        
        var conteudo = '<div class="img img-tropas"></div>';
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="orientacao">Distribua os exércitos em seus territorios.</div>';
        } else {
            conteudo += '<div id="orientacao">'+this.jogadorDaVez+' está distribuindo suas tropas globais.</div>';
        }
        conteudo += '<div id="extra"></div>';
        
        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);
        
        this.alteraQuantidadeDistribuirTropas(quantidadeDeTropas);
    };
    
    this.alteraQuantidadeDistribuirTropas = function(quantidadeDeTropas) {
        $('#acoes_turno .info #extra').html("+" + quantidadeDeTropas);
    };
    
    this.preparaAtacar = function(ehOJogadorDaVez, jogadorDaVez) {
        this.ehOJogadorDaVez = ehOJogadorDaVez;
        this.jogadorDaVez = jogadorDaVez;
        this.quantidadeDeTropasAtacante = {};
        
        var conteudo = "";
        if (this.ehOJogadorDaVez) {
            conteudo += '<div id="orientacao">Selecione um território para atacar.</div>';
        } else {
            conteudo += '<div id="orientacao">'+this.jogadorDaVez+' está atacando.</div>';
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
    
    this.preparaAtacarEscolheuAlvo = function(nomeDoTerritorio, posicaoJogador, quantidade) {
        if (this.ehOJogadorDaVez) {
            $('#acoes_turno .info #conteudoDinamico #orientacao').html('Selecione os territórios que vão atacar '+nomeDoTerritorio+'.');
        }
        
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
        
        $('#acoes_turno .info #conteudoDinamico #alvo .nome').html(nomeDoTerritorio);
        $('#acoes_turno .info #conteudoDinamico #alvo .quantidade').html(quantidade);
    };
    
    this.preparaAtacarAdicionaAtacante = function(posicaoJogador, 
        nomeDoTerritorio, quantidade) {
        
        this.quantidadeDeTropasAtacante[nomeDoTerritorio] = quantidade;
        
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
        
        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += i + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());
        
        var qtdTotal = 0;
        for (var i in this.quantidadeDeTropasAtacante) qtdTotal += this.quantidadeDeTropasAtacante[i];
        $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html(qtdTotal);
    };
    
    this.preparaAtacarRemoveAtacante = function(posicaoJogador, 
        nomeDoTerritorio) {
        
        delete this.quantidadeDeTropasAtacante[nomeDoTerritorio];
        
        var nomeDosTerritorios = "";
        for (var i in this.quantidadeDeTropasAtacante) nomeDosTerritorios += i + " ";
        nomeDosTerritorios = nomeDosTerritorios.trim();
        if (nomeDosTerritorios.length > 12) {
            nomeDosTerritorios = nomeDosTerritorios.substring(0, 13) + "...";
        }
        $('#acoes_turno .info #conteudoDinamico #atacante .nome').html(nomeDosTerritorios.trim());
        
        var qtdTotal = 0;
        for (var i in this.quantidadeDeTropasAtacante) qtdTotal += this.quantidadeDeTropasAtacante[i];
        if (qtdTotal == 0) {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html('');
            $('#acoes_turno .info #conteudoDinamico #atacante').attr('class', '');
        } else {
            $('#acoes_turno .info #conteudoDinamico #atacante .quantidade').html(qtdTotal);
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
};
