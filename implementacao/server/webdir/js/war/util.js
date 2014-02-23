var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Util = function() {
    this.dataAtualFormatada = function() {
        var date = new Date();
        var year    = date.getFullYear();
        var month   = date.getMonth();
        var day     = date.getDate();
        var hour    = date.getHours();
        var minute  = date.getMinutes();
        var seconds = date.getSeconds();

        return day+"/"+month+"/"+year+" "+hour+":"+minute;
    };

    this.substituiURLPorHTMLLinks = function(texto) {
        var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        if (this.temImagemNaURL(texto)) {
            return texto.replace(exp,"<object data='$1'></object>"); 
        }

        return texto.replace(exp,"<a href='$1' target='_blank'>$1</a>"); 
    };

    this.imagemDaURLEstaValida = function(url) {
        var image_new = new Image();
        image_new.src = url;
        if ((image_new.width>0)&&(image_new.height>0)){
            return true;
        } else {
            return false;
        }
    };

    this.temImagemNaURL = function(texto) {
        if (/(jpg|gif|png)$/.test(texto)) {
            //return imagemDaURLEstaValida(texto);
            return true;
        }

        return false;
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
        fadein = setInterval(function() {
            opacidadeAtual += inc;

            if(opacidadeAtual >= MAX_ALPHA) {
                clearInterval(listaFadeinPoligono[codigoTerritorio]);
                listaFadeinPoligono[codigoTerritorio] = null;
                delete listaFadeinPoligono[codigoTerritorio];
                if(typeof(callback) == 'function')
                    callback();
                return;
            }
            
            polygon.setOptions({'fillOpacity': Math.min(MAX_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeinPoligono[codigoTerritorio] = fadein;
    }
}

function utilTerritorio_polygonFadeout(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeoutPoligono[codigoTerritorio] == null ) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = (MAX_ALPHA - MIN_ALPHA) / (milliseconds / 50.0);
        fadeout = setInterval(function() {            
            opacidadeAtual -= inc;

            if(opacidadeAtual <= MIN_ALPHA) {
                clearInterval(listaFadeoutPoligono[codigoTerritorio]);
                listaFadeoutPoligono[codigoTerritorio] = null;
                delete listaFadeoutPoligono[codigoTerritorio];
                if(typeof(callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.max(MIN_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeoutPoligono[codigoTerritorio] = fadeout;
    }
}
