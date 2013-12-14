var gpscheck = gpscheck || {};
gpscheck.mapa = gpscheck.mapa || {};

gpscheck.mapa.Mapa = function() {

    _mapaGoogle = null;

    this.inicia = function(mapaDiv, lat, lng) {
        var mapOptions = {
            center: new google.maps.LatLng(lat, lng),
            zoom: 2,
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
