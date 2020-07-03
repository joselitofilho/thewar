var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Desafios = function () {

    this.processaMsg = function (params) {
        this.preencheElementoHtml(params);
    };

    this.toogle = function () {
        if ($('#desafios_painel').css('visibility') === 'visible') {
            $('#desafios_painel').css('visibility', 'hidden');
        } else {
            $('#desafios_painel').css('visibility', 'visible');
        }
    };

    this.atualiza = function () {
        msg = comunicacao_desafiosEmAndamento();
        _libwebsocket.enviarObjJson(msg);
    };

    this.preencheElementoHtml = function (desafios) {
        if (desafios.length === 0) {
            const htmlEmBreve = '<p>Em breve</p>';
            $('#desafio_carta_centro .desafio_info').html(htmlEmBreve);
            $('#desafio_carta_centro .desafio_info').css('display', '');
            $('#desafio_carta_esq .desafio_info').html(htmlEmBreve);
            $('#desafio_carta_esq .desafio_info').css('display', '');
            $('#desafio_carta_dir .desafio_info').html(htmlEmBreve);
            $('#desafio_carta_dir .desafio_info').css('display', '');

            $('.desafios_termina_em').text('-');
            return;
        }

        // Centro
        const desafio_centro = desafios.filter(d => {
            return d.apenas_doador === 0;
        })[0];
        const img_name = desafio_centro.orientador.name.replace(' ', '').trim().toLowerCase();
        $('#desafio_carta_centro .desafio_carta_conteudo .desafio_orientador img').attr('src', 'imagens/desafios/personagens/' + img_name + '.png');
        $('#desafio_carta_centro .desafio_carta_conteudo .desafio_xp').html('+' + desafio_centro.desafio.xp + ' pontos');
        $('#desafio_carta_centro .desafio_carta_conteudo .desafio_descricao').html(desafio_centro.desafio.description);
        if (desafio_centro.concluido) {
            $('#desafio_carta_centro .desafio_info').html('<p>Realizado</p><i class="material-icons">done_outline</i>');
            $('#desafio_carta_centro .desafio_info').css('display', '');
        } else {
            $('#desafio_carta_centro .desafio_info').html('');
            $('#desafio_carta_centro .desafio_info').css('display', 'none');
        }
        const dateOptions = {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        const terminaEm = new Date(Date.parse(desafio_centro.termina_em + ' GMT'));
        $('.desafios_termina_em').text('Novos desafios em ' + terminaEm.toLocaleDateString("pt-BR", dateOptions));

        // Esquerda, Direita
        const ordem = ['esq', 'dir'];
        const desafios_doadores = desafios.filter(d => {
            return d.apenas_doador === 1;
        });
        const nomeDoadores = _doadores.map(d => d['nome']) || [];
        const doador = nomeDoadores.includes(_usuario) || false;
        for (let i = 0; i < desafios_doadores.length; ++i) {
            const desafio = desafios_doadores[i];
            const img_name = desafio.orientador.name.replace(' ', '').trim().toLowerCase();
            $('#desafio_carta_' + ordem[i] + ' .desafio_carta_conteudo .desafio_orientador img').attr('src', 'imagens/desafios/personagens/' + img_name + '.png');
            $('#desafio_carta_' + ordem[i] + ' .desafio_carta_conteudo .desafio_xp').html('+' + desafio.desafio.xp + ' pontos');
            $('#desafio_carta_' + ordem[i] + ' .desafio_carta_conteudo .desafio_descricao').html(desafio.desafio.description);

            if (doador) {
                if (desafio.concluido) {
                    $('#desafio_carta_' + ordem[i] + ' .desafio_info').html('<p>Realizado</p><i class="material-icons">done_outline</i>');
                    $('#desafio_carta_' + ordem[i] + ' .desafio_info').css('display', '');
                } else {
                    $('#desafio_carta_' + ordem[i] + ' .desafio_info').html('');
                    $('#desafio_carta_' + ordem[i] + ' .desafio_info').css('display', 'none');
                }
            } else {
                $('#desafio_carta_' + ordem[i] + ' .desafio_info').html('<p>Somente doador</p>');
                $('#desafio_carta_' + ordem[i] + ' .desafio_info').css('display', '');
            }
        }
    };
};
