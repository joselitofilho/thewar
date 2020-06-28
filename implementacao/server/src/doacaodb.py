#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


class DoacaoDB(object):

    def __init__(self, baseDeDados='war.db'):
        self.baseDeDados = baseDeDados

    def doadores(self):
        doadores = []
        conn = sqlite3.connect(self.baseDeDados)
        try:
            c = conn.cursor()
            rows = c.execute(
                'SELECT distinct (nome) FROM Doacoes d INNER JOIN Usuarios u ON u.id = d.idUsuario;').fetchall()

            if rows:
                for row in rows:
                    doadores.append({'nome': row[0]})
        except:
            pass
        finally:
            conn.close()

        return {'doadores': doadores}

    def nomes_doadores(self):
        doadores = []
        conn = sqlite3.connect(self.baseDeDados)
        try:
            c = conn.cursor()
            rows = c.execute(
                'SELECT distinct (nome) FROM Doacoes d INNER JOIN Usuarios u ON u.id = d.idUsuario;').fetchall()

            if rows:
                for row in rows:
                    doadores.append(row[0])
        except:
            pass
        finally:
            conn.close()

        return doadores

    def meta_doacoes_progresso(self):
        valor_arrecado = 0
        conn = sqlite3.connect(self.baseDeDados)
        with conn:
            c = conn.cursor()
            row = c.execute(
                "SELECT COALESCE (100.0 * SUM(d.valor) / ( SELECT CAST(c.valor AS DECIMAL) FROM Configuracoes c WHERE chave = 'meta_doacao' ), 0) AS valor FROM Doacoes d WHERE d.valor > 0;").fetchone()
            if row:
                valor_arrecado = row[0]

        return valor_arrecado
