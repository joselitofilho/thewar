var gpscheck = gpscheck || {};
gpscheck.mapa = gpscheck.mapa || {};

var _labelTerritorios = {};
var _markerTerritorios = {};
var _poligonosTerritorios = {};

gpscheck.mapa.Territorios = function(mapa) {

    var COR_BORDA_AMERICA_DO_NORTE = "#222";//"#666600";
    var COR_PREENCHIMENTO_AMERICA_DO_NORTE = "#FFFF00";
    var COR_BORDA_AMERICA_DO_SUL = "#222";//"#003300";
    var COR_PREENCHIMENTO_AMERICA_DO_SUL = "#008000";
    var COR_BORDA_ASIA = "#222";//"#CC6600";
    var COR_PREENCHIMENTO_ASIA = "#FFCC33";
    var COR_BORDA_EUROPA = "#222";//"#000099";
    var COR_PREENCHIMENTO_EUROPA = "#66FFFF";
    var COR_BORDA_AFRICA = "#222";//"#330033";
    var COR_PREENCHIMENTO_AFRICA = "#FF99FF";
    var COR_BORDA_OCEANIA = "#222";//"#660000";
    var COR_PREENCHIMENTO_OCEANIA = "#FF6666";
    
    territorioClick = null;
    fronteiras = {};

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
	
	this.iniciaMapaDasFronteiras = function() {
	    fronteiras["Argentina"] = ["Brasil", "Chile"];
        fronteiras["Brasil"] = ["Argentina", "Chile", "Colombia", "Argelia"];
        fronteiras["Chile"] = ["Argentina", "Brasil", "Colombia"];
        fronteiras["Colombia"] = ["Brasil", "Chile", "Mexico"];

        fronteiras["Mexico"] = ["Colombia", "NovaYork", "California"];
        fronteiras["California"] = ["Mexico", "NovaYork", "Vancouver", "Ottawa"];
        fronteiras["NovaYork"] = ["Mexico", "Ottawa", "Labrador", "California"];
        fronteiras["Vancouver"] = ["California", "Ottawa", "Alaska", "Mackenzie"];
        fronteiras["Ottawa"] = ["Mackenzie", "Vancouver", "California", "NovaYork", "Labrador"];
        fronteiras["Labrador"] = ["Groelandia", "Ottawa", "NovaYork"];
        fronteiras["Alaska"] = ["Mackenzie", "Vancouver", "Vladivostok"];
        fronteiras["Mackenzie"] = ["Alaska", "Vancouver", "Ottawa", "Groelandia"];
        fronteiras["Groelandia"] = ["Mackenzie", "Labrador", "Islandia"];
        
        fronteiras["Islandia"] = ["Groelandia", "Inglaterra"];
        fronteiras["Inglaterra"] = ["Islandia", "Portugal", "Alemanha", "Suecia"];
        fronteiras["Suecia"] = ["Inglaterra", "Moscou"];
        fronteiras["Moscou"] = ["Suecia", "Polonia", "OrienteMedio", "Aral", "Omsk"];
        fronteiras["Polonia"] = ["Moscou", "OrienteMedio", "Egito", "Alemanha"];
        fronteiras["Alemanha"] = ["Portugal", "Polonia"];
        fronteiras["Portugal"] = ["Alemanha", "Inglaterra", "Argelia", "Egito"];
        
        fronteiras["Argelia"] = ["Portugal", "Brasil", "Congo", "Sudao", "Egito"];
        fronteiras["Egito"] = ["Argelia", "Sudao", "OrienteMedio", "Polonia", "Portugal"];
        fronteiras["Sudao"] = ["Egito", "Argelia", "Congo", "AfricaDoSul", "Madagascar"];
        fronteiras["Congo"] = ["Argelia", "AfricaDoSul", "Sudao"];
        fronteiras["AfricaDoSul"] = ["Congo", "Sudao", "Madagascar"];
        fronteiras["Madagascar"] = ["Sudao", "AfricaDoSul"];
        
        fronteiras["OrienteMedio"] = ["Egito", "Polonia", "Moscou", "Aral", "India"];
        fronteiras["India"] = ["Sumatra", "Vietna", "China", "Aral", "OrienteMedio"];
        fronteiras["Vietna"] = ["Borneo", "China", "India"];
        fronteiras["Aral"] = ["Moscou", "Omsk", "China", "India", "OrienteMedio"];
        fronteiras["China"] = ["Vietna", "Japao", "Vladivostok", "Tchita", "Mongolia", "Omsk", "Aral", "India"];
        fronteiras["Japao"] = ["Vladivostok", "China"];
        fronteiras["Omsk"] = ["Moscou", "Aral", "China", "Mongolia", "Dudinka"];
        fronteiras["Mongolia"] = ["Dudinka", "Omsk", "China", "Tchita"];
        fronteiras["Dudinka"] = ["Omsk", "Mongolia", "Tchita", "Siberia"];
        fronteiras["Tchita"] = ["Siberia", "Dudinka", "Mongolia", "Vladivostok"];
        fronteiras["Siberia"] = ["Dudinka", "Tchita", "Vladivostok"];
        fronteiras["Vladivostok"] = ["Siberia", "Tchita", "China", "Japao"];
        
        fronteiras["Australia"] = ["NovaGuine", "Sumatra", "Borneo"];
        fronteiras["NovaGuine"] = ["Australia", "Borneo"];
        fronteiras["Borneo"] = ["NovaGuine", "Australia", "Vietna"];
        fronteiras["Sumatra"] = ["India", "Australia"];
	}
	
	this.carregaGruposTerritorio = function() {
	    var grupos = {};
	    
	    grupos["Asia"] = [
            coordenada_aral,
            coordenada_china,
            coordenada_india,
            coordenada_japao,
            coordenada_mongolia,
            coordenada_oriente_medio,
            coordenada_vietna,
            coordenada_vladivostok
        ];
	    grupos["AmericaDoNorte"] = [
            coordenada_alaska,
            coordenada_california,
            coordenada_groelandia,
            coordenada_labrador,
            coordenada_mackenzie,
            coordenada_mexico,
            coordenada_nova_york,
            coordenada_ottawa,
            coordenada_vancouver
        ];
	    grupos["Europa"] = [
            coordenada_alemanha,
            coordenada_inglaterra,
            coordenada_islandia,
            coordenada_moscou,
            coordenada_polonia,
            coordenada_portugal,
            coordenada_suecia
        ];
	    grupos["Africa"] = [
            coordenada_africa_do_sul,
            coordenada_argelia,
            coordenada_congo,
            coordenada_egito,
            coordenada_madagascar,
            coordenada_sudao
        ];
	    grupos["AmericaDoSul"] = [
            coordenada_argentina, 
            coordenada_brasil,
            coordenada_chile,
            coordenada_colombia
        ];
	    grupos["Oceania"] = [
            coordenada_australia,
            coordenada_borneo,
            coordenada_nova_guine,
            coordenada_sumatra
        ];
	    
	    return grupos;
	};
	
	this.iniciaGrupoTerritorio = function(paises, corDaBorda, corDoPreenchimento) {
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
            
            _poligonosTerritorios[pais.nome] = poligono_pais;
            
            google.maps.event.addListener(poligono_pais, 'click', function(event) {
                territorioClick(_labelTerritorios[pais.nome].posicaoJogador, pais.nome, 1);
            });
        });
    };
    
    this.inicia = function(territorioClick_) {
        this.iniciaMapaDasFronteiras();
        territorioClick = territorioClick_;
    
        // America do Norte.
        this.iniciaGrupoTerritorio([
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
        this.iniciaGrupoTerritorio([
            coordenada_africa_do_sul,
            coordenada_argelia,
            coordenada_congo,
            coordenada_egito,
            coordenada_madagascar,
            coordenada_sudao
        ], "#330033", "#FF99FF");
        
        // America do Sul.
        this.iniciaGrupoTerritorio([
            coordenada_argentina, 
            coordenada_brasil,
            coordenada_chile,
            coordenada_colombia
        ], "#003300", "#008000");
        
        // Oceania.
        this.iniciaGrupoTerritorio([
            coordenada_australia,
            coordenada_borneo,
            coordenada_nova_guine,
            coordenada_sumatra
        ], "#660000", "#FF6666");
        
        // Europa.
        this.iniciaGrupoTerritorio([
            coordenada_alemanha,
            coordenada_inglaterra,
            coordenada_islandia,
            coordenada_moscou,
            coordenada_polonia,
            coordenada_portugal,
            coordenada_suecia
        ], "#000099", "#66FFFF");
        
        // Asia
        this.iniciaGrupoTerritorio([
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
    
    this.manterFocoNoGrupo = function(grupoTerritorio) {
	    var grupos = this.carregaGruposTerritorio();
	    
	    $.each(["AmericaDoNorte", "AmericaDoSul", "Oceania", "Europa", "Asia", "Africa"],
	    function(i, nomeDoGrupo) {
	        if (nomeDoGrupo != grupoTerritorio) {
	            $.each(grupos[nomeDoGrupo], function(i, pais) {
	                _poligonosTerritorios[pais.nome].setOptions({fillOpacity: "0.5", fillColor: "#222", strokeColor: "#222"});
	            });
	        }
	    });
	};
	
	this.pintarGruposTerritorios = function() {
    	var grupos = this.carregaGruposTerritorio();
    	
	    $.each(grupos["Asia"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_ASIA, 
                strokeColor: COR_BORDA_ASIA});
        });
        
        $.each(grupos["AmericaDoNorte"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_AMERICA_DO_NORTE, 
                strokeColor: COR_BORDA_AMERICA_DO_NORTE});
        });
        
        $.each(grupos["Europa"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_EUROPA, 
                strokeColor: COR_BORDA_EUROPA});
        });
        
        $.each(grupos["Africa"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_AFRICA, 
                strokeColor: COR_BORDA_AFRICA});
        });
        
        $.each(grupos["AmericaDoSul"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_AMERICA_DO_SUL, 
                strokeColor: COR_BORDA_AMERICA_DO_SUL});
        });
        
        $.each(grupos["Oceania"], function(i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: "0.5", 
                fillColor: COR_PREENCHIMENTO_OCEANIA, 
                strokeColor: COR_BORDA_OCEANIA});
        });
	};
	
	this.escureceTodosOsTerritoriosExcetoDoJogador = function(posicaoJogador) {
	    var territorios = this.carregaTerritorios();
	    $.each(territorios, function(i, territorio) {
	        if (posicaoJogador != _labelTerritorios[territorio.nome].posicaoJogador) {
	            _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "0.5", fillColor: "#222", strokeColor: "#222"});
	        }
	    });
	};
	
	this.escureceTodosOsTerritoriosDoJogador = function(posicaoJogador) {
	    var territorios = this.carregaTerritorios();
	    $.each(territorios, function(i, territorio) {
	        if (posicaoJogador == _labelTerritorios[territorio.nome].posicaoJogador) {
	            _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "0.5", fillColor: "#222", strokeColor: "#222"});
	        }
	    });
	};
	
	this.focaNoTerritorioAlvoEAdjacentesDoJogador = function(nomeDoTerritorio, posicaoJogador) {
    	var me = this;
	    var territorios = this.carregaTerritorios();
	    $.each(territorios, function(i, territorio) {
	        if (territorio.nome == nomeDoTerritorio) {
	            _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "1"});
	        } else if (!me.temFronteira(nomeDoTerritorio, territorio.nome) || 
	                _labelTerritorios[territorio.nome].posicaoJogador != posicaoJogador ||
	                _labelTerritorios[territorio.nome].texto == '1') {
    	        _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "0.5", fillColor: "#222", strokeColor: "#222"});
    	    }
	    });
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
                    territorioClick(_labelTerritorios[territorio.codigo].posicaoJogador, territorio.codigo, 1);
                });
			}
		});
	};
	
	this.territorioNaoEhDoJogador = function(nomeDoTerritorio, posicaoJogador) {
	    return (_labelTerritorios[nomeDoTerritorio].posicaoJogador != posicaoJogador);
	};
	
	this.temFronteira = function(nomeDoTerritorio1, nomeDoTerritorio2) {
	    console.log(nomeDoTerritorio1);
	    console.log(nomeDoTerritorio2);
	    console.log(fronteiras[nomeDoTerritorio1]);
	    console.log(fronteiras[nomeDoTerritorio1].indexOf(nomeDoTerritorio2));
	    return fronteiras[nomeDoTerritorio1].indexOf(nomeDoTerritorio2) > -1;
	};
};
