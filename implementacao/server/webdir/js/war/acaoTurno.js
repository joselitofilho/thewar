var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ComponenteAcaoTurno = function() {
    this.preparaDistribuirTopasGlobais = function(ehOJogadorDaVez, jogadorDaVez, quantidadeDeTropas) {
        $('#acoes_turno .info #titulo').html('Distribuir tropas');
        
        var conteudo = "<div class=\"img img-tropas\"></div>";
        if (ehOJogadorDaVez) {
            conteudo += "<div id=\"orientacao\">Distribua os exércitos em seus territorios.</div>";
        } else {
            conteudo += "<div id=\"orientacao\">"+jogadorDaVez+" está distribuindo suas tropas globais.</div>";
        }
        conteudo += "<div id=\"extra\"></div>";
        
        $('#acoes_turno .info #conteudoDinamico').html('');
        $('#acoes_turno .info #conteudoDinamico').html(conteudo);
        
        this.distribuirTropasAlteraQuantidade(quantidadeDeTropas);
    };
    
    this.preparaAtacar = function(ehOJogadorDaVez, jogadorDaVez) {
        
    };
    
    this.distribuirTropasAlteraQuantidade = function(quantidadeDeTropas) {
        $('#acoes_turno .info #extra').html("+" + quantidadeDeTropas);
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
