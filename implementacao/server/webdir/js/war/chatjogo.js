var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatJogo = function (area) {
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

        let textoMsg = this.util.substituiMarcacoes(_listaUsuarios.getMapaLista(), params.usuario, params.texto);
        if (indiceCor === -1) { // Servidor.
            textoMsg = "<i><b>Servidor:</b>&nbsp;" + textoMsg + "</i>";
            textoMsg = textoMsg.fontcolor("#494949");
        } else {
            textoMsg = textoMsg.fontcolor("#453122");
        }
        this.escreveNoComponente(textoMsg);
    };

    this.escreveNoComponente = function (texto) {
        area.append(texto + '</br>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.escreveNoLog = function (texto) {
        console.log('[SALA]', texto);
    };

    this.limpa = function () {
        area.text('');
    };

    this.colocaTropa = function (usuario, territorio, quantidade) {
        var texto = '<i>Servidor: ' +
            usuario + ' colocou ';
        if (quantidade > 1)
            texto += quantidade + ' exércitos';
        else
            texto += quantidade + ' exército';
        texto += ' no território ' + territorio + '.</i>';
        this.escreveNoLog(texto);
    };

    this.ataque = function (jogadorAtaque, territoriosDoAtaque,
                            jogadorDefesa, territorioDaDefesa) {
        var territoriosDoAtaqueTexto = territoriosDoAtaque[0].codigo;
        for (i = 1; i < territoriosDoAtaque.length - 1; i++)
            territoriosDoAtaqueTexto += ', ' + territoriosDoAtaque[i].codigo;

        if (territoriosDoAtaque.length > 1)
            territoriosDoAtaqueTexto += ' e ' + territoriosDoAtaque[territoriosDoAtaque.length - 1].codigo;

        var texto = 'Servidor: ' +
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
        var texto = 'Servidor: ';
        texto += jogador + ' moveu ' + quantidade;
        if (quantidade > 1) texto += ' exércitos';
        else texto += ' exército';
        texto += ' do território ' + doTerritorio;
        texto += ' para o território ' + paraOTerritorio + '.';
        this.escreveNoLog(texto);
    };

    this.conquistouTerritorio = function (jogador, territorio) {
        var texto = 'Servidor: ';
        texto += jogador + ' conquistou o território ' + territorio + '.';
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
