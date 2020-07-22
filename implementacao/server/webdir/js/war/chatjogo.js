var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatJogo = function (chatAreaJogadores, msgsBotaoIrParaBaixo, chatAreaLogs, logsBotaoIrParaBaixo) {
    var that = this;
    this.rolou_a_barra_msgs = false;
    this.rolou_a_barra_logs = false;
    this.util = new jogos.war.Util();

    chatAreaJogadores.scroll(function () {
        if (chatAreaJogadores.scrollTop() + chatAreaJogadores.innerHeight() >= chatAreaJogadores[0].scrollHeight) {
            that.rolou_a_barra_msgs = false;
            msgsBotaoIrParaBaixo.hide();
        } else {
            that.rolou_a_barra_msgs = true;
            msgsBotaoIrParaBaixo.show();
        }
    });

    chatAreaLogs.scroll(function () {
        if (chatAreaLogs.scrollTop() + chatAreaLogs.innerHeight() >= chatAreaLogs[0].scrollHeight) {
            that.rolou_a_barra_logs = false;
            logsBotaoIrParaBaixo.hide();
        } else {
            that.rolou_a_barra_logs = true;
            logsBotaoIrParaBaixo.show();
        }
    });

    this.handleQuestionAnswerCallback = function (texto) {
        jogo_enviaMsg(texto);
    };

    this.ativar = function () {
        this.ativo = true;
    };

    this.desativar = function () {
        this.ativo = false;
    };

    this.estaAtivo = function () {
        return this.ativo || false;
    };

    this.atualizaJogadoresDaSala = function (jogadores) {
        this.jogadores = jogadores;
    };

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

    this.indiceJogador = function (usuario) {
        for (let i = 0; i < this.jogadores.length; ++i) {
            if (this.jogadores[i].usuario === usuario) {
                return this.jogadores[i].posicao;
            }
        }
        return -1;
    };

    this.escreveNoComponente = function (texto) {
        chatAreaJogadores.append(texto + '</br>');

        if (this.rolou_a_barra_msgs) {
            if (chatAreaJogadores.scrollTop() + chatAreaJogadores.innerHeight() >= chatAreaJogadores[0].scrollHeight) {
                this.rolou_a_barra_msgs = false;
                msgsBotaoIrParaBaixo.hide();
            } else {
                this.rolou_a_barra_msgs = true;
                msgsBotaoIrParaBaixo.show();
            }
        } else {
            this.msgsVaiParaBaixo();
        }
    };

    this.escreveNoLog = function (indice, texto) {
        let cor = 'cor_marrom';
        if (indice === 0) {
            cor = 'cor_vermelha';
        } else if (indice === 1) {
            cor = 'cor_azul';
        } else if (indice === 2) {
            cor = 'cor_verde';
        } else if (indice === 3) {
            cor = 'cor_preto';
        } else if (indice === 4) {
            cor = 'cor_branco';
        } else if (indice === 5) {
            cor = 'cor_amarelo';
        }
        chatAreaLogs.append('<div class="log_mensagem_item"><div class="barra_lateral ' + cor + '"></div><div style="display: flex;flex-direction: column;margin: 4px 8px;width: 100%;"><p>' + texto + '</p></div></div>');

        if (this.rolou_a_barra_logs) {
            if (chatAreaLogs.scrollTop() + chatAreaLogs.innerHeight() >= chatAreaLogs[0].scrollHeight) {
                this.rolou_a_barra_logs = false;
                logsBotaoIrParaBaixo.hide();
            } else {
                this.rolou_a_barra_logs = true;
                logsBotaoIrParaBaixo.show();
            }
        } else {
            this.logsVaiParaBaixo();
        }
    };

    this.msgsVaiParaBaixo = function (fromButton = false) {
        if (fromButton) {
            this.rolou_a_barra_msgs = false;
            msgsBotaoIrParaBaixo.hide();
        }
        chatAreaJogadores.scrollTop(chatAreaJogadores[0].scrollHeight - chatAreaJogadores.height());
    };

    this.logsVaiParaBaixo = function (fromButton = false) {
        if (fromButton) {
            this.rolou_a_barra_logs = false;
            logsBotaoIrParaBaixo.hide();
        }
        chatAreaLogs.scrollTop(chatAreaLogs[0].scrollHeight - chatAreaLogs.height());
    };

    this.limpa = function () {
        chatAreaJogadores.text('');
        this.rolou_a_barra_msgs = false;
        msgsBotaoIrParaBaixo.hide();
        chatAreaLogs.text('');
        this.rolou_a_barra_logs = false;
        logsBotaoIrParaBaixo.hide();
    };

    this.boasVindas = function () {
        this.limpa();
        let texto = '';
        texto += 'Entre na sala de áudio para falar com os outros jogadores:'.fontcolor("#453122");
        texto += '<div style=" width: 100%; display: flex; justify-content: start; text-align: center;">';
        texto += '    <a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>';
        texto += '</div>';
        this.escreveNoComponente(texto);
    };

    this.distrubuirTropasGlobais = function (jogador, quantidade) {
        const texto = jogador + ' está distribuindo ' + quantidade + ' exércitos pelo mundo.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.distrubuirTropasGrupoTerritorio = function (jogador, grupo, quantidade) {
        const texto = jogador + ' está distribuindo ' + quantidade + ' exércitos no continente ' + grupo + '.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
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
        this.escreveNoLog(this.indiceJogador(usuario), texto);
    };

    this.ataque = function (jogadorAtaque, territoriosDoAtaque, dadosAtaque,
                            jogadorDefesa, territorioDaDefesa, dadosDefesa) {
        var territoriosDoAtaqueTexto = territoriosDoAtaque[0].codigo;
        for (i = 1; i < territoriosDoAtaque.length - 1; i++)
            territoriosDoAtaqueTexto += ', ' + territoriosDoAtaque[i].codigo;

        if (territoriosDoAtaque.length > 1)
            territoriosDoAtaqueTexto += ' e ' + territoriosDoAtaque[territoriosDoAtaque.length - 1].codigo;

        let texto = '' +
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

        const divDadosAtaque = this.geraDivDados(dadosAtaque);
        const divDadosDefesa = this.geraDivDados(dadosDefesa);

        texto += '<div class="log_dados"><div class="dice dice_label">A</div>' + divDadosAtaque + '</div>';
        texto += '<div class="log_dados"><div class="dice dice_label">D</div>' + divDadosDefesa + '</div>';
        this.escreveNoLog(this.indiceJogador(jogadorAtaque), texto);
    };

    this.geraDivDados = function(dados) {
        const splitDados = dados;
        let divDados = '';
        for (let i = 0; i < splitDados.length; ++i) {
            console.log(splitDados[i]);
            switch (splitDados[i]) {
                case 1:
                    divDados += '<div class="first-face dice"><span class="dot"></span></div>';
                    break;
                case 2:
                    divDados += '<div class="second-face dice"><span class="dot"></span><span class="dot"></span></div>';
                    break;
                case 3:
                    divDados += '<div class="third-face dice"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
                    break;
                case 4:
                    divDados += '<div class="fourth-face dice"><div class="column"><span class="dot"></span><span class="dot"></span></div><div class="column"><span class="dot"></span><span class="dot"></span></div></div>';
                    break;
                case 5:
                    divDados += '<div class="fifth-face dice"><div class="column"><span class="dot"></span><span class="dot"></span></div><div class="column"><span class="dot"></span></div><div class="column"><span class="dot"></span><span class="dot"></span></div></div>';
                    break;
                case 6:
                    divDados += '<div class="sixth-face dice"><div class="column"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div><div class="column"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>';
                    break;
            }
        }
        return divDados;
    };

    this.moveu = function (jogador, doTerritorio, paraOTerritorio, quantidade) {
        var texto = '';
        texto += jogador + ' moveu ' + quantidade;
        if (quantidade > 1) texto += ' exércitos';
        else texto += ' exército';
        texto += ' do território ' + doTerritorio;
        texto += ' para o território ' + paraOTerritorio
        texto += '.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.conquistouTerritorio = function (jogador, territorio) {
        const texto = jogador + ' conquistou o território ' + territorio + '.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.trocouCartasTerritorio = function (jogador, quantidade) {
        const texto = jogador + ' trocou suas cartas territórios por ' + quantidade + ' exércitos.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.verificandoTroca = function (jogador) {
        const texto = jogador + ' está no turno troca de cartas.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.estaAtacando = function (jogador) {
        const texto = jogador + ' está no turno atacar.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
    };

    this.estaMovendo = function (jogador) {
        const texto = jogador + ' está no turno mover.';
        this.escreveNoLog(this.indiceJogador(jogador), texto);
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
