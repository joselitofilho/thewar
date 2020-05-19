var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.PainelVitoria = function () {
    _nomeVencedor = "";
    _objetivoVencedor = -1;

    this.abre = function (vencedor, pontos, objetivo) {
        $('#painel_vitoria').css('visibility', 'visible');
        $('#pv_fundo').css('visibility', 'visible');
        $('#pv_vencedor').html(vencedor);
        $('#pv_pontos').html('+' + pontos);
        _nomeVencedor = vencedor;
        _objetivoVencedor = Number(objetivo) + 1;
    };

    this.abreObjetivoDoVencedor = function () {
        _painelObjetivo.abreEspecifico(_objetivoVencedor, _nomeVencedor + ' venceu o jogo!');
    };

    this.fecha = function () {
        jogo_sair();
        $('#painel_vitoria').css('visibility', 'hidden');
        $('#pv_fundo').css('visibility', 'hidden');
        $('#pv_vencedor').html('');
        $('#pv_pontos').html('');
        _nomeVencedor = "";
        _objetivoVencedor = -1;
    };
};
