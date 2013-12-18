#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Banco(object):

    def __init__(self):
        self.conn = sqlite3.connect("war.db")

    def usuarioExiste(self, usuario, senha):
        retorno = False

        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM Usuarios WHERE nome=? AND senha=?"
            cursor.execute(sql, (usuario, senha))
            linha = cursor.fetchone()

            retorno = (linha != None)

        return retorno
