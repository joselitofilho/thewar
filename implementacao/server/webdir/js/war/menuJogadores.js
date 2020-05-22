var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.MenuJogadores = function () {
    const cores = [
        "cor_vermelha", "cor_azul", "cor_verde",
        "cor_preto", "cor_branco", "cor_amarelo"];
    const infoTerritoriosCores = [
        "info_territorios_vermelho", "info_territorios_azul", "info_territorios_verde",
        "info_territorios_preta", "info_territorios_branca", "info_territorios_amarela"];
    const infoCartasCores = [
        "info_cartas_vermelha", "info_cartas_azul", "info_cartas_verde",
        "info_cartas_preta", "info_cartas_branca", "info_cartas_amarela"];

    this.preencheElementoHtml = function (jogadoresDaSala) {
        menuJogadores = $('#menu_jogadores .menu_jogadores_grid');
        menuJogadores.html('');
        for (let p = 0; p < jogadoresDaSala.length; ++p) {
            const i = jogadoresDaSala[p].posicao;
            conteudo = "<div id='menu_jogador" + i + "' class='menu_jogadores_box'>";
            conteudo += "    <div class='menu_jogadores_box_title " + cores[i] + "'></div>";
            conteudo += "    <div id='menu_jogador" + i + "_insignia' class='menu_jogadores_box_badge'></div>";
            conteudo += "    <div id='jogador" + (i + 1) + "' class='menu_jogadores_box_name'>-</div>";
            conteudo += "    <div class='menu_jogadores_grid2x2 menu_jogadores_box_infos'>";
            conteudo += "        <div class='menu_jogadores_box_info_item'>";
            conteudo += "            <div class='info_territorios_ico " + infoTerritoriosCores[i] + "'></div>";
            conteudo += "            <span id='menu_jogador" + i + "_info_territorios'>-</span>";
            conteudo += "        </div>";
            conteudo += "        <div class='menu_jogadores_box_info_item'>";
            conteudo += "            <div class='info_cartas_ico " + infoCartasCores[i] + "'></div>";
            conteudo += "            <span id='menu_jogador" + i + "_info_cartas'>-</span>";
            conteudo += "        </div>";
            conteudo += "    </div>";
            conteudo += "</div>";
            menuJogadores.append(conteudo);
        }
    };

    this.posicionaElementos = function (jogadorQueComecou, jogadoresDaSala) {
        let corte = jogadorQueComecou;
        for (let i = 0; i < jogadoresDaSala.length; i++) {
            if (jogadoresDaSala[i].posicao === jogadorQueComecou) {
                corte = i;
                break;
            }
        }
        const jogadoresNaOrdem = jogadoresDaSala.slice(corte).concat(jogadoresDaSala.slice(0, corte));

        this.preencheElementoHtml(jogadoresNaOrdem);

        for (let i = 0; i < jogadoresNaOrdem.length; i++) {
            const infos = jogadoresNaOrdem[i];

            $("#menu_jogador" + infos.posicao + "_insignia").attr('class', 'menu_jogadores_box_badge');
            for (let j = 0; j < _ranking.length; ++j) {
                if (_ranking[j].nome === infos.usuario) {
                    $("#menu_jogador" + infos.posicao + "_insignia")
                        .addClass("insignia_size insignias_x40_nv" + ranking_levelByXp(_ranking[j].pontos));
                    break;
                }
            }

            $("#jogador" + (infos.posicao + 1)).html(infos.usuario);
            $("#menu_jogador" + infos.posicao + "_info_territorios").html(infos.total_territorios);
            $("#menu_jogador" + infos.posicao + "_info_cartas").html(infos.total_cartas_territorio);

            $("#jogador" + (infos.posicao + 1)).removeClass("text_through");
            if (!infos.esta_na_sala) {
                $("#jogador" + (infos.posicao + 1)).addClass("text_through");
            }
        }
    };
};
