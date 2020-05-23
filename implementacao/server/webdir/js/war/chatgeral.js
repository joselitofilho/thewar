var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ChatGeral = function (area) {
    this.util = new jogos.war.Util();

    this.escreve = function (params, indiceCor) {
        const mensagemServidor = (indiceCor === -1);

        let texto = this.util.substituiMarcacoes(_listaUsuarios.getMapaLista(), params.usuario, params.texto);
        if (mensagemServidor) {
            texto = "<i><b>Servidor:</b>&nbsp;" + texto + "</i>";
            texto = texto.fontcolor("#494949");
        } else {
            texto = "<b>" + params.usuario + "</b> diz:<br/>" + texto;
            texto = texto.fontcolor("#453122");
        }

        area.append(texto + '<br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.servidorDiz = function (msg) {
        this.escreve({usuario: 'Servidor', texto: msg}, -1);
    };

    this.limpa = function () {
        area.html('');
    };

    this.boasVindas = function () {
        let texto = '<h4>Seja bem-vindo ao servidor principal!</h4>';
        texto += 'Connect-se a uma de nossas redes:';
        texto = texto.fontcolor("#453122");
        texto += '<div style=" width: 50%; display: flex; justify-content: space-around; text-align: center;">';
        texto += '    <a href="https://chat.whatsapp.com/DjRwmsDjKJUEUh9HLyFky2" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/whatsapp.png" /></a>';
        texto += '    <a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>';
        texto += '</div>';
        area.append(texto);
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
