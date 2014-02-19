var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatJogo = function(area) {

    this.escreveColorido = function(texto, indiceCor) {
        if (indiceCor == 0) texto = texto.fontcolor("#841D0F");
        else if (indiceCor == 1) texto = texto.fontcolor("#262165");
        else if (indiceCor == 2) texto = texto.fontcolor("#214A29");
        else if (indiceCor == 3) texto = texto.fontcolor("#282423");
        else if (indiceCor == 4) texto = texto.fontcolor("#F8F7E9");
        else if (indiceCor == 5) texto = texto.fontcolor("#DFE136");
        else texto = texto.fontcolor("#494949");

        this.escreve(texto);
    };

    this.escreve = function(texto) {
        area.append(texto + '</br>');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };
    
    this.limpa = function() {
        area.text('');
    };

    this.colocaTropa = function(usuario, territorio, quantidade) {
        var texto = 'Servidor: ' + 
            usuario + ' colocou ';
        if (quantidade > 1)
            texto += quantidade + ' exércitos';
        else
            texto += quantidade + ' exército';
        texto += ' no território ' + territorio + '.';
        //this.escreve(texto);
    };

    this.ataque = function(jogadorAtaque, territoriosDoAtaque,
            jogadorDefesa, territorioDaDefesa) {
        var territoriosDoAtaqueTexto = territoriosDoAtaque[0].codigo;
        for (i = 1; i < territoriosDoAtaque.length - 1; i++) 
            territoriosDoAtaqueTexto += ', ' + territoriosDoAtaque[i].codigo;
        
        if (territoriosDoAtaque.length > 1)
            territoriosDoAtaqueTexto += ' e ' + territoriosDoAtaque[territoriosDoAtaque.length-1].codigo;

        var texto  = 'Servidor: ' +
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
        //this.escreve(texto);
    };
    
    this.moveu = function(jogador, doTerritorio, paraOTerritorio, quantidade) {
        var texto = 'Servidor: ';
        texto += jogador + ' moveu ' + quantidade;
        if (quantidade > 1) texto += ' exércitos';
        else texto += ' exército';
        texto += ' do território ' + doTerritorio;
        texto += ' para o território ' + paraOTerritorio + '.';
        //this.escreve(texto);
    };
    
    this.conquistouTerritorio = function(jogador, territorio) {
        var texto = 'Servidor: ';
        texto += jogador + ' conquistou o território ' + territorio + '.';
        //this.escreve(texto);
    };
    
    this.entrouNoJogo = function(jogador, olheiro) {
        var texto = '<b>Servidor</b>: ';
        if (olheiro) texto += jogador + ' está assintindo a partida.';
        else texto += jogador + ' voltou para o jogo.';
        this.escreveColorido(texto, -1);
    };
    
    this.saiuDoJogo = function(jogador, olheiro) {
        var texto = '<b>Servidor</b>: ';
        if (olheiro) texto += jogador + ' não está mais assistindo a partida.';
        else texto += jogador + ' saiu do jogo.';
        this.escreveColorido(texto, -1);
    };
};
