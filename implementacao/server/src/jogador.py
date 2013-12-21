from territorio import *

class Jogador(object):
    _usuario = None
    _socket = None
    _objetivo = None
    _territorios = []
    _cartasTerritorio = []

    def __init__(self, usuario):
        self._usuario = usuario
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
            territorio.QuantidadeDeTropas += quantidade

        return territorio
    
    def removeTropasNoTerritorio(self, codigoTerritorio, quantidade):
        territorio = None
        for t in self._territorios:
            if t.codigo == codigoTerritorio:
                territorio = t
                break
        
        if territorio != None:
            territorio.QuantidadeDeTropas -= quantidade

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
    def socket(self):
        return self._socket

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
