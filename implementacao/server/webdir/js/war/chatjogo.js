var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatJogo = function (chatAreaJogadores, chatAreaLogs) {
    this.util = new jogos.war.Util();

    this.escreve = function (params, indiceCor) {
        let textoUsuarioDiz;
        if (indiceCor !== -1) {
            textoUsuarioDiz = "<b>" + params.usuario + "</b> diz:";
            if (indiceCor === 0) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#841D0F");
            } else if (indiceCor === 1) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#2621A8"); // #262165
            } else if (indiceCor === 2) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#436C4B");
            } else if (indiceCor === 3) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#282423");
            } else if (indiceCor === 4) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#F8F7E9");
            } else if (indiceCor === 5) {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#DFE136");
            } else {
                textoUsuarioDiz = textoUsuarioDiz.fontcolor("#453122");
            }
            this.escreveNoComponente(textoUsuarioDiz);
        }

        let textoMsg = params.texto;
        if (indiceCor === -1) { // Servidor.
            textoMsg = "<i><b>Servidor:</b>&nbsp;" + textoMsg + "</i>";
            textoMsg = textoMsg.fontcolor("#494949");
        } else {
            textoMsg = this.util.substituiMarcacoes(_listaUsuarios.getMapaLista(), params.usuario, params.texto);
            textoMsg = textoMsg.fontcolor("#453122");
        }
        this.escreveNoComponente(textoMsg);
    };

    this.escreveNoComponente = function (texto) {
        chatAreaJogadores.append(texto + '</br>');
        chatAreaJogadores.scrollTop(
            chatAreaJogadores[0].scrollHeight - chatAreaJogadores.height() + 250 /*Tamanho das imagens dentro do chat*/
        );
    };

    this.escreveNoLog = function (texto) {
        chatAreaLogs.append(texto + '</br>');
    };

    this.limpa = function () {
        chatAreaJogadores.text('');
        chatAreaLogs.text('');
    };

    this.boasVindas = function () {
        let texto = 'Entre na sala de áudio para falar com os outros jogadores:';
        texto = texto.fontcolor("#453122");
        texto += '<div style=" width: 100%; display: flex; justify-content: start; text-align: center;">';
        texto += '    <a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>';
        texto += '</div>';
        chatAreaJogadores.append(texto);
        chatAreaJogadores.scrollTop(
            chatAreaJogadores[0].scrollHeight - chatAreaJogadores.height()
        );
    };

    this.distrubuirTropasGlobais = function(jogador, quantidade) {
        const texto = jogador + ' está distribuindo ' + quantidade + ' exércitos pelo mundo.';
        this.escreveNoLog(texto);
    };

    this.distrubuirTropasGrupoTerritorio = function(jogador, grupo, quantidade) {
        const texto = jogador + ' está distribuindo ' + quantidade + ' exércitos no continente ' + grupo + '.';
        this.escreveNoLog(texto);
    };

    this.colocaTropa = function (usuario, territorio, quantidade) {
        var texto = '' +
            usuario + ' colocou ';
        if (quantidade > 1)
            texto += quantidade + ' exércitos';
        else
            texto += quantidade + ' exército';
        texto += ' no território ' + territorio
        texto += '.';
        this.escreveNoLog(texto);
    };

    this.ataque = function (jogadorAtaque, territoriosDoAtaque,
                            jogadorDefesa, territorioDaDefesa) {
        var territoriosDoAtaqueTexto = territoriosDoAtaque[0].codigo;
        for (i = 1; i < territoriosDoAtaque.length - 1; i++)
            territoriosDoAtaqueTexto += ', ' + territoriosDoAtaque[i].codigo;

        if (territoriosDoAtaque.length > 1)
            territoriosDoAtaqueTexto += ' e ' + territoriosDoAtaque[territoriosDoAtaque.length - 1].codigo;

        var texto = '' +
            jogadorAtaque + ' atacou ' +
            jogadorDefesa +
            ' no território ' +
            territorioDaDefesa.codigo;
        if (territoriosDoAtaque.length > 1) {
            texto += ' dos territórios ' +
                territoriosDoAtaqueTexto;
        } else {
            texto += ' do território ' +
                territoriosDoAtaqueTexto;
        }
        texto += '.';
        this.escreveNoLog(texto);
    };

    this.moveu = function (jogador, doTerritorio, paraOTerritorio, quantidade) {
        var texto = '';
        texto += jogador + ' moveu ' + quantidade;
        if (quantidade > 1) texto += ' exércitos';
        else texto += ' exército';
        texto += ' do território ' + doTerritorio;
        texto += ' para o território ' + paraOTerritorio
        texto += '.';
        this.escreveNoLog(texto);
    };

    this.conquistouTerritorio = function (jogador, territorio) {
        const texto = jogador + ' conquistou o território ' + territorio + '.';
        this.escreveNoLog(texto);
    };

    this.trocouCartasTerritorio = function(jogador, quantidade) {
        const texto = jogador + ' trocou suas cartas territórios por ' + quantidade + ' exércitos.';
        this.escreveNoLog(texto);
    };

    this.verificandoTroca = function(jogador) {
        const texto = jogador + ' está no turno troca de cartas.';
        this.escreveNoLog(texto);
    };

    this.estaAtacando = function(jogador) {
        const texto = jogador + ' está no turno atacar.';
        this.escreveNoLog(texto);
    };

    this.estaMovendo = function(jogador) {
        const texto = jogador + ' está no turno mover.';
        this.escreveNoLog(texto);
    };

    this.entrouNoJogo = function (jogador, olheiro) {
        let texto;
        if (olheiro) {
            texto = jogador + ' está assintindo a partida.';
        } else {
            texto = jogador + ' voltou para o jogo.';
        }
        this.escreve({usuario: 'Servidor', texto: texto}, -1);
    };

    this.saiuDoJogo = function (jogador, olheiro) {
        let texto;
        if (olheiro) {
            texto = jogador + ' não está mais assistindo a partida.';
        } else {
            texto = jogador + ' saiu da sala.';
        }
        this.escreve({usuario: 'Servidor', texto: texto}, -1);
    };
};
