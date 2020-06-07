var jogos = jogos || {};
jogos.war = jogos.war || {};

function util_handleQuestionAnswer(pergunta, resposta) {
    const texto = "Minha resposta é \"" + resposta + "\" para a pergunta \"" + pergunta + "\"";
    if (_chatJogo && _chatJogo.estaAtivo()) {
        _chatJogo.handleQuestionAnswerCallback(texto);
    } else if (_chatGeral) {
        _chatGeral.handleQuestionAnswerCallback(texto);
    }
}

jogos.war.Util = function () {

    const _comandos = {
        lista: [
            "a1", "a6",
            "bial1", "bial2", "bial3", "bial4",
            "capitao1", "capitao2",
            "d1", "d6", "discord",
            "funeral1", "funeral2", "funeral3",
            "joker1",
            "pergunta",
            "rank",
            "whatsapp"
        ],
        a1: {regex: /:a1/g, html: "<div style='display: inline-block;'><div class='dado dado_ataque dado_ataque1'></div></div>"},
        a6: {regex: /:a6/g, html: "<div style='display: inline-block;'><div class='dado dado_ataque dado_ataque6'></div></div>"},
        bial1: {regex: /:bial1/g, html: "<img class='meme' src='../imagens/memes/bial1.jpeg'/>"},
        bial2: {regex: /:bial2/g, html: "<img class='meme' src='../imagens/memes/bial2.jpeg'/>"},
        bial3: {regex: /:bial3/g, html: "<img class='meme' src='../imagens/memes/bial3.jpeg'/>"},
        bial4: {regex: /:bial4/g, html: "<img class='meme' src='../imagens/memes/bial4.jpeg'/>"},
        capitao1: {regex: /:capitao1/g, html: "<img class='meme' src='../imagens/memes/capitao1.jpeg'/>"},
        capitao2: {regex: /:capitao2/g, html: "<img class='meme' src='../imagens/memes/capitao2.jpeg'/>"},
        d1: {regex: /:d1/g, html: "<div style='display: inline-block;'><div class='dado dado_ataque dado_defesa1'></div></div>"},
        d6: {regex: /:d6/g, html: "<div style='display: inline-block;'><div class='dado dado_ataque dado_defesa6'></div></div>"},
        discord: {
            regex: /:discord/g,
            html: '<a href="https://discord.gg/2Xr8TyR" target="_blank" rel="noopener noreferrer"><img height="64px" src="../../imagens/social/discord.png" /></a>'
        },
        funeral1: {
            regex: /:funeral1/g,
            html:
                '<audio class="meme meme_audio" controls><source src="../../sons/funeral1.mp3" type="audio/mpeg">' +
                '    Your browser does not support the audio element.' +
                '</audio>',
            sound: 'funeral1.mp3'
        },
        funeral2: {
            regex: /:funeral2/g,
            html:
                '<audio class="meme meme_audio" controls><source src="../../sons/funeral2.mp3" type="audio/mpeg">' +
                '    Your browser does not support the audio element.' +
                '</audio>',
            sound: 'funeral2.mp3'
        },
        funeral3: {
            regex: /:funeral3/g,
            html:
                '<audio class="meme meme_audio" controls><source src="../../sons/funeral3.mp3" type="audio/mpeg">' +
                '    Your browser does not support the audio element.' +
                '</audio>' +
                '<img class="meme" src="../imagens/memes/funeral3.gif"/>',
            sound: 'funeral3.mp3'
        },
        joker1: {regex: /:joker1/g, html: "<img class='meme' src='../imagens/memes/joker1.jpeg'/>"},
        pergunta: {
            regex: /:pergunta(\w+|\W+)*\?(\w+|\W+)*,(\w+|\W+)*/gm,
            html:
                '<div class="question_box">' +
                '    <div class="question_text">' +
                '        <p>{pergunta}</p>' +
                '    </div>' +
                '    <div class="question_options">' +
                '        <button onClick="util_handleQuestionAnswer(\'{pergunta}\', \'{resposta_positiva}\')">{resposta_positiva}</button>' +
                '        <button onClick="util_handleQuestionAnswer(\'{pergunta}\', \'{resposta_negativa}\')">{resposta_negativa}</button>' +
                '    </div>' +
                '</div>'
        },
        rank: {regex: /:rank/g, html: "<div class='comando_rank insignia_size insignias_x40_nv{level}'></div>"},
        whatsapp: {
            regex: /:whatsapp/g,
            html: '<a href=\"https://chat.whatsapp.com/DjRwmsDjKJUEUh9HLyFky2\" target=\"_blank\" rel=\"noopener noreferrer\"><img height=\"64px\" src=\"../../imagens/social/whatsapp.png\" /></a>'
        },
    };

    this.dataAtualFormatada = function () {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth();
        var day = date.getDate();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var seconds = date.getSeconds();

        return day + "/" + month + "/" + year + " " + hour + ":" + minute;
    };

    this.substituiMarcacoes = function (listaUsuarios, usuarioQueEnviou, texto) {
        if (texto.match(/:comandos/) || texto.match(/:memes/)) {
            return "Memes disponíveis --> " + ":" + Array.from(_comandos.lista).join(', :');
        } else {
            const cmdKey = "pergunta";
            const cmd = _comandos[cmdKey];
            const match = texto.match(cmd.regex);
            if (match !== null) {
                texto = match[0].trim();
                const textoSplit = texto.split('?');
                const pergunta = textoSplit[0].replace(':' + cmdKey, '').trim() + '?';
                const opcoes = textoSplit[1].split(',');
                texto = cmd.html
                    .replace(/{pergunta}/g, pergunta)
                    .replace(/{resposta_positiva}/g, opcoes[0].trim())
                    .replace(/{resposta_negativa}/g, opcoes[1].trim());
                return texto;
            }
        }
        texto = this.substituiURLPorHTMLLinks(texto);
        texto = this.substituiComandos(listaUsuarios, usuarioQueEnviou, texto);
        return texto;
    };

    this.substituiURLPorHTMLLinks = function (texto) {
        var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        var urls = texto.match(exp);
        if (urls) {
            for (i = 0; i < urls.length; i++) {
                if (this.temImagemNaURL(urls[i]))
                    texto = texto.replace(urls[i], "<object data='" + urls[i] + "'></object>");
                else
                    texto = texto.replace(urls[i], "<a href='" + urls[i] + "' target='_blank'>" + urls[i] + "</a>");
            }
        }
        return texto;
    };

    this.temImagemNaURL = function (texto) {
        return (/(jpg|gif|png)$/.test(texto));
    };

    this.substituiComandos = function (listaUsuarios, usuarioQueEnviou, texto) {
        for (let i = 0; i < _comandos.lista.length; ++i) {
            const cmdKey = _comandos.lista[i];
            const cmd = _comandos[cmdKey];
            if (cmdKey === "rank") {
                if (listaUsuarios[usuarioQueEnviou]) {
                    const level = ranking_levelByXp(listaUsuarios[usuarioQueEnviou].pontos);
                    const elemento = cmd.html.replace("{level}", level);
                    texto = texto.replace(cmd.regex, elemento);
                }
            } else {
                if (cmdKey === "funeral1" ||
                    cmdKey === "funeral2" ||
                    cmdKey === "funeral3") {
                    if (texto.match(cmd.regex)) {
                        tocarSom(this, cmd.sound);
                    }
                }
                texto = texto.replace(cmd.regex, cmd.html);
            }
        }
        return texto;
    };
};

