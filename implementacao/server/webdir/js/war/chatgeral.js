var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatGeral = function(area) {
    this.escreve = function(texto) {
        area.append(texto + '<br/>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };
    
    this.limpa = function() {
        area.html('');
    };
    
    this.boasVindas = function() {
        this.escreve("<b>Seja bem-vindo ao servidor principal!</b>");
    };

    this.usuarioConectou = function(jogador) {
        var texto = 'Servidor: ';
        texto += jogador + ' acabou de entrar.';
        this.escreve(texto);
    };
    
    this.usuarioDesconectou = function(jogador, olheiro) {
        var texto = 'Servidor: ';
        texto += jogador + ' saiu.';
        this.escreve(texto);
    };
};
