var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Util = function () {
    const _comandos = {
        lista: ["bial1", "bial2", "bial3", "bial4", "capitao1", "capitao2", "discord", "joker1", "rank", "whatsapp"],
        bial1: {regex: /:bial1/g, html: "<img src='../imagens/memes/bial1.jpeg'/>"},
        bial2: {regex: /:bial2/g, html: "<img src='../imagens/memes/bial2.jpeg'/>"},
        bial3: {regex: /:bial3/g, html: "<img src='../imagens/memes/bial3.jpeg'/>"},
        bial4: {regex: /:bial4/g, html: "<img src='../imagens/memes/bial4.jpeg'/>"},
        capitao1: {regex: /:capitao1/g, html: "<img src='../imagens/memes/capitao1.jpeg'/>"},
        capitao2: {regex: /:capitao2/g, html: "<img src='../imagens/memes/capitao2.jpeg'/>"},
        discord: {
            regex: /:discord/g,
            html: '<a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>'
        },
        rank: {regex: /:rank/g, html: "<div class='comando_rank insignia_size insignias_x40_nv{level}'></div>"},
        joker1: {regex: /:joker1/g, html: "<img src='../imagens/memes/joker1.jpeg'/>"},
        whatsapp: {
            regex: /:whatsapp/g,
            html: '<a href=\"https://chat.whatsapp.com/DjRwmsDjKJUEUh9HLyFky2\" target=\"_blank\" rel=\"noopener noreferrer\"><img height=\"64px\" src=\"../../imagens/social/whatsapp.png\" /></a>'
        },
    };

    this.dataAtualFormatada = function () {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDate();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var seconds = date.getSeconds();

        return day + "/" + month + "/" + year + " " + hour + ":" + minute;
    };

    this.substituiMarcacoes = function (listaUsuarios, usuarioQueEnviou, texto) {
        if (texto.includes(":comandos")) {
            return "Memes disponíveis --> " + ":" + Array.from(_comandos.lista).join(', :');
        }
        texto = this.substituiURLPorHTMLLinks(texto);
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
    var caracteresInvalidos = 'àèìòùâêîôûäëïöüáéíóúãõÀÈÌÒÙÂÊÎÔÛÄËÏÖÜÁÉÍÓÚÃÕ';
    var caracteresValidos = 'aeiouaeiouaeiouaeiouaoAEIOUAEIOUAEIOUAEIOUAO';

    for (i = 0; i < caracteresInvalidos.length; i++) {
        if (palavra.indexOf(caracteresInvalidos.charAt(i)) != -1) {
            nova = caracteresValidos.charAt(i);
            palavra = palavra.replace(caracteresInvalidos.charAt(i), nova);
        }
    }

    var acento = "\"'´`^¨~";
    for (i = 0; i < acento.length; i++) {
        if (palavra.indexOf(acento.charAt(i)) != -1) {
            nova = caracteresValidos.charAt(i);
            palavra = palavra.replace(acento.charAt(i), '');
        }
    }

    return palavra;
}
