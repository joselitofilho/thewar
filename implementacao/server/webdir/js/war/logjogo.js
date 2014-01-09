var jogowar = jogowar || {};
jogowar.war = jogowar.war || {};

jogowar.war.LogJogo = function(area) {
    this.colocaTropa = function(usuario, territorio, quantidade) {
        area.append('Servidor: ' + 
            usuario + ' colocou ' + 
            quantidade + ' exército(s) no território ' + 
            territorio + '.\n');
        area.scrollTop(
            area[0].scrollHeight - area.height()
        );
    };
};
