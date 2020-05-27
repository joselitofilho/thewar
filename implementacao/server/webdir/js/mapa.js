var jogowar = gpscheck || {};
jogowar.mapa = gpscheck.mapa || {};

jogowar.mapa.Mapa = function () {

    _mapaGoogle = null;

    this.inicia = function (mapaDiv, lat, lng, zoom) {
        var mapOptions = {
            center: new google.maps.LatLng(lat, lng),
            zoom: zoom,
            zoomControl: false,
            mapTypeId: google.maps.MapTypeId.SATELLITE,
            disableDoubleClickZoom: true,
            keyboardShortcuts: false,
            draggable: false,
            panControl: false,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            scrollwheel: false,
            overviewMapControl: false,
        };

        _mapaGoogle = new google.maps.Map(mapaDiv, mapOptions);
        mapaDiv.style.backgroundColor = "transparent";
    };

    this.alteraEstilo = function (estilo) {
        if (_mapaGoogle) {
            var styledMap = new google.maps.StyledMapType(estilo, {name: "GuerraMap"});
            _mapaGoogle.mapTypes.set('guerra_map_style', styledMap);
            _mapaGoogle.setMapTypeId('guerra_map_style');
            $("#mapa.gm-style").parent().css({"background-color": "rgba(0,0,0,0)"});
        }
    };
};
