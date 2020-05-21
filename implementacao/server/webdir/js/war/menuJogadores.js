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
    this.preencheElementoHtml = function () {
        menuJogadores = $('#menu_jogadores .menu_jogadores_grid');
        menuJogadores.html('');
        for (var i = 0; i < 6; ++i) {
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
};
