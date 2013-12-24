var listaFadeinPoligono = {};
var listaFadeoutPoligono = {};

function utilTerritorio_polygonFadein(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeinPoligono[codigoTerritorio] == null) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = 0.5 / (milliseconds / 50.0);
        fadein = setInterval(function() {
            opacidadeAtual += inc;

            if(opacidadeAtual >= 1.0) {
                clearInterval(listaFadeinPoligono[codigoTerritorio]);
                listaFadeinPoligono[codigoTerritorio] = null;
                delete listaFadeinPoligono[codigoTerritorio];
                if(typeof(callback) == 'function')
                    callback();
                return;
            }
            
            polygon.setOptions({'fillOpacity': Math.min(1.0, Number(opacidadeAtual))});
        }, 50);

        listaFadeinPoligono[codigoTerritorio] = fadein;
    }
}

function utilTerritorio_polygonFadeout(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeoutPoligono[codigoTerritorio] == null ) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = 0.5 / (milliseconds / 50.0);
        fadeout = setInterval(function() {            
            opacidadeAtual -= inc;

            if(opacidadeAtual <= 0.5) {
                clearInterval(listaFadeoutPoligono[codigoTerritorio]);
                listaFadeoutPoligono[codigoTerritorio] = null;
                delete listaFadeoutPoligono[codigoTerritorio];
                if(typeof(callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.max(0.5, Number(opacidadeAtual))});
        }, 50);

        listaFadeoutPoligono[codigoTerritorio] = fadeout;
    }
}
