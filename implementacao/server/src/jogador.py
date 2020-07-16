#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator

from src.jsonserializer import *
from src.territorio import *


class TipoJogador:
    humano = "human"
    cpu = "cpu"
    desabilitado = "disable"


class JogadorDaSala(JSONSerializer):
    def __init__(self, usuario, posicao, dono, tipo=TipoJogador.humano):
        self.usuario = usuario
        self.posicao = posicao
        self.dono = dono
        self.tipo = tipo


class JogadorDoJogo(JSONSerializer):
    def __init__(self, usuario, posicao, dono, tipo):
        self.usuario = usuario
        self.posicao = posicao
        self.dono = dono
        self.tipo = tipo
        self.objetivo = -1

        self.territorios = []
        self.cartasTerritorio = []

        self.jogadoresDestruidos = []

    def iniciaTerritorios(self, codigosTerritorios):
        self.territorios = []
        for t in codigosTerritorios:
            self.territorios.append(Territorio(t))

    def gruposTerritorio(self):
        retorno = []

        codigosTerritorios = []
        for terr in self.territorios:
            codigosTerritorios.append(terr.codigo)

        temAsia = True
        for terr in GrupoTerritorio.ListaAsia:
            if terr not in codigosTerritorios:
                temAsia = False
        if temAsia:
            retorno.append(GrupoTerritorio.Asia)

        temAmericaDoNorte = True
        for terr in GrupoTerritorio.ListaAmericaDoNorte:
            if terr not in codigosTerritorios:
                temAmericaDoNorte = False
        if temAmericaDoNorte:
            retorno.append(GrupoTerritorio.AmericaDoNorte)

        temEuropa = True
        for terr in GrupoTerritorio.ListaEuropa:
            if terr not in codigosTerritorios:
                temEuropa = False
        if temEuropa:
            retorno.append(GrupoTerritorio.Europa)

        temAfrica = True
        for terr in GrupoTerritorio.ListaAfrica:
            if terr not in codigosTerritorios:
                temAfrica = False
        if temAfrica:
            retorno.append(GrupoTerritorio.Africa)

        temAmericaDoSul = True
        for terr in GrupoTerritorio.ListaAmericaDoSul:
            if terr not in codigosTerritorios:
                temAmericaDoSul = False
        if temAmericaDoSul:
            retorno.append(GrupoTerritorio.AmericaDoSul)

        temOceania = True
        for terr in GrupoTerritorio.ListaOceania:
            if terr not in codigosTerritorios:
                temOceania = False
        if temOceania:
            retorno.append(GrupoTerritorio.Oceania)

        return retorno

    def territoriosPorGrupo(self, listaGrupo, codigosTerritorios):
        territorios = []
        for terr in codigosTerritorios:
            if terr in listaGrupo:
                territorios.append(terr)
        return territorios

    def densidadePorGrupoTerritorio(self, listaGrupo, codigosTerritorios):
        qtd = 0
        for terr in listaGrupo:
            if terr in codigosTerritorios:
                qtd = qtd + 1
        return qtd * 100.0 / len(listaGrupo)

    def densidadeTodosGruposTerritorio(self):
        retorno = {}

        codigosTerritorios = []
        for terr in self.territorios:
            codigosTerritorios.append(terr.codigo)

        retorno[GrupoTerritorio.Asia] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaAsia, codigosTerritorios)
        retorno[GrupoTerritorio.AmericaDoNorte] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaAmericaDoNorte,
                                                                                   codigosTerritorios)
        retorno[GrupoTerritorio.Europa] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaEuropa,
                                                                           codigosTerritorios)
        retorno[GrupoTerritorio.Africa] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaAfrica,
                                                                           codigosTerritorios)
        retorno[GrupoTerritorio.AmericaDoSul] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaAmericaDoSul,
                                                                                 codigosTerritorios)
        retorno[GrupoTerritorio.Oceania] = self.densidadePorGrupoTerritorio(GrupoTerritorio.ListaOceania,
                                                                            codigosTerritorios)

        retorno = sorted(retorno.items(), key=operator.itemgetter(1), reverse=True)

        return retorno

    def temTerritorio(self, codigoTerritorio):
        for t in self.territorios:
            if t.codigo == codigoTerritorio:
                return True
        return False

    def temOsTerritorios(self, listaCodigoTerritorio):
        codigosTerritoriosDoJogador = []
        for t in self.territorios:
            codigosTerritoriosDoJogador.append(t.codigo)

        for t in listaCodigoTerritorio:
            if t not in codigosTerritoriosDoJogador:
                return False
        return True

    def adicionaTropasNoTerritorio(self, codigoTerritorio, quantidade):
        territorio = None
        for t in self.territorios:
            if t.codigo == codigoTerritorio:
                territorio = t
                break

        if territorio != None:
            territorio.quantidadeDeTropas += quantidade

        return territorio

    def removeTropasNoTerritorio(self, codigoTerritorio, quantidade):
        territorio = None
        for t in self.territorios:
            if t.codigo == codigoTerritorio:
                territorio = t
                break

        if territorio != None:
            territorio.quantidadeDeTropas -= quantidade

        return territorio

    def adicionaTerritorio(self, territorio):
        self.territorios.append(territorio)

    def removeTerritorio(self, codigoTerritorio):
        novos_territorios = []
        for t in self.territorios:
            if t.codigo != codigoTerritorio:
                novos_territorios.append(t)
        self.territorios.clear()
        self.territorios = novos_territorios

    def seuTerritorio(self, codigoTerritorio):
        for t in self.territorios:
            if t.codigo == codigoTerritorio:
                return t

        return None

    def adicionaCartaTerritorio(self, cartaTerritorio):
        self.cartasTerritorio.append(cartaTerritorio)

    def removeCartaTerritorio(self, cartaTerritorio):
        self.cartasTerritorio.remove(cartaTerritorio)

    def destruiuJogador(self, posicao):
        return posicao in self.jogadoresDestruidos


