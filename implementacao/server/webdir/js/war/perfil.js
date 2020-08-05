var jogos = jogos || {};
jogos.war = jogos.war || {};

jogos.war.Perfil = function (historicoBatalhasDiv) {

    this.preencheHistoricoBatalhas = function (usuario, historicoBatalhas) {
        historicoBatalhas = historicoBatalhas || [];

        const dateOptions = {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };

        const trofeu_svg = [
            "<svg class='trofeu' xmlns='http://www.w3.org/2000/svg' width='20'",
            "     height='20' viewBox='0 0 24 24' fill='#ffe34c' stroke='#ffe34c'>",
            "    <path d='M19 1c0 9.803-5.094 13.053-5.592 17h-2.805c-.498-3.947-5.603-7.197-5.603-17h14zm-7.305 13.053c-1.886-3.26-2.635-7.432-2.646-11.053h-1.699c.205 4.648 1.99 8.333 4.345 11.053zm1.743 4.947h-2.866c-.202 1.187-.63 2.619-2.571 2.619v1.381h8v-1.381c-1.999 0-2.371-1.432-2.563-2.619zm7.08-1.596c-1.402-.634-2.609-.19-3.354.293.745-.484 1.603-1.464 1.595-3.003-2.591 1.038-2.295 2.496-2.765 3.345-.315.571-1.007.274-1.007.274l-.213.352c.365.193.989.319 1.716.319 1.307 0 2.949-.409 4.028-1.58zm2.444-4.022c-1.382.097-2.118 1.061-2.501 1.763.383-.702.614-1.942-.05-3.158-1.61 1.929-.752 2.958-.762 3.831-.004.427-.49.417-.49.417l.007.404c.314-.041 3.154-.717 3.796-3.257zm1.036-3.87c-1.171.426-1.56 1.473-1.718 2.175.158-.702.041-1.863-.835-2.75-.915 2.068.082 2.745.29 3.503.102.371-.325.606-.325.606l.29.179c.061-.029 2.385-1.332 2.298-3.713zm-.2-3.792c-.903.666-1.017 1.688-.974 2.335-.042-.646-.395-1.639-1.376-2.182-.264 2.018.769 2.349 1.142 2.95.182.294.023.658.023.658l.284-.019s.026-.127.169-.442c.291-.644 1.255-1.334.732-3.3zm-1.901-2.72s-.273.984-.045 1.732c.244.798.873 1.361.873 1.361s.34-.873.099-1.733c-.222-.792-.927-1.36-.927-1.36zm-12.67 15.665l-.213-.352s-.691.297-1.007-.274c-.47-.849-.174-2.307-2.765-3.345-.008 1.539.85 2.52 1.595 3.003-.745-.484-1.952-.927-3.354-.293 1.078 1.171 2.721 1.581 4.028 1.581.727-.001 1.35-.127 1.716-.32zm-4.393-2.027l.007-.404s-.486.01-.49-.417c-.009-.873.848-1.901-.762-3.831-.664 1.216-.433 2.457-.05 3.158-.383-.702-1.12-1.666-2.501-1.763.642 2.541 3.482 3.217 3.796 3.257zm-2.533-3.413l.29-.179s-.427-.236-.325-.606c.208-.758 1.205-1.435.29-3.503-.876.887-.994 2.048-.835 2.75-.158-.702-.546-1.749-1.718-2.175-.088 2.381 2.236 3.684 2.298 3.713zm-1.366-4.204c.143.315.169.442.169.442l.284.019s-.159-.364.023-.658c.373-.601 1.405-.933 1.142-2.95-.983.542-1.335 1.534-1.377 2.181.042-.647-.072-1.67-.974-2.335-.523 1.966.441 2.656.733 3.301zm.241-4.661c-.24.86.099 1.733.099 1.733s.629-.563.873-1.361c.228-.748-.045-1.732-.045-1.732s-.705.568-.927 1.36z'></path>",
            "</svg>"
        ].join("");

        const cpu_svg = [
            "<svg class='svg_cpu' viewBox='0 0 24 24'>",
            "    <path fill='var(--bg-color)'",
            "          d='M4,6H20V16H4M20,18A2,2 0 0,0 22,16V6C22,4.89 21.1,4 20,4H4C2.89,4 2,4.89 2,6V16A2,2 0 0,0 4,18H0V20H24V18H20Z'/>",
            "</svg>"
        ].join("");

        const lp_player_cor = ["lp_player_card-red", "lp_player_card-blue", "lp_player_card-green", "lp_player_card-black", "lp_player_card-white", "lp_player_card-yellow"];

        const historicoBatalhasLimiteMax = historicoBatalhas.length;
        for (var i = 0; i < historicoBatalhasLimiteMax; ++i) {
            const jogadores = historicoBatalhas[i].jogadores || [];
            const ordem = historicoBatalhas[i].ordem || [];
            const vencedor = historicoBatalhas[i].vencedor || {};
            const pontuacao = historicoBatalhas[i].pontuacao || {};

            const venceu = vencedor.usuario === usuario;

            var newItem = $("<div>").attr("id", 'historico_batalha_item_' + i);

            var span_venceu_ou_perdeu = "<span>VENCEU</span>";
            if (!venceu) {
                span_venceu_ou_perdeu = "<span>PERDEU</span>";
            }
            var lp_venceu_ou_perdeu = "lp_venceu";
            if (!venceu) {
                lp_venceu_ou_perdeu = "lp_perdeu";
            }
            var lp_header_item_right_venceu_ou_perdeu = "lp_header_item_right_venceu";
            if (!venceu) {
                lp_header_item_right_venceu_ou_perdeu = "lp_header_item_right_perdeu";
            }

            var pontos = pontuacao[vencedor.usuario] || 0;
            if (pontos > 0) {
                pontos = "+" + pontos + " pontos";
            } else {
                pontos = "0 pontos";
            }

            var iniciouEm = new Date(0);
            iniciouEm.setUTCSeconds(historicoBatalhas[i].iniciou_em / 1000);
            iniciouEm = iniciouEm.toLocaleDateString("pt-BR", dateOptions);

            var duracao = (historicoBatalhas[i].terminou_em - historicoBatalhas[i].iniciou_em) / 1000;
            duracao /= 60;
            duracao = duracao.toFixed(0);
            if (duracao < 60) {
                if (duracao < 10) {
                    duracao = "0" + duracao;
                }
                duracao += " m";
            } else {
                duracao /= 60;
                duracao = duracao.toFixed(0);
                if (duracao < 10) {
                    duracao = "0" + duracao;
                }
                duracao += " h";
            }

            var conteudo = [
                "<div class='lp_row'>",
                "    <div style='display: flex; flex-direction: column;'>",
                "        <div class='lp_content_item'>",
                "            <div class='lp_players_box'>",
                "                <div class='lp_header_item lp_header_item_infos ", lp_venceu_ou_perdeu, "'>",
                "                    <div style='display: flex; justify-content: center; align-items: center; height: 40px; border-bottom: 4px solid var(--color-dark-brown);'>",
                span_venceu_ou_perdeu,
                "                    </div>",
                "                    <span style='text-align: left; display: flex; justify-content: center; align-items: center; padding-left: 16px;'>", pontos, "</span>",
                "                    <div>",
                "                        <div class='lp_header_item_footer'>",
                "                            <i class='material-icons-outlined md-24'>timer</i>", duracao,
                "                        </div>",
                "                    </div>",
                "                </div>",
                "                <div class='lp_header_item lp_header_item_right ", lp_header_item_right_venceu_ou_perdeu, "'>",
                "                    <div style='display: flex; align-items: center; justify-content: center; height: 40px; border-bottom: 4px solid var(--color-dark-brown);'></div>",
                "                    <div class='lp_header_item_footer'></div>",
                "                </div>"
            ];

            for (var j = 0; j < ordem.length; ++j) {
                const posicao = ordem[j];
                const jogador = jogadores[posicao];

                var trofeu = "";
                if (jogador.usuario === vencedor.usuario) {
                    trofeu = trofeu_svg;
                }

                const lp_player_card_color = lp_player_cor[posicao];

                var insignia = cpu_svg;
                if (jogador.tipo === "human") {
                    insignia = "<div class='insignia_x40_size insignias_x40_nv11'></div>";
                }

                conteudo = conteudo.concat([
                    "<a href='#' class='lp_players_item lp_player_card ", lp_player_card_color, "'>",
                    "   <div class='lp_player_card_content'>",
                    "       <div class='circle'>", insignia, "</div>",
                    "       <div class='lp_player_card_footer'>",
                    "           <span class='lp_player_footer_name'>", jogador.usuario, "</span>",
                    "           <div class='lp_player_footer_badges'>", trofeu, "</div>",
                    "       </div>",
                    "   </div>",
                    "</a>"
                ]);
            }
            conteudo = conteudo.concat([
                "            </div>",
                "            <div style='width: 135px;height: 180px;transform: scale(0.45);margin: -50px 45px 0 0px;'>",
                "                <div id='partida_", i, "_objetivo' class='carta_objetivo carta_objetivo_1'></div>",
                "            </div>",
                "        </div>",
                "        <div class='lp_footer'>",
                "            <div class='lp_footer_item'>",
                "                <span class='material-icons-outlined md-24'>event</span>",
                "                <span>", iniciouEm, "</span>",
                "            </div>",
                "        </div>",
                "    </div>",
                "</div>"
            ]);
            newItem.html(conteudo.join(""));
            newItem.appendTo(historicoBatalhasDiv);
        }
    };

};