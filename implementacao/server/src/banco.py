#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sqlite3


class Banco(object):

    def __init__(self):
        self.conn = sqlite3.connect("war.db")

    def registraUsuario(self, usuario, senha, email):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO Usuarios(nome, senha, email) VALUES(?,?,?)"
            cursor.execute(sql, (usuario, senha, email))
            self.conn.commit()

        except sqlite3.Error:
            if self.conn:
                self.conn.rollback()

    def atualizaSenha(self, codigo, email, senha):
        retorno = False
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE Usuarios SET senha = ? WHERE EXISTS (SELECT 1 FROM RecuperacaoSenha rs WHERE rs.codigo = ? AND Usuarios.email = rs.email AND rs.email = ?)"
            cursor.execute(sql, (senha, codigo, email))
            retorno = cursor.rowcount > 0
            self.conn.commit()
        except sqlite3.Error:
            if self.conn:
                self.conn.rollback()
        return retorno

    def verificaCredenciaisDoUsuario(self, usuario, senha):
        retorno = None

        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT nome FROM Usuarios WHERE (nome = ? OR email = ?) AND senha = ?"
            cursor.execute(sql, (usuario, usuario, senha))
            linha = cursor.fetchone()

            if linha:
                retorno = linha[0]

        return retorno

    def usuarioExiste(self, usuario, email):
        retorno = False

        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM Usuarios WHERE nome = ? OR email = ?"
            cursor.execute(sql, (usuario, email,))
            linha = cursor.fetchone()

            retorno = (linha != None)

        return retorno

    def emailExiste(self, email):
        with self.conn:
            cursor = self.conn.cursor()
            sql = "SELECT senha FROM Usuarios WHERE email = ?"
            cursor.execute(sql, (email,))
            linha = cursor.fetchone()

            retorno = (linha != None)

        return retorno

    def geraCodigoRecuperacao(self, email):
        codigo = None
        try:
            codigo = str(random.randint(1000, 9999))
            cursor = self.conn.cursor()
            sql = "INSERT OR REPLACE INTO RecuperacaoSenha(email, codigo) VALUES(?,?)"
            cursor.execute(sql, (email, codigo))
            self.conn.commit()

        except:
            if self.conn:
                self.conn.rollback()
        return codigo
