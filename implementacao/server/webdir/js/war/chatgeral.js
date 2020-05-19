var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ChatGeral = function (area) {
    this.util = new jogos.war.Util();

    this.escreve = function (texto, indiceCor) {
        texto = this.util.substituiURLPorHTMLLinks(texto);

        if (indiceCor == -1) texto = texto.fontcolor("#494949"); // Servidor.
        else texto = texto.fontcolor("#453122");

        area.append(texto + '<br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.servidorDiz = function (msg) {
        var texto = '<i><b>Servidor:</b> ';
        texto += msg;
        texto += "</i>";
        this.escreve(texto, -1);
    };

    this.limpa = function () {
        area.html('');
    };

    this.boasVindas = function () {
        texto = '<b>Seja bem-vindo ao servidor principal!</b>';
        texto = texto.fontcolor("#453122");
        area.append(texto + '<br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.usuarioConectou = function (jogador) {
        msg = jogador + ' acabou de entrar.';
        this.servidorDiz(msg);
    };

    this.usuarioDesconectou = function (jogador) {
        msg = jogador + ' saiu.';
        this.servidorDiz(msg);
    };
};
