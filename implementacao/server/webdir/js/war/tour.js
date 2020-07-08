var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Tour = function () {

    this.pages = [];

    this.toogle = function () {
        if ($('#tour_painel').css('visibility') === 'visible') {
            $('#tour_painel').css('visibility', 'hidden');
        } else {
            $('#tour_painel').css('visibility', 'visible');
        }
    };

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

    this.start = function () {
        this.init();
        this.toogle();

        $('#tour_btn_page_2').removeClass('war_button_active');
        $('#tour_btn_page_3').removeClass('war_button_active');

        $('#tour_conteudo').removeClass();
        $('#tour_conteudo').addClass(this.pages['page_1'].page.class);
        $('#tour_header .tour_titulo').text(this.pages['page_1'].page.title);

        this.pageActive = this.pages['page_1'];
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
