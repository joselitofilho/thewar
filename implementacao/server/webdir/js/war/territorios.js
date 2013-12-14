var gpscheck = gpscheck || {};
gpscheck.mapa = gpscheck.mapa || {};

var _labelTerritorios = {};
var _markerTerritorios = {};

gpscheck.mapa.Territorios = function(mapa) {

	var poligonos_dos_territorios = {};
	
	this.desenhaGrupoTerritorio = function(paises, corDaBorda, corDoPreenchimento) {
        $.each(paises, function(i, pais) {
            var poligono_pais = new google.maps.Polygon({
                map: mapa,
                paths: pais.territorio,
                strokeColor: corDaBorda,
                strokeOpacity: 1,
                strokeWeight: 2,
                fillColor: corDoPreenchimento,
                fillOpacity: 0.5,
                zIndex: 1
            });

            google.maps.event.addListener(poligono_pais, 'click', function(event) {
                var colocarTropaMsg = comunicacao_colocarTropa(_labelTerritorios[pais.nome].posicaoJogador, pais.nome, 1);
                _libwebsocket.enviarObjJson(colocarTropaMsg);
            });
        });
    };
    
    this.desenha = function() {
        this.carregaTerritorios();
    
        // America do Norte.
        this.desenhaGrupoTerritorio([
            coordenada_alaska,
            coordenada_california,
            coordenada_groelandia,
            coordenada_labrador,
            coordenada_mackenzie,
            coordenada_mexico,
            coordenada_nova_york,
            coordenada_ottawa,
            coordenada_vancouver
        ], "#666600", "#FFFF00");
        
        // Africa.
        this.desenhaGrupoTerritorio([
            coordenada_africa_do_sul,
            coordenada_argelia,
            coordenada_congo,
            coordenada_egito,
            coordenada_madagascar,
            coordenada_sudao
        ], "#330033", "#FF99FF");
        
        // America do Sul.
        this.desenhaGrupoTerritorio([
            coordenada_argentina, 
            coordenada_brasil,
            coordenada_chile,
            coordenada_colombia
        ], "#003300", "#008000");
        
        // Oceania.
        this.desenhaGrupoTerritorio([
            coordenada_australia,
            coordenada_borneo,
            coordenada_nova_guine,
            coordenada_sumatra
        ], "#660000", "#FF6666");
        
        // Europa.
        this.desenhaGrupoTerritorio([
            coordenada_alemanha,
            coordenada_inglaterra,
            coordenada_islandia,
            coordenada_moscou,
            coordenada_polonia,
            coordenada_portugal,
            coordenada_suecia
        ], "#000099", "#66FFFF");
        
        // Asia
        this.desenhaGrupoTerritorio([
            coordenada_aral,
            coordenada_china,
            coordenada_india,
            coordenada_japao,
            coordenada_mongolia,
            coordenada_oriente_medio,
            coordenada_vietna,
            coordenada_vladivostok
        ], "#CC6600", "#FFCC33");
    };

	this.carregaTerritorios = function() {
		var territorios = {};

		territorios["AfricaDoSul"] = coordenada_africa_do_sul;
		territorios["Alaska"] = coordenada_alaska;
		territorios["Alemanha"] = coordenada_alemanha;
		territorios["Aral"] = coordenada_aral;
		territorios["Argelia"] = coordenada_argelia;
		territorios["Argentina"] = coordenada_argentina;
		territorios["Australia"] = coordenada_australia;
		territorios["Borneo"] = coordenada_borneo;
		territorios["Brasil"] = coordenada_brasil;
		territorios["California"] = coordenada_california;
		territorios["Chile"] = coordenada_chile;
		territorios["China"] = coordenada_china;
		territorios["Colombia"] = coordenada_colombia;
		territorios["Congo"] = coordenada_congo;
		territorios["Egito"] = coordenada_egito;
		territorios["Groelandia"] = coordenada_groelandia;
		territorios["India"] = coordenada_india;
		territorios["Inglaterra"] = coordenada_inglaterra;
		territorios["Islandia"] = coordenada_islandia;
		territorios["Japao"] = coordenada_japao;
		territorios["Labrador"] = coordenada_labrador;
		territorios["Madagascar"] = coordenada_madagascar;
		territorios["Mackenzie"] = coordenada_mackenzie;
		territorios["Mexico"] = coordenada_mexico;
		territorios["Mongolia"] = coordenada_mongolia;
		territorios["Moscou"] = coordenada_moscou;
		territorios["NovaGuine"] = coordenada_nova_guine;
		territorios["NovaYork"] = coordenada_nova_york;
		territorios["OrienteMedio"] = coordenada_oriente_medio;
		territorios["Ottawa"] = coordenada_ottawa;
		territorios["Polonia"] = coordenada_polonia;
		territorios["Portugal"] = coordenada_portugal;
		territorios["Sudao"] = coordenada_sudao;
		territorios["Suecia"] = coordenada_suecia;
		territorios["Sumatra"] = coordenada_sumatra;
		territorios["Vancouver"] = coordenada_vancouver;
		territorios["Vietna"] = coordenada_vietna;
		territorios["Vladivostok"] = coordenada_vladivostok;

		return territorios;
	};
	
	this.corDeFundoDaPosicao = function(posicao) {
	    var corDeFundo = '#555';
        switch(posicao) {
            case 0:
                corDeFundo = '#FA0C01';
                break;
            case 1:
                corDeFundo = '#00008B';
                break;
            case 2:
                corDeFundo = '#006400';
                break;
            case 3:
                corDeFundo = '#FFF';
                break;
            case 4:
                corDeFundo = '#000';
                break;
            case 5:
                corDeFundo = '#FFD700';
                break;
        }
        
        return corDeFundo;
	}
	
	this.corDoTextoDaPosicao = function(posicao) {
	    var corDoTexto = '#FFF';
        if (posicao == 3) corDoTexto = '#000';
        
        return corDoTexto;
	}

	this.iniciaLabelDosTerritorios = function(territorios, posicaoJogador) {
		var territorioJs = this.carregaTerritorios();
        
        var corDeFundo = this.corDeFundoDaPosicao(posicaoJogador);
        var corDoTexto = this.corDoTextoDaPosicao(posicaoJogador);

        var circulo = {
            path: google.maps.SymbolPath.CIRCLE, 
            fillColor: corDeFundo,
            fillOpacity: 0.8,
            scale: 15,
            strokeColor: "#000000",
            strokeWeight: 2
        };

		$.each(territorios, function(i, territorio) {
			if (territorioJs[territorio.codigo]) {
				var posicao = territorioJs[territorio.codigo].centro;
		        var marker = new google.maps.Marker({
		            position: posicao,
		            map: mapa,
		            icon: circulo,
		            title: territorio.nome,
		            zIndex: 2
		        });
		        
		        var label = new Label({
                    map: mapa
                }, corDoTexto);
                label.bindTo('position', marker, 'position');
                label.bindTo('text', marker, 'position');
               
                label.texto = '1';
                label.posicaoJogador = posicaoJogador;

                label.metadata = {pos: posicaoJogador};

                _markerTerritorios[territorio.codigo] = marker;
                _labelTerritorios[territorio.codigo] = label;

                google.maps.event.addListener(marker, 'click', function(event) {
                    var colocarTropaMsg = comunicacao_colocarTropa(_labelTerritorios[territorio.codigo].posicaoJogador, territorio.codigo, 1);
                    _libwebsocket.enviarObjJson(colocarTropaMsg);
                });
			}
		});
	};
};
