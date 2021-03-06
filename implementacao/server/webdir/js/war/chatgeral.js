var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ChatGeral = function (area, botaoIrParaBaixo) {
    var that = this;
    this.rolou_a_barra = false;
    this.util = new jogos.war.Util();

    area.scroll(function () {
        if (area.scrollTop() + area.innerHeight() >= area[0].scrollHeight) {
            that.rolou_a_barra = false;
            botaoIrParaBaixo.hide();
        } else {
            that.rolou_a_barra = true;
            botaoIrParaBaixo.show();
        }
    });

    this.handleQuestionAnswerCallback = function (texto) {
        sala_enviaMsg(texto);
    };

    this.escreve = function (params, indiceCor) {
        const mensagemServidor = (indiceCor === -1);

        let texto = this.util.substituiMarcacoes(_listaUsuarios.getMapaLista(), params.usuario, params.texto);
        if (mensagemServidor) {
            texto = "<i><b>Servidor:</b>&nbsp;" + texto + "</i><br/>";
            texto = texto.fontcolor("#494949");
        } else {
            texto =
                "<div style='color: var(--color-dark-brown);'>" +
                "<a style='color: var(--color-dark-brown);' href='javascript:perfil_jogador_onclick(\"" + params.usuario + "\", \"human\");'><b>" + params.usuario + "</b></a> diz:" +
                "<br/>" + texto + "</div>";
        }

        area.append(texto);

        if (this.rolou_a_barra) {
            if (area.scrollTop() + area.innerHeight() >= area[0].scrollHeight) {
                that.rolou_a_barra = false;
                botaoIrParaBaixo.hide();
            } else {
                that.rolou_a_barra = true;
                botaoIrParaBaixo.show();
            }
        } else {
            this.vaiParaBaixo();
        }
    };

    this.servidorDiz = function (msg) {
        this.escreve({usuario: 'Servidor', texto: msg}, -1);
    };

    this.limpa = function () {
        area.html('');
        this.rolou_a_barra = false;
        botaoIrParaBaixo.hide();
    };

    this.boasVindas = function () {
        this.limpa();

        let texto = '';
        texto += '<h5>Seja bem-vindo ao servidor principal!</h5>';
        texto += '<div class="chat_tour" onclick="_tour.open()">';
        texto += '    <div class="chat_soldado"></div>';
        texto += '    <p>Primeira vez por aqui?<br/>Clique aqui para conhecer o jogo.</p>';
        texto += '</div>';
        // texto += '<img src="../../imagens/lobby/banners/evento_chat.png" style="width: 100%; border-radius: 5px;" />';
        texto += 'Connect-se a uma de nossas redes:'.fontcolor("#453122");
        texto += '<div style=" width: 50%; display: flex; justify-content: space-around; text-align: center;">';
        texto += '    <a href="https://chat.whatsapp.com/DjRwmsDjKJUEUh9HLyFky2" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/whatsapp.png" /></a>';
        texto += '    <a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>';
        texto += '</div>';
        area.append(texto);
        this.vaiParaBaixo(true);
    };

    this.vaiParaBaixo = function (fromButton = false) {
        if (fromButton) {
            this.rolou_a_barra = false;
            botaoIrParaBaixo.hide();
        }
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.usuarioConectou = function (jogador) {
        const msg = jogador + ' acabou de entrar.';
        this.servidorDiz(msg);
    };

    this.usuarioDesconectou = function (jogador) {
        const msg = jogador + ' saiu.';
        this.servidorDiz(msg);
    };
};
