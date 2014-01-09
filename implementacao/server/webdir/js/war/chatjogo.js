var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.ChatJogo = function(area) {
    this.escreve = function(texto) {
        area.append(texto + '\n');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };

    this.colocaTropa = function(usuario, territorio, quantidade) {
        var texto = 'Servidor: ' + 
            usuario + ' colocou ';
        if (quantidade > 1)
            texto += quantidade + ' exércitos';
        else
            texto += quantidade + ' exército';
        texto += ' no território ' + territorio + '.';
        this.escreve(texto);
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
        this.escreve(texto);
    };
};
