var jogos = jogos || {};
jogos.war = jogos.war || {};

var _labelTerritorios = {};
var _markerTerritorios = {};
var _poligonosTerritorios = {};

var _piscarLoopFunc = {};

const TERR_COD_AFRICADOSUL = "AfricaDoSul";
const TERR_COD_BORNEO = "Borneo";
const TERR_COD_SUMATRA = "Sumatra";
const TERR_COD_NOVAGUINE = "NovaGuine";
const TERR_COD_JAPAO = "Japao";
const TERR_COD_MADAGASCAR = "Madagascar";
const TERR_COD_INGLATERRA = "Inglaterra";
const TERR_COD_ISLANDIA = "Islandia";

jogos.war.TerritoriosJS = function () {
    this.carrega = function () {
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
        territorios["Dudinka"] = coordenada_dudinka;
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
        territorios["Omsk"] = coordenada_omsk;
        territorios["OrienteMedio"] = coordenada_oriente_medio;
        territorios["Ottawa"] = coordenada_ottawa;
        territorios["Polonia"] = coordenada_polonia;
        territorios["Portugal"] = coordenada_portugal;
        territorios["Siberia"] = coordenada_siberia;
        territorios["Sudao"] = coordenada_sudao;
        territorios["Suecia"] = coordenada_suecia;
        territorios["Sumatra"] = coordenada_sumatra;
        territorios["Tchita"] = coordenada_tchita;
        territorios["Vancouver"] = coordenada_vancouver;
        territorios["Vietna"] = coordenada_vietna;
        territorios["Vladivostok"] = coordenada_vladivostok;

        return territorios;
    };
};

