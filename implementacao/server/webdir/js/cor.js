var jogos = jogos || {};

jogos.Cor = function() {
    this.componenteParaHex = function(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    };

    this.rgbParaHex = function(r, g, b) {
        return "#" + 
            this.componenteParaHex(r) + 
            this.componenteParaHex(g) + 
            this.componenteParaHex(b);
    };
    
    this.adiciona = function(value, inc) {
        value += inc;
        if (value > 255) value = 255;
        return value;
    };
    
    this.subtrai = function(value, inc) {
        value -= inc;
        if (value < 0) value = 0;
        return value;
    };
};
