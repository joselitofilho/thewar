var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Slider = function(divSlider) {
    var min;
    var max;
    var itemEsq;
    var itemAtivo;
    var itemDir;
    var indiceAtivo;
    var fila;
            
    this.inicia = function(min, max) {
        this.min = min;
        this.max = max;
        this.itemEsq = $('#smt_itemEsquerda');
        this.itemAtivo = $('#smt_itemAtivo');
        this.itemDir = $('#smt_itemDireita');
        
        this.criaFila();
        this.preencheItens();
        this.maximo();
        
        divSlider.css('visibility', 'visible');
    };
            
    this.criaFila = function() {
        this.fila = [];
        for (i=this.min; i<=this.max; i++) {
            this.fila.push(i);
        }
    };
            
    this.preencheItens = function() {
        var esq = 
            (this.indiceAtivo-1 < 0)
                ? this.fila[this.fila.length-1]
                : this.fila[this.indiceAtivo-1];
        var dir = 
            (this.indiceAtivo+1 == this.fila.length)
                ? this.fila[0]
                : this.fila[this.indiceAtivo+1];
        
        this.itemEsq.text(esq);
        this.itemAtivo.text(this.fila[this.indiceAtivo]);
        this.itemDir.text(dir);
    };
            
    this.esquerda = function() {
        --this.indiceAtivo;
        if (this.indiceAtivo < 0) this.indiceAtivo = this.fila.length-1
        this.preencheItens();
    };
            
    this.direita = function() {
        ++this.indiceAtivo;
        if (this.indiceAtivo == this.fila.length) this.indiceAtivo = 0;
        this.preencheItens();
    };
    
    this.minimo = function() {
        this.indiceAtivo = 0;
        this.preencheItens();
    };
    
    this.maximo = function() {
        this.indiceAtivo = this.fila.length-1;
        this.preencheItens();
    };
    
    this.quantidade = function() {
        return this.fila[this.indiceAtivo];
    };
    
    this.fechar = function() {
        divSlider.css('visibility', 'hidden');
    };
    
    this.alteraPosicionamentoNoHTML = function(posicao) {
        divSlider.offset({ top: posicao.top, left: posicao.left });
    };
};
