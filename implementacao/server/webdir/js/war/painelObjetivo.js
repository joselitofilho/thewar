var gpscheck = gpscheck || {};
gpscheck.war = gpscheck.war || {};

gpscheck.war.PainelObjetivo = function(cartaObjetivo) {
    this.cartaObjetivo = cartaObjetivo;

    this.abre = function() {
        this.abreEspecifico(this.cartaObjetivo, "Carta objetivo");
    };

    this.fecha = function() {
        $('#painel_objetivo').css('visibility', 'hidden');
        $('#po_fundo').css('visibility', 'hidden');
    };

    this.abreEspecifico = function(cartaObjetivo, titulo) {
        $('#cartaObjetivo').attr('class', 'carta_objetivo carta_objetivo_' + cartaObjetivo);
        $('#po_titulo').html(titulo);
        $('#painel_objetivo').css('visibility', 'visible');
        $('#po_fundo').css('visibility', 'visible');
    };
};
