#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sqlite3

from src.desafios.desafios import *


def main():
    random.seed()
    database = 'war.db'
    desafios = Desafios(database)

    con = sqlite3.connect(database)
    with con:
        cur = con.cursor()

        desafios_iniciaram_ontem = cur.execute(
            "SELECT idDesafio FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now', '-1 DAY'), time('10:00:00'));").fetchall()
        if len(desafios_iniciaram_ontem) != 3:
            cur.execute(
                "DELETE FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now', '-1 DAY'), time('10:00:00'));")
            orientadores = desafios.shuffle_orientadores()
            desafios_todos = desafios.shuffle_desafios(0)
            desafios_apenas_doador = desafios.shuffle_desafios(1)
            i = random.randint(0, len(orientadores) - 3)
            for apenas_doador in [1, 0, 1]:
                if apenas_doador == 0:
                    id_desafio = desafios_todos[random.randint(0, len(desafios_todos) - 1)]['id']
                else:
                    id_desafio = desafios_apenas_doador[random.randint(0, len(desafios_apenas_doador) - 1)]['id']
                nome_orientador = orientadores[i]['name']
                cur.execute(
                    "INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (?, ?, ?, datetime(date('now', '-1 DAY'), time('10:00:00')), datetime(date('now'), time('09:59:59')));",
                    [id_desafio, nome_orientador, apenas_doador])

                i += 1

        desafios_vao_iniciar = cur.execute(
            "SELECT idDesafio FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now'), time('10:00:00'));").fetchall()
        if len(desafios_vao_iniciar) != 3:
            cur.execute("DELETE FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now'), time('10:00:00'));")
            orientadores = desafios.shuffle_orientadores()
            desafios_todos = desafios.shuffle_desafios(0)
            desafios_apenas_doador = desafios.shuffle_desafios(1)
            i = random.randint(0, len(orientadores) - 3)
            for apenas_doador in [1, 0, 1]:
                if apenas_doador == 0:
                    id_desafio = desafios_todos[random.randint(0, len(desafios_todos) - 1)]['id']
                else:
                    id_desafio = desafios_apenas_doador[random.randint(0, len(desafios_apenas_doador) - 1)]['id']
                nome_orientador = orientadores[i]['name']
                cur.execute(
                    "INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (?, ?, ?, datetime(date('now'), time('10:00:00')), datetime(date('now', '+1 DAY'), time('09:59:59')));",
                    [id_desafio, nome_orientador, apenas_doador])

                i += 1

        con.commit()


if __name__ == "__main__":
    main()
