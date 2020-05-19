import csv
import json


def ler_csv():
    with open('ranking.csv', 'r') as arquivo_csv:
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


def gerar_json(ranking):
    with open('ranking.json', 'w') as arquivo_json:
        json.dump(ranking, arquivo_json)


def main():
    ranking = ler_csv()
    gerar_json(ranking)


if __name__ == "__main__":
    main()
