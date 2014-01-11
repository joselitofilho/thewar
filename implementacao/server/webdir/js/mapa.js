var jogowar = gpscheck || {};
jogowar.mapa = gpscheck.mapa || {};

jogowar.mapa.Mapa = function() {

    _mapaGoogle = null;

    this.inicia = function(mapaDiv, lat, lng, zoom) {
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
            overviewMapControl: false
        };

        _mapaGoogle = new google.maps.Map(mapaDiv, mapOptions);
    };
};