class Jogador(JSONSerializer):
    _usuario = None
    _posicaoNaSala = -1
    _socket = None
    _objetivo = None
    _territorios = []
    _cartasTerritorio = []

    def __init__(self, usuario):
        self._usuario = usuario
        self._posicaoNaSala = -1
        self._socket = None
        self._territorios = []
        self._cartasTerritorio = []

    def gruposTerritorio(self):
        retorno = []

        codigosTerritorios = []
        for terr in self._territorios:
            codigosTerritorios.append(terr.codigo)

        temAsia = True
        for terr in GrupoTerritorio.ListaAsia:
            if terr not in codigosTerritorios:
                temAsia = False
        if temAsia:
            retorno.append(GrupoTerritorio.Asia)

        temAmericaDoNorte = True
        for terr in GrupoTerritorio.ListaAmericaDoNorte:
            if terr not in codigosTerritorios:
                temAmericaDoNorte = False
        if temAmericaDoNorte:
            retorno.append(GrupoTerritorio.AmericaDoNorte)

        temEuropa = True
        for terr in GrupoTerritorio.ListaEuropa:
            if terr not in codigosTerritorios:
                temEuropa = False
        if temEuropa:
            retorno.append(GrupoTerritorio.Europa)

        temAfrica = True
        for terr in GrupoTerritorio.ListaAfrica:
            if terr not in codigosTerritorios:
                temAfrica = False
        if temAfrica:
            retorno.append(GrupoTerritorio.Africa)

        temAmericaDoSul = True
        for terr in GrupoTerritorio.ListaAmericaDoSul:
            if terr not in codigosTerritorios:
                temAmericaDoSul = False
        if temAmericaDoSul:
            retorno.append(GrupoTerritorio.AmericaDoSul)

        temOceania = True
        for terr in GrupoTerritorio.ListaOceania:
            if terr not in codigosTerritorios:
                temOceania = False
        if temOceania:
            retorno.append(GrupoTerritorio.Oceania)

        return retorno

    def temTerritorio(self, codigoTerritorio):
        for t in self._territorios:
            if t.codigo == codigoTerritorio:
                return True
        return False

    def temOsTerritorios(self, listaCodigoTerritorio):
        codigosTerritoriosDoJogador = []
        for t in self._territorios:
            codigosTerritoriosDoJogador.append(t.codigo)

        for t in listaCodigoTerritorio:
            if t not in codigosTerritoriosDoJogador:
                return False
        return True

    def adicionaTropasNoTerritorio(self, codigoTerritorio, quantidade):
        territorio = None
        for t in self._territorios:
            if t.codigo == codigoTerritorio:
                territorio = t
                break

        if territorio != None:
            territorio.quantidadeDeTropas += quantidade

        return territorio

    def removeTropasNoTerritorio(self, codigoTerritorio, quantidade):
        territorio = None
        for t in self._territorios:
            if t.codigo == codigoTerritorio:
                territorio = t
                break

        if territorio != None:
            territorio.quantidadeDeTropas -= quantidade

        return territorio

    def seuTerritorio(self, codigoTerritorio):
        for t in self._territorios:
            if t.codigo == codigoTerritorio:
                return t

        return None

    def adicionaCartaTerritorio(self, cartaTerritorio):
        self._cartasTerritorio.append(cartaTerritorio)

    def removeCartaTerritorio(self, cartaTerritorio):
        self._cartasTerritorio.remove(cartaTerritorio)

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        self._usuario = valor

    @property
    def posicaoNaSala(self):
        return self._posicaoNaSala

    @posicaoNaSala.setter
    def posicaoNaSala(self, valor):
        self._posicaoNaSala = valor

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, valor):
        self._socket = valor;

    @property
    def objetivo(self):
        return self._objetivo

    @objetivo.setter
    def objetivo(self, objetivo):
        self._objetivo = objetivo

    @property
    def territorios(self):
        return self._territorios

    @territorios.setter
    def territorios(self, codigosTerritorios):
        self._territorios = []
        for t in codigosTerritorios:
            self._territorios.append(Territorio(t))

    @property
    def cartasTerritorio(self):
        return self._cartasTerritorio
