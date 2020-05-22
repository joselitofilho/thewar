var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Util = function () {
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
        if (listaUsuarios[usuarioQueEnviou]) {
            const level = ranking_levelByXp(listaUsuarios[usuarioQueEnviou].pontos);
            const exp = /:rank/g;
            texto = texto.replace(exp, "<div class='comando_rank insignia_size insignias_x40_nv" + level + "'></div>");
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
