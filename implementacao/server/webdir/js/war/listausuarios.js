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
        let nomeDoadores = [];
        if (this.doadores) {
            nomeDoadores = this.doadores.map(d => d['nome']);
        }
        const conteudoDaLista = $('#lista_usuarios .conteudo');
        conteudoDaLista.html('');
        for (i = 0; i < this.lista.length; i++) {
            // const doador = this.lista[i].doador || false;
            const doador = nomeDoadores.includes(this.lista[i].nome) || false;
            let conteudo =
                "<div class='item' onclick='perfil_jogador_onclick(\"" + this.lista[i].nome + "\", \"human\");'>";
            conteudo += "<div class='grow1'><div class='foto insignia_x40_size insignias_x40_nv" + ranking_levelByXp(this.lista[i].pontos) + "'></div></div>";
            conteudo += "<div class='grow6 infos'>";
            conteudo += "    <div class='nome'>" + this.lista[i].nome + "</div>";
            conteudo += "    <div>";
            conteudo += '        <svg class="trofeu" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M19 1c0 9.803-5.094 13.053-5.592 17h-2.805c-.498-3.947-5.603-7.197-5.603-17h14zm-7.305 13.053c-1.886-3.26-2.635-7.432-2.646-11.053h-1.699c.205 4.648 1.99 8.333 4.345 11.053zm1.743 4.947h-2.866c-.202 1.187-.63 2.619-2.571 2.619v1.381h8v-1.381c-1.999 0-2.371-1.432-2.563-2.619zm7.08-1.596c-1.402-.634-2.609-.19-3.354.293.745-.484 1.603-1.464 1.595-3.003-2.591 1.038-2.295 2.496-2.765 3.345-.315.571-1.007.274-1.007.274l-.213.352c.365.193.989.319 1.716.319 1.307 0 2.949-.409 4.028-1.58zm2.444-4.022c-1.382.097-2.118 1.061-2.501 1.763.383-.702.614-1.942-.05-3.158-1.61 1.929-.752 2.958-.762 3.831-.004.427-.49.417-.49.417l.007.404c.314-.041 3.154-.717 3.796-3.257zm1.036-3.87c-1.171.426-1.56 1.473-1.718 2.175.158-.702.041-1.863-.835-2.75-.915 2.068.082 2.745.29 3.503.102.371-.325.606-.325.606l.29.179c.061-.029 2.385-1.332 2.298-3.713zm-.2-3.792c-.903.666-1.017 1.688-.974 2.335-.042-.646-.395-1.639-1.376-2.182-.264 2.018.769 2.349 1.142 2.95.182.294.023.658.023.658l.284-.019s.026-.127.169-.442c.291-.644 1.255-1.334.732-3.3zm-1.901-2.72s-.273.984-.045 1.732c.244.798.873 1.361.873 1.361s.34-.873.099-1.733c-.222-.792-.927-1.36-.927-1.36zm-12.67 15.665l-.213-.352s-.691.297-1.007-.274c-.47-.849-.174-2.307-2.765-3.345-.008 1.539.85 2.52 1.595 3.003-.745-.484-1.952-.927-3.354-.293 1.078 1.171 2.721 1.581 4.028 1.581.727-.001 1.35-.127 1.716-.32zm-4.393-2.027l.007-.404s-.486.01-.49-.417c-.009-.873.848-1.901-.762-3.831-.664 1.216-.433 2.457-.05 3.158-.383-.702-1.12-1.666-2.501-1.763.642 2.541 3.482 3.217 3.796 3.257zm-2.533-3.413l.29-.179s-.427-.236-.325-.606c.208-.758 1.205-1.435.29-3.503-.876.887-.994 2.048-.835 2.75-.158-.702-.546-1.749-1.718-2.175-.088 2.381 2.236 3.684 2.298 3.713zm-1.366-4.204c.143.315.169.442.169.442l.284.019s-.159-.364.023-.658c.373-.601 1.405-.933 1.142-2.95-.983.542-1.335 1.534-1.377 2.181.042-.647-.072-1.67-.974-2.335-.523 1.966.441 2.656.733 3.301zm.241-4.661c-.24.86.099 1.733.099 1.733s.629-.563.873-1.361c.228-.748-.045-1.732-.045-1.732s-.705.568-.927 1.36z"></path></svg>';
            conteudo += "        <div class='pontos'>" + this.lista[i].posicaoNoRanking + "º | " + this.lista[i].pontos + " pts</div>";
            conteudo += "    </div>";
            conteudo += "</div>"; // infos.
            conteudo += "<div class='grow1'>";
            if (doador) {
                conteudo += "<div class='box_crown sala_menu_jogadores_box_crown' title='Doador'></div>";
            }
            conteudo += "</div>";
            conteudo +=
                "</div>"; // item.
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
