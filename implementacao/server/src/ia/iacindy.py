# -*- coding: utf-8 -*-
from .iainterface import IAInterface


class IACindy(IAInterface):
    def __init__(self, sufixo=''):
        self.usuario = 'Lucy' + sufixo

    def usuario(self):
        return self.usuario

    def processa_msg(self, jogo, msg):
        print('IACindy', self.usuario, 'processa_msg', msg)

    def turno_distribuir_tropas_globais(self, jogo, quantidade):
        pass

    def turno_distribuir_tropas_grupo_territorio(self, jogo, grupo, quantidade):
        pass

    def turno_distribuir_topas_troca_de_cartas(self, jogo, quantidade):
        pass

    def turno_troca_de_cartas(self, jogo):
        pass

    def turno_atacar(self, jogo):
        pass

    def turno_mover(self, jogo):
        pass
