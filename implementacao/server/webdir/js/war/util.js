var jogos = jogos || {};
jogos.war = jogos.war || {};

function util_handleQuestionAnswer(pergunta, resposta) {
    const texto = "Minha resposta é \"" + resposta + "\" para a pergunta \"" + pergunta + "\"";
    if (_chatJogo && _chatJogo.estaAtivo()) {
        _chatJogo.handleQuestionAnswerCallback(texto);
    } else if (_chatGeral) {
        _chatGeral.handleQuestionAnswerCallback(texto);
    }
}

jogos.war.Util = function () {

    const _comandos = {
        lista: [
            "rank"
        ],
        rank: {regex: /:rank/g, html: "<div class='comando_rank insignia_x40_size insignias_x40_nv{level}'></div>"}
    };

    this.dataAtualFormatada = function () {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDate();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var seconds = date.getSeconds();

        // return day + "/" + month + "/" + year + " " + hour + ":" + minute;
        return hour + ":" + minute;
    };

    this.substituiMarcacoes = function (listaUsuarios, usuarioQueEnviou, texto) {
        if (texto.match(/:comandos/) || texto.match(/:memes/) || texto.match(/:help/)) {
            return "Memes disponíveis --> " + ":" + Array.from(_comandos.lista).join(', :');
        }
        if (!texto.match(/a href/)) {
            // TODO: Colocar a interpretação de urls para o backend.
            texto = this.substituiURLPorHTMLLinks(texto);
        }
        texto = this.substituiComandos(listaUsuarios, usuarioQueEnviou, texto);
        return texto;
    };

    this.substituiURLPorHTMLLinks = function (texto) {
        var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        var urls = texto.match(exp);
        if (urls) {
            for (i = 0; i < urls.length; i++) {
                if (this.temImagemNaURL(urls[i]))
                    texto = texto.replace(urls[i], "<object data='" + urls[i] + "'></object>");
                else
                    texto = texto.replace(urls[i], "<a href='" + urls[i] + "' target='_blank'>" + urls[i] + "</a>");
            }
        }
        return texto;
    };

    this.temImagemNaURL = function (texto) {
        return (/(jpg|gif|png)$/.test(texto));
    };

    this.substituiComandos = function (listaUsuarios, usuarioQueEnviou, texto) {
        for (let i = 0; i < _comandos.lista.length; ++i) {
            const cmdKey = _comandos.lista[i];
            const cmd = _comandos[cmdKey];
            if (cmdKey === "rank") {
                if (listaUsuarios[usuarioQueEnviou]) {
                    const level = ranking_levelByXp(listaUsuarios[usuarioQueEnviou].pontos);
                    const elemento = cmd.html.replace("{level}", level);
                    texto = texto.replace(cmd.regex, elemento);
                }
            } else {
                texto = texto.replace(cmd.regex, cmd.html);
            }
        }
        return texto;
    };
};

var listaFadeinPoligono = {};
var listaFadeoutPoligono = {};

var MAX_ALPHA = 1.0;
var MIN_ALPHA = 0.5;

function utilTerritorio_polygonFadein(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeinPoligono[codigoTerritorio] == null) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = (MAX_ALPHA - MIN_ALPHA) / (milliseconds / 50.0);
        fadein = setInterval(function () {
            opacidadeAtual += inc;

            if (opacidadeAtual >= MAX_ALPHA) {
                clearInterval(listaFadeinPoligono[codigoTerritorio]);
                listaFadeinPoligono[codigoTerritorio] = null;
                delete listaFadeinPoligono[codigoTerritorio];
                if (typeof (callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.min(MAX_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeinPoligono[codigoTerritorio] = fadein;
    }
}

function utilTerritorio_polygonFadeout(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeoutPoligono[codigoTerritorio] == null) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = (MAX_ALPHA - MIN_ALPHA) / (milliseconds / 50.0);
        fadeout = setInterval(function () {
            opacidadeAtual -= inc;

            if (opacidadeAtual <= MIN_ALPHA) {
                clearInterval(listaFadeoutPoligono[codigoTerritorio]);
                listaFadeoutPoligono[codigoTerritorio] = null;
                delete listaFadeoutPoligono[codigoTerritorio];
                if (typeof (callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.max(MIN_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeoutPoligono[codigoTerritorio] = fadeout;
    }
}

function utilRetiraAcento(palavra) {
    return palavra.replace(/[\W_]+/g, " ");
}
