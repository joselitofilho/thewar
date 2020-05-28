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
