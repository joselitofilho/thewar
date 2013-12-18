#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Banco(object):

    def __init__(self):
        self.conn = sqlite3.connect("war.db")
        
    def registraUsuario(self, usuario, senha):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO Usuarios(nome, senha) VALUES(?,?)"
            cursor.execute(sql, (usuario, senha))
            self.conn.commit()
        
        except sqlite3.Error, e:
            if self.conn:
                self.conn.rollback()
            print "Error %s:" % e.args[0]
            
    def verificaCredenciaisDoUsuario(self, usuario, senha):
        retorno = False

        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM Usuarios WHERE nome = ? AND senha = ?"
            cursor.execute(sql, (usuario, senha))
            linha = cursor.fetchone()

            retorno = (linha != None)

        return retorno

    def usuarioExiste(self, usuario):
        retorno = False

        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM Usuarios WHERE nome = ?"
            cursor.execute(sql, (usuario,))
            linha = cursor.fetchone()

            retorno = (linha != None)

        return retorno