jogos.war.Territorios = function (mapa) {

    var MENOR_OPACIDADE = "0.5";

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

    territoriosJS = null;
    territorios = {};

    territorioClick = null;
    territorioMouseMove = null;
    territorioMouseOut = null;
    fronteiras = {};

    this.poligonosListener = [];

    this.iniciaFronteiras = function () {
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
        fronteiras["Polonia"] = ["Moscou", "Portugal", "OrienteMedio", "Egito", "Alemanha"];
        fronteiras["Alemanha"] = ["Portugal", "Polonia", "Inglaterra"];
        fronteiras["Portugal"] = ["Alemanha", "Inglaterra", "Polonia", "Argelia", "Egito"];

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
        fronteiras["Tchita"] = ["Siberia", "Dudinka", "Mongolia", "Vladivostok", "China"];
        fronteiras["Siberia"] = ["Dudinka", "Tchita", "Vladivostok"];
        fronteiras["Vladivostok"] = ["Siberia", "Tchita", "China", "Japao", "Alaska"];

        fronteiras["Australia"] = ["NovaGuine", "Sumatra", "Borneo"];
        fronteiras["NovaGuine"] = ["Australia", "Borneo"];
        fronteiras["Borneo"] = ["NovaGuine", "Australia", "Vietna"];
        fronteiras["Sumatra"] = ["India", "Australia"];
    };

    this.iniciaPontesEntreTerritorios = function () {
        var coords = [
            [new google.maps.LatLng(19.311143, 85.781250), new google.maps.LatLng(5.965754, 95.273438)],
            [new google.maps.LatLng(10.833306, 108.984375), new google.maps.LatLng(4.039618, 113.730469)],
            [new google.maps.LatLng(-7.013668, 106.699219), new google.maps.LatLng(-20.138470, 119.707031)],
            [new google.maps.LatLng(-1.581830, 116.718750), new google.maps.LatLng(-14.604847, 125.859375)],
            [new google.maps.LatLng(-1.581830, 116.718750), new google.maps.LatLng(-3.688855, 133.417969)],
            [new google.maps.LatLng(-5.266008, 137.636719), new google.maps.LatLng(-12.039321, 134.648438)],
            [new google.maps.LatLng(-5.266008, -34.980469), new google.maps.LatLng(10.141932, -14.414063)],
            [new google.maps.LatLng(-12.039321, 49.042969), new google.maps.LatLng(1.230374, 45.351563)],
            [new google.maps.LatLng(-25.799891, 44.121094), new google.maps.LatLng(-28.613459, 33.046875)],
            [new google.maps.LatLng(53.540307, 160.488281), new google.maps.LatLng(53.540307, -152.226563), new google.maps.LatLng(59.977005, -143.964844)],
            [new google.maps.LatLng(68.528235, -81.914063), new google.maps.LatLng(71.746432, -55.195313)], // Mackenzie <-> Groelandia
            [new google.maps.LatLng(56.072035, -60.820313), new google.maps.LatLng(62.431074, -50.449219)],
            [new google.maps.LatLng(68.656555, -25.488281), new google.maps.LatLng(66.018018, -19.511719)],
            [new google.maps.LatLng(63.782486, -15.996094), new google.maps.LatLng(58.263287, -6.679688)],
            [new google.maps.LatLng(55.178868, -1.230469), new google.maps.LatLng(59.355596, 5.449219)],
            [new google.maps.LatLng(55.178868, -1.230469), new google.maps.LatLng(53.540307, 6.152344)],
            [new google.maps.LatLng(37.160317, 23.906250), new google.maps.LatLng(31.503629, 25.488281)],
            [new google.maps.LatLng(38.685510, 17.226563), new google.maps.LatLng(31.353637, 19.511719)],
            [new google.maps.LatLng(42.811522, 4.042969), new google.maps.LatLng(37.020098, 5.800781)],
            [new google.maps.LatLng(40.313043, 141.855469), new google.maps.LatLng(59.085739, 148.359375)],
            [new google.maps.LatLng(33.431441, 133.066406), new google.maps.LatLng(28.613459, 121.992188)],
            [new google.maps.LatLng(14.349548, -89.296875), new google.maps.LatLng(7.710992, -77.167969)] // Mexico <-> Colombia
        ];

        var lineSymbol = {
            path: 'M 0,-1 0,1',
            strokeOpacity: 1,
            scale: 4
        };

        $.each(coords, function (i, coord) {
            new google.maps.Polyline({
                path: coord,
                strokeColor: "#282423", strokeOpacity: 1, strokeWeight: 1,
                icons: [{
                    icon: lineSymbol,
                    offset: '0',
                    repeat: '18px'
                }],
                map: mapa
            });
        });
    };

    this.carregaGruposTerritorio = function () {
        var grupos = {};

        grupos["Asia"] = [
            coordenada_aral,
            coordenada_china,
            coordenada_dudinka,
            coordenada_india,
            coordenada_japao,
            coordenada_mongolia,
            coordenada_omsk,
            coordenada_oriente_medio,
            coordenada_siberia,
            coordenada_tchita,
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

    this.iniciaGrupoTerritorio = function (paises, corDaBorda, corDoPreenchimento) {
        $.each(paises, function (i, pais) {
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

            google.maps.event.addListener(poligono_pais, 'mousemove', function (event) {
                territorioMouseMove(event, _labelTerritorios[pais.nome].posicaoJogador, pais.nome);
            });
            google.maps.event.addListener(poligono_pais, 'mouseout', function () {
                territorioMouseOut(_labelTerritorios[pais.nome].posicaoJogador, pais.nome);
            });
            google.maps.event.addListener(poligono_pais, 'click', function (event) {
                clearTimeout(this.doNotTriggerTwiceTimeout);
                this.doNotTriggerTwiceTimeout = setTimeout(function(){
                    territorioClick(_labelTerritorios[pais.nome].posicaoJogador, pais.nome);
                }, 300);
            });
        });
    };

    this.iniciaRegioes = function () {
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
        ], COR_BORDA_AMERICA_DO_NORTE, COR_PREENCHIMENTO_AMERICA_DO_NORTE);

        // Africa.
        this.iniciaGrupoTerritorio([
            coordenada_africa_do_sul,
            coordenada_argelia,
            coordenada_congo,
            coordenada_egito,
            coordenada_madagascar,
            coordenada_sudao
        ], COR_BORDA_AFRICA, COR_PREENCHIMENTO_AFRICA);

        // America do Sul.
        this.iniciaGrupoTerritorio([
            coordenada_argentina,
            coordenada_brasil,
            coordenada_chile,
            coordenada_colombia
        ], COR_BORDA_AMERICA_DO_SUL, COR_PREENCHIMENTO_AMERICA_DO_SUL);

        // Oceania.
        this.iniciaGrupoTerritorio([
            coordenada_australia,
            coordenada_borneo,
            coordenada_nova_guine,
            coordenada_sumatra
        ], COR_BORDA_OCEANIA, COR_PREENCHIMENTO_OCEANIA);

        // Europa.
        this.iniciaGrupoTerritorio([
            coordenada_alemanha,
            coordenada_inglaterra,
            coordenada_islandia,
            coordenada_moscou,
            coordenada_polonia,
            coordenada_portugal,
            coordenada_suecia
        ], COR_BORDA_EUROPA, COR_PREENCHIMENTO_EUROPA);

        // Asia
        this.iniciaGrupoTerritorio([
            coordenada_aral,
            coordenada_china,
            coordenada_dudinka,
            coordenada_india,
            coordenada_japao,
            coordenada_mongolia,
            coordenada_omsk,
            coordenada_oriente_medio,
            coordenada_siberia,
            coordenada_tchita,
            coordenada_vietna,
            coordenada_vladivostok
        ], COR_BORDA_ASIA, COR_PREENCHIMENTO_ASIA);
    };

    this.inicia = function (territorioClick_, territorioMouseMove_, territorioMouseOut_) {
        this.territoriosJS = new jogos.war.TerritoriosJS();
        this.territorios = this.territoriosJS.carrega();

        this.iniciaFronteiras();
        territorioMouseMove = territorioMouseMove_;
        territorioMouseOut = territorioMouseOut_;
        territorioClick = territorioClick_;

        this.iniciaPontesEntreTerritorios();

        this.iniciaRegioes();
    };

    this.manterFocoNoGrupo = function (grupoTerritorio) {
        var grupos = this.carregaGruposTerritorio();
        var me = this;

        $.each(["AmericaDoNorte", "AmericaDoSul", "Oceania", "Europa", "Asia", "Africa"],
            function (i, nomeDoGrupo) {
                if (nomeDoGrupo != grupoTerritorio) {
                    $.each(grupos[nomeDoGrupo], function (i, pais) {
                        me.escureceTerritorio(pais.nome);
                    });
                }
            });
    };

    this.pintarGruposTerritorios = function () {
        var grupos = this.carregaGruposTerritorio();

        if (Object.keys(_poligonosTerritorios).length == 0)
            this.iniciaRegioes();

        const opacity = 0.8;

        $.each(grupos["Asia"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_ASIA,
                strokeColor: COR_BORDA_ASIA
            });
        });

        $.each(grupos["AmericaDoNorte"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_AMERICA_DO_NORTE,
                strokeColor: COR_BORDA_AMERICA_DO_NORTE
            });
        });

        $.each(grupos["Europa"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_EUROPA,
                strokeColor: COR_BORDA_EUROPA
            });
        });

        $.each(grupos["Africa"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_AFRICA,
                strokeColor: COR_BORDA_AFRICA
            });
        });

        $.each(grupos["AmericaDoSul"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_AMERICA_DO_SUL,
                strokeColor: COR_BORDA_AMERICA_DO_SUL
            });
        });

        $.each(grupos["Oceania"], function (i, pais) {
            _poligonosTerritorios[pais.nome].setOptions({
                fillOpacity: opacity,
                fillColor: COR_PREENCHIMENTO_OCEANIA,
                strokeColor: COR_BORDA_OCEANIA
            });
        });
    };

    this.escureceTerritorio = function (codigoTerritorio) {
        var corDeFundo = _poligonosTerritorios[codigoTerritorio].fillColor;
        var libCor = new jogos.Cor();

        corDeFundo = corDeFundo.replace("#", "");
        var rgb = parseInt(corDeFundo, 16);
        var red = (rgb >> 16) & 0xFF;
        var green = (rgb >> 8) & 0xFF;
        var blue = rgb & 0xFF;

        var inc = parseInt("66", 16);

        red = libCor.subtrai(red, inc);
        green = libCor.subtrai(green, inc);
        blue = libCor.subtrai(blue, inc);

        var novaCor = libCor.rgbParaHex(red, green, blue);
        _poligonosTerritorios[codigoTerritorio].setOptions({fillOpacity: MENOR_OPACIDADE, fillColor: novaCor});
    };

    this.escureceTodosOsTerritoriosExcetoDoJogador = function (posicaoJogador) {
        var me = this;
        $.each(this.territorios, function (i, territorio) {
            if (posicaoJogador != _labelTerritorios[territorio.nome].posicaoJogador) {
                me.escureceTerritorio(territorio.nome);
            }
        });
    };

    this.escureceTodosOsTerritoriosDoJogador = function (posicaoJogador) {
        var me = this;
        $.each(this.territorios, function (i, territorio) {
            if (posicaoJogador == _labelTerritorios[territorio.nome].posicaoJogador) {
                me.escureceTerritorio(territorio.nome);
            }
        });
    };

    this.aumentaBrilhoTerritorio = function (nomeDoTerritorio) {
        _poligonosTerritorios[nomeDoTerritorio].setOptions({fillOpacity: "1"});
    };

    this.diminuiBrilhoTerritorio = function (nomeDoTerritorio) {
        _poligonosTerritorios[nomeDoTerritorio].setOptions({fillOpacity: "0.5"});
    };

    this.focaNoTerritorioAlvoEAdjacentesDoJogador = function (nomeDoTerritorio, posicaoJogador) {
        var me = this;
        $.each(this.territorios, function (i, territorio) {
            if (territorio.nome == nomeDoTerritorio) {
                _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "1"});
            } else if (!me.temFronteira(nomeDoTerritorio, territorio.nome) ||
                _labelTerritorios[territorio.nome].posicaoJogador != posicaoJogador) {
                me.escureceTerritorio(territorio.nome);
            }
        });
    };

    this.focaNosTerritorios = function (territoriosParaFoco) {
        var me = this;
        $.each(this.territorios, function (i, territorio) {
            if (territoriosParaFoco.indexOf(territorio.nome) == -1) {
                me.escureceTerritorio(territorio.nome);
            } else {
                _poligonosTerritorios[territorio.nome].setOptions({fillOpacity: "1"});
            }
        });
    };

    this.corDeFundoDaPosicao = function (posicao) {
        var corDeFundo = '#555';
        switch (posicao) {
            case 0: // Vermelho
                corDeFundo = '#841D0F';
                break;
            case 1: // Azul
                corDeFundo = '#2621A8';
                break;
            case 2: // Verde
                corDeFundo = '#436C4B';
                break;
            case 3:
                corDeFundo = '#1A191E';
                break;
            case 4:
                corDeFundo = '#bdbdbd';
                break;
            case 5:
                corDeFundo = '#ffd861';
                break;
        }

        return corDeFundo;
    };

    this.iniciaLabelDosTerritorios = function (territorios, posicaoJogador) {
        this.atualizaTerritorios(territorios, posicaoJogador);
    };

    this.territorioNaoEhDoJogador = function (codigoTerritorio, posicaoJogador) {
        return (_labelTerritorios[codigoTerritorio].posicaoJogador != posicaoJogador);
    };

    this.temFronteira = function (nomeDoTerritorio1, nomeDoTerritorio2) {
        return fronteiras[nomeDoTerritorio1].indexOf(nomeDoTerritorio2) > -1;
    };

    this.quantidadeDeTropaDoTerritorio = function (nomeDoTerritorio) {
        return Number(_labelTerritorios[nomeDoTerritorio].texto);
    };

    this.alteraDonoTerritorio = function (codigoTerritorio, posicaoJogador) {
        var corDeFundo = this.corDeFundoDaPosicao(posicaoJogador);

        var novoCirculo = {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: corDeFundo,
            fillOpacity: 0.75,
            scale: 16,
            strokeColor: "#282423",
            strokeWeight: 2
        };
        _markerTerritorios[codigoTerritorio].setOptions({icon: novoCirculo});
        _labelTerritorios[codigoTerritorio].alteraPosicaoJogador(posicaoJogador);
    };

    this.barreiraDosTerritorios = function (territorios) {
        var bounds = new google.maps.LatLngBounds();
        $.each(territorios, function (i, codigoTerritorio) {
            bounds.extend(_markerTerritorios[codigoTerritorio].position);
        });
        return bounds;
    };

    this.atualizaTerritorios = function (territorios, posicaoJogador) {
        var corDeFundo = this.corDeFundoDaPosicao(posicaoJogador);

        var circulo = {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: corDeFundo,
            fillOpacity: 0.75,
            scale: 16,
            strokeColor: "#282423",
            strokeWeight: 2
        };

        var me = this;
        $.each(territorios, function (i, territorio) {
            if (me.territorios[territorio.codigo]) {
                var posicao = me.territorios[territorio.codigo].centro;

                var marker = null;
                if (_markerTerritorios[territorio.codigo]) {
                    marker = _markerTerritorios[territorio.codigo];
                    marker.position = posicao;
                    marker.icon = circulo;
                } else {
                    marker = new google.maps.Marker({
                        position: posicao,
                        map: mapa,
                        icon: circulo,
                        title: territorio.nome,
                        clickable: true,
                        zIndex: 2
                    });

                    google.maps.event.addListener(marker, 'mousemove', function (event) {
                        territorioMouseMove(event, _labelTerritorios[territorio.codigo].posicaoJogador, territorio.codigo);
                    });

                    google.maps.event.addListener(marker, 'mouseout', function () {
                        territorioMouseOut(_labelTerritorios[territorio.codigo].posicaoJogador, territorio.codigo);
                    });

                    google.maps.event.addListener(marker, 'click', function (event) {
                        clearTimeout(this.doNotTriggerTwiceTimeout);
                        this.doNotTriggerTwiceTimeout = setTimeout(function() {
                            territorioClick(_labelTerritorios[territorio.codigo].posicaoJogador, territorio.codigo);
                        }, 300);
                    });
                }

                var label = null;
                if (_labelTerritorios[territorio.codigo]) {
                    label = _labelTerritorios[territorio.codigo];
                } else {
                    label = new Label({
                        map: mapa
                    }, true);

                    label.bindTo('position', marker, 'position');
                    label.bindTo('text', marker, 'position');
                }

                label.texto = territorio.quantidadeDeTropas;
                label.alteraQuantiadeDeTropas(territorio.quantidadeDeTropas);
                label.alteraPosicaoJogador(posicaoJogador);

                _markerTerritorios[territorio.codigo] = marker;
                _labelTerritorios[territorio.codigo] = label;
            }
        });
    };

    this.piscar = function (codigoTerritorio) {
        utilTerritorio_polygonFadein(codigoTerritorio, _poligonosTerritorios[codigoTerritorio],
            500,
            function () {
                utilTerritorio_polygonFadeout(codigoTerritorio, _poligonosTerritorios[codigoTerritorio], 500)
            });
    };

    this.limpa = function () {
        $.each(_labelTerritorios, function (i, label) {
            label.alteraQuantiadeDeTropas(0);
            label.setMap(null);
        });
        _labelTerritorios = {};

        $.each(_markerTerritorios, function (i, marker) {
            marker.setMap(null);
        });
        _markerTerritorios = {};

        $.each(_poligonosTerritorios, function (i, poligono) {
            poligono.setMap(null);
        });
        _poligonosTerritorios = {};
    };

    this.posicaoHTML = function (nomeDoTerritorio) {
        return _labelTerritorios[nomeDoTerritorio].posicaoHTML();
    };
};

