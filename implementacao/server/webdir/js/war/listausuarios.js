var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.ListaUsuarios = function (elementoListaUsuarios) {
    this.getMapaLista = function () {
        const mapa = {};
        for (let i = 0; i < this.lista.length; ++i) {
            mapa[this.lista[i].nome] = this.lista[i];
        }
        return mapa;
    };

    this.preencheElementoHtml = function () {
        const nomeDoadores = this.doadores.map(d => d['nome']) || [];
        const conteudoDaLista = $('#lista_usuarios .conteudo');
        conteudoDaLista.html('');
        for (i = 0; i < this.lista.length; i++) {
            // const doador = this.lista[i].doador || false;
            const doador = nomeDoadores.includes(this.lista[i].nome) || false;
            let conteudo = "<div class='item'>";
            // conteudo += "<div class='foto imagem-soldado imagem-soldado-padrao'></div>";
            conteudo += "<div class='foto insignia_size insignias_x40_nv" + ranking_levelByXp(this.lista[i].pontos) + "'></div>";
            conteudo += "<div class='infos'>";
            conteudo += "    <div class='nome'>" + this.lista[i].nome + "</div>";
            conteudo += "    <div>";
            conteudo += "        <div class='trofeu'></div>";
            conteudo += "        <div class='pontos'>" + this.lista[i].posicaoNoRanking + "º | " + this.lista[i].pontos + " pts</div>";
            conteudo += "    </div>";
            conteudo += "</div>"; // infos.
            if (doador) {
                conteudo += "<div class='box_crown sala_menu_jogadores_box_crown'></div>";
            }
            conteudo += "</div>"; // item.
            conteudoDaLista.append(conteudo);
        }
    };

    this.ordenaLista = function (chave) {
        this.lista = this.lista.sort(function (a, b) {
            var x = a[chave];
            var y = b[chave];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    };

    this.carrega = function (lista) {
        this.lista = lista;
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };

    this.adiciona = function (info) {
        for (var i = 0; i < this.lista.length; i++)
            if (this.lista[i].nome === info.nome) return;
        this.lista.push(info);
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };

    this.remove = function (usuario) {
        var pos = -1;
        for (var i = 0; i < this.lista.length; i++)
            if (this.lista[i].nome === usuario) {
                pos = i;
                break;
            }
        if (pos !== -1) {
            this.lista.splice(pos, 1);
        }
        this.ordenaLista("nome");
        this.preencheElementoHtml();
    };

    this.atualizaPontuacao = function (ranking) {
        if (this.lista) {
            const mapaRanking = {};
            for (let i = 0; i < ranking.length; ++i) {
                mapaRanking[ranking[i].nome] = ranking[i];
            }
            let teveMudanca = false;
            for (let i = 0; i < this.lista.length; ++i) {
                const l = this.lista[i];
                if (this.lista[i].posicaoNoRanking !== mapaRanking[l.nome].posicaoNoRanking ||
                    this.lista[i].pontos !== mapaRanking[l.nome].pontos) {
                    this.lista[i].posicaoNoRanking = mapaRanking[l.nome].posicaoNoRanking;
                    this.lista[i].pontos = mapaRanking[l.nome].pontos;
                    teveMudanca = true;
                }
            }
            if (teveMudanca) {
                this.preencheElementoHtml();
            }
        }
    };

    this.atualizaDoadores = function (doadores) {
        this.doadores = doadores;
        this.preencheElementoHtml();
    };
};
