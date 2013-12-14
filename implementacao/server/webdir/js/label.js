// Define the overlay, derived from google.maps.OverlayView
function Label(opt_options, corTexto) {
    // Initialization
    this.setValues(opt_options);
    
    this.texto = '1';
    this.corTexto = corTexto;
    this.posicaoJogador = -1;

    // Label specific
    var span = this.span_ = document.createElement('span');
    span.setAttribute('class', 'label_tropas');
    span.style.color = this.corTexto;

    var div = this.div_ = document.createElement('div');
    div.appendChild(span);
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
    }
};

Label.prototype.alteraQuantiadeDeTropas = function(qtd) {
    this.texto = qtd;
    //this.draw();
    this.span_.innerHTML = this.texto;  
};
