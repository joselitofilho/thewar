var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatGeral = function(area) {
    this.escreve = function(texto) {
        area.append(texto + '\n');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };
    
    this.limpa = function() {
        area.text('');
    };
    
    this.bemvindo = function() {
        this.escreve("Seja bem-vindo no servidor profissional!");
    };

    this.entrouNoJogo = function(jogador) {
        var texto = 'Servidor: ';
        texto += jogador + ' entrou.';
        this.escreve(texto);
    };
    
    this.saiuDoJogo = function(jogador, olheiro) {
        var texto = 'Servidor: ';
        texto += jogador + ' saiu.';
        this.escreve(texto);
    };
};
