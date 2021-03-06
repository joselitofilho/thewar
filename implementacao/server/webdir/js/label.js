/**
 * Define a camada derivada de google.maps.OverlayView
 */
function Label(opt_options, labelOverlayClick) {
    // Inicializacao
    this.setValues(opt_options);

    this.labelOverlayClick = labelOverlayClick;

    this.texto = '1';
    this.corTexto = '#F8F7E9';
    this.posicaoJogador = -1;

    // Label contendo a quantidade de tropas...
    var span = this.span_ = document.createElement('span');
    span.setAttribute('class', 'label_tropas unselectable');
    span.style.color = this.corTexto;

    var spanInfoTropasPerdidas = this.spanInfoTropasPerdidas_ = document.createElement('span');
    spanInfoTropasPerdidas.setAttribute('class', 'label_info_tropas_perdidas unselectable');

    var divExplosao = this.divExplosao_ = document.createElement('div');
    divExplosao.setAttribute('class', 'label_div_explosao unselectable');
    $(this.divExplosao_).css("background", "url('../imagens/explosao_50px_sprite.png') no-repeat");
    $(this.divExplosao_).css('display', 'none');

    var div = this.div_ = document.createElement('div');
    div.appendChild(span);
    div.appendChild(spanInfoTropasPerdidas);
    div.appendChild(divExplosao);
    div.style.cssText = 'position: absolute; display: none';
}

Label.prototype = new google.maps.OverlayView;

Label.prototype.onAdd = function () {
    var pane = this.getPanes().floatPane;
    pane.appendChild(this.div_);

    // Repinta o label se houver alteração na posição do label ou do texto.
    var me = this;
    this.listeners_ = [
        google.maps.event.addListener(this, 'position_changed',
            function () {
                me.draw();
            }),
        google.maps.event.addListener(this, 'text_changed',
            function () {
                me.draw();
            })
    ];

    if (this.labelOverlayClick) {
        this.getPanes().overlayMouseTarget.appendChild(this.div_);
        google.maps.event.addDomListener(this.div_, 'click', function () {
            google.maps.event.trigger(me, 'click');
        });
    }
};

Label.prototype.onRemove = function () {
    this.div_.parentNode.removeChild(this.div_);

    // Label é removido do mapa e para de atualizar a posição/texto.
    for (var i = 0, I = this.listeners_.length; i < I; ++i) {
        google.maps.event.removeListener(this.listeners_[i]);
    }
};

Label.prototype.draw = function () {
    var projection = this.getProjection();
    var position = projection.fromLatLngToDivPixel(this.get('position'));

    if (position != null) {
        var div = this.div_;
        div.style.left = position.x + 'px';
        div.style.top = position.y + 'px';
        div.style.display = 'inline-block'; // 'block';
        this.span_.innerHTML = this.texto;
    }
};

Label.prototype.alteraQuantiadeDeTropas = function (qtd) {
    this.texto = qtd;
    this.span_.innerHTML = '';
    this.span_.innerHTML = this.texto;
};

Label.prototype.alteraPosicaoJogador = function (posicaoJogador) {
    this.posicaoJogador = posicaoJogador;
    if (posicaoJogador === 4 || posicaoJogador === 5) {
        this.corTexto = '#282423';
    } else {
        this.corTexto = '#F8F7E9';
    }
    this.span_.style.color = this.corTexto;
};

Label.prototype.perdeuTropas = function (quantidade) {
    if (quantidade > 0) {
        $(this.spanInfoTropasPerdidas_).css("background-position", ((quantidade - 1) * -20) + "px 0px");

        this.spanInfoTropasPerdidas_.style.opacity = 1.0;
        this.spanInfoTropasPerdidas_.style.top = 0;
        $(this.spanInfoTropasPerdidas_)
            .animate({
                    "top": "-=50px"
                },
                1000,
                function () {
                    $(this).animate({
                        opacity: 0.0,
                    }), 500
                }
            );
    }
};

Label.prototype.explosao = function () {
    $(this.divExplosao_).css('display', '');
    $(".label_div_explosao").css("background-position", "0px 0px");
    var i = 0;
    var explosaoLoop = setInterval(function () {
        $(".label_div_explosao").css("background-position", (i * -50) + "px 0px");
        ++i;
    }, 100);
    setTimeout(function () {
        $(".label_div_explosao").css('display', 'none');
        clearInterval(explosaoLoop);
    }, 2700);
};

Label.prototype.posicaoHTML = function () {
    // TODO: Talvez um algoritmo melhor...
    var offset = $(this.span_).offset();
    offset.top -= 32;
    offset.left += 32;
    return offset;
};
