_ranking = [];
_insignias = [];

function ranking_levelByXp(xp) {
    var level = 0;
    if (xp > 0) {
        for (var i = 0; i < _insignias.length; ++i) {
            if (xp < parseInt(_insignias[i].xp)) {
                level = i - 1;
                break;
            }
        }
    }
    return level;
}

function ranking_processaMsg(params) {
    _ranking = params['ranking'];
    _insignias = params['badges'];

    const mapaRankingUsuarios = {};
    for (let i = 0; i < _ranking.length; ++i) {
        let r = _ranking[i];
        mapaRankingUsuarios[r.nome] = r;
    }
    return mapaRankingUsuarios;
}