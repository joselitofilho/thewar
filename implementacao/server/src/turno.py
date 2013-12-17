from tipoAcaoTurno import *

class Turno(object):
    _numero = 1
    _tipoAcao = TipoAcaoTurno.distribuir_tropas_globais
    _quantidadeDeTropas = 0
    
    # Atributo utilizado para o turno: distribuir tropas para os grupos de territorios.
    _gruposTerritorio = []
    _grupoTerritorioAtual = None
    
    # Atributos utilizado para o turno: mover tropas apos conquistar territorio.
    _tropasParaMoverAposAtaque = 0
    _territoriosDoAtaqueDaConquista = []
    _territorioConquistado = None
    
    def reiniciarVariaveisExtras(self):
        _quantidadeDeTropas = 0
        _gruposTerritorio = []
    
        _tropasParaMoverAposAtaque = 0
        _territoriosDoAtaqueDaConquista = []
        _territorioConquistado = None
        
    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def tipoAcao(self):
        return self._tipoAcao
    @tipoAcao.setter
    def tipoAcao(self, tipoAcao):
        self._tipoAcao = tipoAcao
        
    @property
    def quantidadeDeTropas(self):
        return self._quantidadeDeTropas
    @quantidadeDeTropas.setter
    def quantidadeDeTropas(self, quantidadeDeTropas):
        self._quantidadeDeTropas = quantidadeDeTropas
    
    @property
    def gruposTerritorio(self):
        return self._gruposTerritorio
    @gruposTerritorio.setter
    def gruposTerritorio(self, valor):
        self._gruposTerritorio = valor

    @property
    def grupoTerritorioAtual(self):
        return self._grupoTerritorioAtual
    @grupoTerritorioAtual.setter
    def grupoTerritorioAtual(self, valor):
        self._grupoTerritorioAtual = valor
        
    @property
    def tropasParaMoverAposAtaque(self):
        return self._tropasParaMoverAposAtaque
    @tropasParaMoverAposAtaque.setter
    def tropasParaMoverAposAtaque(self, valor):
        self._tropasParaMoverAposAtaque = valor
