var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Desafios = function () {

    this.processaMsg = function (params) {
        this.preencheElementoHtml(params);
    };

    this.show = function () {
        if ($('#desafios_painel').css('visibility') === 'hidden') {
            $('#desafios_painel').css('visibility', 'visible');
        }
    };

    this.hide = function () {
        if ($('#desafios_painel').css('visibility') === 'visible') {
            $('#desafios_painel').css('visibility', 'hidden');
        }
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

        // Verificação se o usuário é doador.
        const nomeDoadores = _doadores.map(d => d['nome']) || [];
        const doador = nomeDoadores.includes(_usuario) || false;

        // Centro
        let desafio_centro = desafios
            .sort((a, b) => {
                return a.concluido - b.concluido;
            })
            .sort((a, b) => {
                return a.ordem > b.ordem;
            })
            .filter(d => {
                if (!doador) {
                    return d.apenas_doador === 0 && d.ordem === 0;
                }
                return d.apenas_doador === 0;
            });

        const total_desafios_centro_restantes = desafios
            .filter(d => {
                return !d.concluido && d.apenas_doador === 0;
            }).length;
        console.log('total_desafios_centro_restantes', total_desafios_centro_restantes);
        let hh = '<p>Restam <b>' + total_desafios_centro_restantes + '</b></p>';
        if (!doador) {
            hh += '<p>Apenas para doadores</p>';
        }
        if (total_desafios_centro_restantes > 1) {
            $('#desafio_carta_centro_restantes').html(hh);
        }
        console.log('desafio_centro', desafio_centro);
        desafio_centro = desafio_centro[0];
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
