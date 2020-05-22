var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ChatGeral = function (area) {
    this.util = new jogos.war.Util();

    this.escreve = function (params, indiceCor) {
        let texto;
        if (indiceCor === -1) {
            texto = "<i><b>Servidor:</b> " + msg + "</i>";
        } else {
            texto = "<b>" + params.usuario + "</b> diz:<br/>" + params.texto;
        }

        texto = this.util.substituiMarcacoes(_listaUsuarios.getMapaLista(), params.usuario, texto);

        if (indiceCor === -1) {
            texto = texto.fontcolor("#494949");
        } // Servidor.
        else {
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
        let texto = '<b>Seja bem-vindo ao servidor principal!</b>';
        texto = texto.fontcolor("#453122");
        area.append(texto + '<br/>');
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
