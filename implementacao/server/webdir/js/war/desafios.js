var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Desafios = function () {
    this.toogle = function () {
        if ($('#desafios_painel').css('visibility') === 'visible') {
            $('#desafios_painel').css('visibility', 'hidden');
        } else {
            $('#desafios_painel').css('visibility', 'visible');
        }
    };

    this.preencheElementoHtml = function (desafios) {
        // #desafio_carta_esq, #desafio_carta_centro, #desafio_carta_dir

        // .desafio_info: <p>Somente doador</p>
        // .desafio_info: <p>Realizado</p><i class="material-icons">done_outline</i>
        // .desafio_info.visibility: hidden, visible

        // .desafio_carta_conteudo .desafio_orientador
        // .desafio_carta_conteudo .desafio_xp
        // .desafio_carta_conteudo .desafio_descricao
    };
};
