#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from src.desafios.desafios import *


def main():
    database = 'war.db'
    desafios = Desafios(database)

    con = sqlite3.connect(database)
    with con:
        cur = con.cursor()

        desafios_iniciaram_ontem = cur.execute(
            "SELECT idDesafio FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now', '-1 DAY'), time('23:00:00'));").fetchall()
        if len(desafios_iniciaram_ontem) != 3:
            cur.execute(
                "DELETE FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now', '-1 DAY'), time('23:00:00'));")
            for apenas_doador in [1, 0, 1]:
                id_desafio = desafios.shuffle_desafios(apenas_doador)['id']
                nome_orientador = desafios.shuffle_orientadores(apenas_doador)['name']
                cur.execute(
                    "INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (?, ?, ?, datetime(date('now', '-1 DAY'), time('23:00:00')), datetime(date('now'), time('22:59:59')));",
                    [id_desafio, nome_orientador, apenas_doador])

        desafios_vao_iniciar = cur.execute(
            "SELECT idDesafio FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now'), time('23:00:00'));").fetchall()
        if len(desafios_vao_iniciar) != 3:
            cur.execute("DELETE FROM DesafiosEmAndamento WHERE iniciaEm = datetime(date('now'), time('23:00:00'));")
            for apenas_doador in [1, 0, 1]:
                id_desafio = desafios.shuffle_desafios(apenas_doador)['id']
                nome_orientador = desafios.shuffle_orientadores(apenas_doador)['name']
                cur.execute(
                    "INSERT INTO DesafiosEmAndamento (idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm) VALUES (?, ?, ?, datetime(date('now'), time('23:00:00')), datetime(date('now', '+1 DAY'), time('22:59:59')));",
                    [id_desafio, nome_orientador, apenas_doador])

        con.commit()


if __name__ == "__main__":
    main()
