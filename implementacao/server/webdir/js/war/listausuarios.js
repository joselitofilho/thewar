var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ListaUsuarios = function(elementoListaUsuarios) {
    var lista = [];
    _conteudoDaLista = $('#lista_usuarios .conteudo');

    this.preencheElementoHtml = function() {
        _conteudoDaLista.html('');
        for (i=0; i<this.lista.length; i++) {
            conteudo = "<div class='item'>";
            conteudo += "<div class='foto imagem-soldado imagem-soldado-padrao'></div>";
            conteudo += "<div class='infos'>";
            conteudo += "<div class='nome'>"+this.lista[i].nome+"</div>";
            conteudo += "<div>";
            conteudo += "<div class='trofeu'></div>";
            conteudo += "<div class='pontos'>"+this.lista[i].posicaoNoRanking+"º | "+this.lista[i].pontos+" pts</div>";
            conteudo += "<div>";
            conteudo += "</div>"; // infos.
            conteudo += "</div>"; // item.
            _conteudoDaLista.append(conteudo);
        }
    };

    this.ordenaLista = function(chave) {
        this.lista = this.lista.sort(function(a, b) {
            var x = a[chave]; var y = b[chave];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    };

    this.carrega = function(lista) {
        this.lista = lista;
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };

    this.adiciona = function(info) {
        for(var i = 0; i < this.lista.length; i++)
            if (this.lista[i].nome == info.nome) return;
        this.lista.push(info);
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };

    this.remove = function(usuario) {
        var pos = -1;
        for(var i = 0; i < this.lista.length; i++)
            if (this.lista[i].nome == usuario) {
                pos = i;
                break;
            }
        if (pos != -1) {
            this.lista.splice(pos,1);
        }
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };
};
