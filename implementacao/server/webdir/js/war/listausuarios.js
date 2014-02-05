var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ListaUsuarios = function(elementoListaUsuarios) {
    var lista = [];

    this.preencheElementoHtml = function() {
        elementoListaUsuarios.html('');
        for (i=0; i<this.lista.length; i++) {
            elementoListaUsuarios.append("<div>"+this.lista[i]+"</div>");
        }
    };

    this.carrega = function(lista) {
        this.lista = lista.sort();
        this.preencheElementoHtml();
    };

    this.adiciona = function(usuario) {
        if (this.lista.indexOf(usuario) == -1) {
            this.lista.push(usuario);
        }
        this.lista.sort();
        this.preencheElementoHtml();
    };

    this.remove = function(usuario) {
        var pos = this.lista.indexOf(usuario);
        if (pos != -1) {
            this.lista.splice(pos,1);
        }
        this.lista.sort();
        this.preencheElementoHtml();
    };
};
