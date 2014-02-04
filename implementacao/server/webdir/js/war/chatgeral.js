var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ChatGeral = function(area) {
    this.util = new jogos.war.Util();

    this.escreve = function(texto) {
        var dataHora = this.util.dataAtualFormatada();
        area.append(dataHora + " " + texto + '<br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };
    
    this.limpa = function() {
        area.html('');
    };
    
    this.boasVindas = function() {
        area.append('<b>Seja bem-vindo ao servidor principal!</b><br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.usuarioConectou = function(jogador) {
        var texto = '<b>Servidor:</b> ';
        texto += jogador + ' acabou de entrar.';
        this.escreve(texto);
    };
    
    this.usuarioDesconectou = function(jogador) {
        var texto = '<b>Servidor:</b> ';
        texto += jogador + ' saiu.';
        this.escreve(texto);
    };
};
