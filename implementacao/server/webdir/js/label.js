/** 
 * Define a camada derivada de google.maps.OverlayView
 */
function Label(opt_options) {
    // Inicializacao
    this.setValues(opt_options);
    
    this.texto = '1';
    this.corTexto = '#FFF';
    this.posicaoJogador = -1;
    this.infoTropasPerdidas = '0';

    // Label contendo a quantidade de tropas...
    var span = this.span_ = document.createElement('span');
    span.setAttribute('class', 'label_tropas');
    span.style.color = this.corTexto;

    var spanInfoTropasPerdidas = this.spanInfoTropasPerdidas_ = document.createElement('span');
    spanInfoTropasPerdidas.setAttribute('class', 'label_info_tropas_perdidas');

    var div = this.div_ = document.createElement('div');
    div.appendChild(span);
    div.appendChild(spanInfoTropasPerdidas);
    div.style.cssText = 'position: absolute; display: none';
};
Label.prototype = new google.maps.OverlayView;

Label.prototype.onAdd = function() {
    var pane = this.getPanes().floatPane;
    pane.appendChild(this.div_);

    // Repinta o label se houver alteração na posição do label ou do texto.
    var me = this;
    this.listeners_ = [
    google.maps.event.addListener(this, 'position_changed',
        function() { me.draw(); }),
    google.maps.event.addListener(this, 'text_changed',
        function() { me.draw(); })
    ];
};

Label.prototype.onRemove = function() {
    this.div_.parentNode.removeChild(this.div_);

    // Label é removido do mapa e para de atualizar a posição/texto.
    for (var i = 0, I = this.listeners_.length; i < I; ++i) {
        google.maps.event.removeListener(this.listeners_[i]);
    }
};

Label.prototype.draw = function() {
    var projection = this.getProjection();
    var position = projection.fromLatLngToDivPixel(this.get('position'));

    if (position != null) {
        var div = this.div_;
        div.style.left = position.x + 'px';
        div.style.top = position.y + 'px';
        div.style.display = 'block';
        this.span_.innerHTML = this.texto;
        this.spanInfoTropasPerdidas_.innerHTML = this.infoTropasPerdidas;
        $(this.spanInfoTropasPerdidas_).css("opacity", "0.0");
    }
};

Label.prototype.alteraQuantiadeDeTropas = function(qtd) {
    this.texto = qtd;
    this.span_.innerHTML = this.texto;
};

Label.prototype.alteraPosicaoJogador = function(posicaoJogador) {
    this.posicaoJogador = posicaoJogador;
    if (posicaoJogador == 4) {
        this.corTexto = '#000';
    } else {
        this.corTexto = '#FFF';
    }
    this.span_.style.color = this.corTexto;
};

Label.prototype.perdeuTropas = function(quantidade) {
    if (quantidade > 0) {
        this.spanInfoTropasPerdidas_.innerHTML = '-' + quantidade;
        this.spanInfoTropasPerdidas_.style.opacity = 1.0;
        this.spanInfoTropasPerdidas_.style.top = 0;
        $(this.spanInfoTropasPerdidas_)
            .animate({
                opacity: 0.0,
                "top": "-=50px"
            }, 2000, function() {/*Animacao complete.*/});
    }
};
