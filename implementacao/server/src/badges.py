#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json


class Badges(object):

    def ler_csv(self, path):
        with open(path, 'r') as arquivo_csv:
            leitor = csv.reader(arquivo_csv, delimiter=',')
            next(leitor)
            ranking = []
            for coluna in leitor:
                patente = {
                    "level": coluna[0],
                    "name": coluna[1],
                    "xp": coluna[2],
                    "level_up": coluna[3]
                }
                ranking.append(patente)
        return ranking

    def gerar_json(self, ranking):
        with open('bdgs.json', 'w') as arquivo_json:
            json.dump(ranking, arquivo_json)

    def gerar_css(self):
        w, h = 400, 240
        lines = 6
        columns = 10

        with open('insignias_x{}.css'.format(w // columns), 'w') as arquivo_css:
            nv_i = 0
            for i in range(0, (lines * columns)):
                lin = (i % columns) * (w // columns) * -1
                col = (i // columns) * (w // columns) * -1
                txt = ".insignias_x%s_nv%s {background: url('../imagens/insignias_%sx%s.png') %spx %spx no-repeat;}" % \
                      (w // columns, nv_i, w, h, lin, col)
                nv_i += 1
                arquivo_css.write(txt + '\n')

# def main():
#     badges = Badges()
#     ranking = badges.ler_csv()
#     badges.gerar_json(ranking)
#     badges.gerar_css()
#
#
# if __name__ == "__main__":
#     main()
