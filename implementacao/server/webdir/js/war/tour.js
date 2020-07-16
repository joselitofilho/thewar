var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Tour = function () {

    var that = this;

    this.pages = [];

    this.init = function () {
        const page_1 = {
            id: 'page_1',
            prev: null,
            page: {
                id: 'page_1',
                class: 'tour_1',
                title: 'Menu do jogo'
            },
            next: 'page_2'
        };

        const page_2 = {
            id: 'page_2',
            prev: 'page_1',
            page: {
                id: 'page_2',
                class: 'tour_2',
                title: 'Crie uma sala'
            },
            next: 'page_3'
        };

        const page_3 = {
            id: 'page_3',
            prev: 'page_2',
            page: {
                id: 'page_3',
                class: 'tour_3',
                title: 'Complete os desafios'
            },
            next: null
        };

        this.pages = {
            'page_1': page_1,
            'page_2': page_2,
            'page_3': page_3
        };
    };

    this.toogle = function () {
        if ($('#tour_painel').css('visibility') === 'visible') {
            $('#tour_painel').css('visibility', 'hidden');
        } else {
            $('#tour_painel').css('visibility', 'visible');
        }
    };

    this.show = function () {
        if ($('#tour_painel').css('visibility') === 'hidden') {
            $('#tour_painel').css('visibility', 'visible');
        }
    };

    this.hide = function () {
        if ($('#tour_painel').css('visibility') === 'visible') {
            $('#tour_painel').css('visibility', 'hidden');
        }
    };

    this.open = function () {
        this.init();
        this.show();

        $('#tour_btn_page_1').removeClass('war_button_active');
        $('#tour_btn_page_2').removeClass('war_button_active');
        $('#tour_btn_page_3').removeClass('war_button_active');

        $('#tour_btn_page_1').addClass('war_button_active');

        $('#tour_conteudo').removeClass();
        $('#tour_conteudo').addClass(this.pages['page_1'].page.class);
        $('#tour_header .tour_titulo').text(this.pages['page_1'].page.title);

        this.pageActive = this.pages['page_1'];
    };

    this.start = function () {
        this.hide();
        this.wait_creation_room = false;

        var enjoyhint_instance = new EnjoyHint({
            backgroundColor: "rgba(73, 54, 37, 0.8)",
            onEnd: function () {
                that.wait_creation_room = true;
            },
        });
        var enjoyhint_script_steps = [
            {
                'next #botao_ver_regras': 'Confira todas as regras do jogo, como distribuir suas tropas, atacar territórios e muito mais.',
            },
            {
                'next #botao_configuracoes': 'Altere as configurações do jogo.',
            },
            {
                'next #botao_ranking': 'Acompanhe o seu progresso no jogo e em qual posição no ranking você está.',
            },
            {
                'click #botao_desafios': 'Clique no botão "desafios" para ver quais são os desafios do dia.',
                onBeforeStart: function () {
                    _desafios.hide();
                },
            },
            {
                'next #desafio_carta_centro_descricao': 'Descrição do que você deve fazer para concluir o desafio.',
                onBeforeStart: function () {
                    _desafios.show();
                },
            },
            {
                'next #desafio_carta_centro_xp': 'Você ganha pontos adicionais ao concluir o desafio.',
                onBeforeStart: function () {
                    _desafios.show();
                },
            },
            {
                selector: '#desafios_header .desafios_termina_em',
                event_type: "next",
                description: 'Fique de olho quando os desafios terminam para você não perder nenhum.',
                onBeforeStart: function () {
                    $('body').enjoyhint("show_next");
                    _desafios.show();
                },
            },
            {
                'click #botao_criar_sala': 'Clique no botão "criar sala" para começar a jogar com seus amigos.',
                onBeforeStart: function () {
                    _desafios.hide();
                    that.wait_creation_room = true;
                },
            },
        ];

        enjoyhint_instance.set(enjoyhint_script_steps);
        enjoyhint_instance.run();
    };

    this.start_creation_room = function () {
        if (true === this.wait_creation_room) {
            this.wait_creation_room = false;
            this.hide();
            var enjoyhint_instance = new EnjoyHint({
                backgroundColor: "rgba(73, 54, 37, 0.8)",
            });
            var enjoyhint_script_steps = [
                {
                    selector: '#sala_' + _salaDoJogador + ' .sala_jogador_tipo.cor_azul',
                    event: "click",
                    description: 'Clique aqui para jogar contra a máquina.',
                },
                {
                    selector: '#sala_' + _salaDoJogador + ' .sala_jogador_tipo.cor_azul',
                    event: "click",
                    description: 'Clique novamente para impedir que outros jogadores joguem com essa cor nesta sala.',
                },
                {
                    selector: '#sala_' + _salaDoJogador + ' .sala_jogador_tipo.cor_azul',
                    event: "click",
                    description: 'Clique mais uma vez para liberar essa cor para os outros jogadores.',
                },
                {
                    selector: '#sala' + _salaDoJogador + '_jogador2',
                    event: "click",
                    description: 'Clique aqui para alterar a cor das suas tropas para azul.',
                },
                {
                    selector: '#btnIniciarPartida' + _salaDoJogador,
                    event: "click",
                    description: 'Quando estiver pronto, basta clicar no botão "iniciar partida". Divirta-se.',
                    skipButton: {text: "I got it"},
                },
            ];

            enjoyhint_instance.set(enjoyhint_script_steps);
            enjoyhint_instance.run();
        }
    };

    this.prev = function () {
        const pg = this.pageActive;
        if (pg && pg.prev) {
            const prev_page = this.pages[pg.prev];
            $('#tour_btn_' + pg.page.id).removeClass('war_button_active');
            $('#tour_btn_' + prev_page.page.id).addClass('war_button_active');

            $('#tour_conteudo').removeClass();
            $('#tour_conteudo').addClass(prev_page.page.class);
            $('#tour_header .tour_titulo').text(prev_page.page.title);

            this.pageActive = prev_page;
        }
    };

    this.next = function () {
        const pg = this.pageActive;
        if (pg && pg.next) {
            const next_page = this.pages[pg.next];
            $('#tour_btn_' + pg.page.id).removeClass('war_button_active');
            $('#tour_btn_' + next_page.page.id).addClass('war_button_active');

            $('#tour_conteudo').removeClass();
            $('#tour_conteudo').addClass(next_page.page.class);
            $('#tour_header .tour_titulo').text(next_page.page.title);

            this.pageActive = next_page;
        }
    };

    this.to_page = function (pageId) {
        const pg = this.pageActive;
        const next_page = this.pages[pageId];
        if (pg && next_page) {
            $('#tour_btn_' + pg.page.id).removeClass('war_button_active');
            $('#tour_btn_' + next_page.page.id).addClass('war_button_active');

            $('#tour_conteudo').removeClass();
            $('#tour_conteudo').addClass(next_page.page.class);
            $('#tour_header .tour_titulo').text(next_page.page.title);

            this.pageActive = next_page;
        }
    };
};
