#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sqlite3


class Desafios(object):

    def __init__(self, baseDeDados='war.db'):
        self.baseDeDados = baseDeDados

        self.carrega_infos()

    def carrega_infos(self):
        self.desafios_json = []
        self.orientadores_json = []
        self.desafios_em_andamento = []
        
        desafios_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'desafios.json')
        with open(desafios_path, 'r') as f:
            self.desafios_json = json.load(f)

        orientadores_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'orientadores.json')
        with open(orientadores_path, 'r') as f:
            self.orientadores_json = json.load(f)

        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rows = c.execute("SELECT idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm FROM DesafiosEmAndamento WHERE datetime('now') BETWEEN iniciaEm AND terminaEm;").fetchall()
        for row in rows:
            idDesafio = row[0]
            nomeOrientador = row[1]
            for desafio in self.desafios_json:
                if desafio['id'] == idDesafio:
                    break
            for orientador in self.orientadores_json:
                if orientador['name'] == nomeOrientador:
                    break
            self.desafios_em_andamento.append({
                "desafio": desafio,
                "orientador": orientador,
                "apenas_doador": row[2],
                "inicia_em": row[3],
                "termina_em": row[4]
            })

        conn.close()

    def em_andamento(self, usuario=None):
        self.carrega_infos()

        if usuario:
            conn = sqlite3.connect(self.baseDeDados)
            c = conn.cursor()
            rows = c.execute(
                """
                SELECT da.idDesafio
                  FROM DesafiosEmAndamento da 
                  JOIN DesafiosConcluidos dc ON dc.idDesafio = da.idDesafio 
                  JOIN Usuarios u ON u.id = dc.idUsuario 
                 WHERE dc.data BETWEEN da.iniciaEm AND da.terminaEm AND u.nome = ?;
                """, [usuario]).fetchall()
            desafiosId = []
            for row in rows:
                desafiosId.append(row[0])
            conn.close()

            for d in self.desafios_em_andamento:
                d['concluido'] = d['desafio']['id'] in desafiosId

        return self.desafios_em_andamento