var listaFadeinPoligono = {};
var listaFadeoutPoligono = {};

var MAX_ALPHA = 1.0;
var MIN_ALPHA = 0.5;

function utilTerritorio_polygonFadein(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeinPoligono[codigoTerritorio] == null) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = (MAX_ALPHA - MIN_ALPHA) / (milliseconds / 50.0);
        fadein = setInterval(function () {
            opacidadeAtual += inc;

            if (opacidadeAtual >= MAX_ALPHA) {
                clearInterval(listaFadeinPoligono[codigoTerritorio]);
                listaFadeinPoligono[codigoTerritorio] = null;
                delete listaFadeinPoligono[codigoTerritorio];
                if (typeof (callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.min(MAX_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeinPoligono[codigoTerritorio] = fadein;
    }
}

function utilTerritorio_polygonFadeout(codigoTerritorio, polygon, milliseconds, callback) {
    if (listaFadeoutPoligono[codigoTerritorio] == null) {
        var opacidadeAtual = Number(polygon.fillOpacity);
        var inc = (MAX_ALPHA - MIN_ALPHA) / (milliseconds / 50.0);
        fadeout = setInterval(function () {
            opacidadeAtual -= inc;

            if (opacidadeAtual <= MIN_ALPHA) {
                clearInterval(listaFadeoutPoligono[codigoTerritorio]);
                listaFadeoutPoligono[codigoTerritorio] = null;
                delete listaFadeoutPoligono[codigoTerritorio];
                if (typeof (callback) == 'function')
                    callback();
                return;
            }

            polygon.setOptions({'fillOpacity': Math.max(MIN_ALPHA, Number(opacidadeAtual))});
        }, 50);

        listaFadeoutPoligono[codigoTerritorio] = fadeout;
    }
}

function utilRetiraAcento(palavra) {
    return palavra.replace(/[\W_]+/g," ");
}