var _nomeDosTerritoriosPeloCodigo = {};
_nomeDosTerritoriosPeloCodigo["AfricaDoSul"] = "África do Sul";
_nomeDosTerritoriosPeloCodigo["Alaska"] = "Alaska";
_nomeDosTerritoriosPeloCodigo["Alemanha"] = "Alemanha";
_nomeDosTerritoriosPeloCodigo["Aral"] = "Aral";
_nomeDosTerritoriosPeloCodigo["Argelia"] = "Argélia";
_nomeDosTerritoriosPeloCodigo["Argentina"] = "Argentina";
_nomeDosTerritoriosPeloCodigo["Australia"] = "Austrália";
_nomeDosTerritoriosPeloCodigo["Borneo"] = "Bórneo";
_nomeDosTerritoriosPeloCodigo["Brasil"] = "Brasil";
_nomeDosTerritoriosPeloCodigo["California"] = "California";
_nomeDosTerritoriosPeloCodigo["Chile"] = "Chile";
_nomeDosTerritoriosPeloCodigo["China"] = "China";
_nomeDosTerritoriosPeloCodigo["Colombia"] = "Colômbia";
_nomeDosTerritoriosPeloCodigo["Congo"] = "Congo";
_nomeDosTerritoriosPeloCodigo["Dudinka"] = "Dudinka";
_nomeDosTerritoriosPeloCodigo["Egito"] = "Egito";
_nomeDosTerritoriosPeloCodigo["Groelandia"] = "Groelândia";
_nomeDosTerritoriosPeloCodigo["India"] = "Índia";
_nomeDosTerritoriosPeloCodigo["Inglaterra"] = "Inglaterra";
_nomeDosTerritoriosPeloCodigo["Islandia"] = "Islândia";
_nomeDosTerritoriosPeloCodigo["Japao"] = "Japão";
_nomeDosTerritoriosPeloCodigo["Labrador"] = "Labrador";
_nomeDosTerritoriosPeloCodigo["Madagascar"] = "Madagascar";
_nomeDosTerritoriosPeloCodigo["Mackenzie"] = "Mackenzie";
_nomeDosTerritoriosPeloCodigo["Mexico"] = "México";
_nomeDosTerritoriosPeloCodigo["Mongolia"] = "Mongólia";
_nomeDosTerritoriosPeloCodigo["Moscou"] = "Moscou";
_nomeDosTerritoriosPeloCodigo["NovaGuine"] = "Nova Guiné";
_nomeDosTerritoriosPeloCodigo["NovaYork"] = "Nova York";
_nomeDosTerritoriosPeloCodigo["Omsk"] = "Omsk";
_nomeDosTerritoriosPeloCodigo["OrienteMedio"] = "Oriente Médio";
_nomeDosTerritoriosPeloCodigo["Ottawa"] = "Ottawa";
_nomeDosTerritoriosPeloCodigo["Polonia"] = "Polônia";
_nomeDosTerritoriosPeloCodigo["Portugal"] = "Portugal";
_nomeDosTerritoriosPeloCodigo["Siberia"] = "Sibéria";
_nomeDosTerritoriosPeloCodigo["Sudao"] = "Sudão";
_nomeDosTerritoriosPeloCodigo["Suecia"] = "Suécia";
_nomeDosTerritoriosPeloCodigo["Sumatra"] = "Sumatra";
_nomeDosTerritoriosPeloCodigo["Tchita"] = "Tchita";
_nomeDosTerritoriosPeloCodigo["Vancouver"] = "Vancouver";
_nomeDosTerritoriosPeloCodigo["Vietna"] = "Vietnã";
_nomeDosTerritoriosPeloCodigo["Vladivostok"] = "Vladivostok";
