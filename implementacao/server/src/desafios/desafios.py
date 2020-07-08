#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import sqlite3

from src.territorio import *


class Desafios(object):

    def __init__(self, baseDeDados='war.db'):
        random.seed()
        self.baseDeDados = baseDeDados
        self.carrega_infos()

    def carrega_infos(self):
        self.desafios_json = []
        self.orientadores_json = []
        self.desafios_em_andamento = []

        desafios_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lista_desafios.json')
        with open(desafios_path, 'r') as f:
            self.desafios_json = json.load(f)

        orientadores_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'orientadores.json')
        with open(orientadores_path, 'r') as f:
            self.orientadores_json = json.load(f)

        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()
        rows = c.execute(
            "SELECT idDesafio, nomeOrientador, apenasDoador, iniciaEm, terminaEm FROM DesafiosEmAndamento WHERE datetime('now') BETWEEN iniciaEm AND terminaEm;").fetchall()
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

    def shuffle_desafios(self, apenas_doador):
        desafios = self.desafios_json
        random.shuffle(desafios)
        if apenas_doador == 1:
            desafios = [d for d in desafios if d['xp'] > 50]

        return desafios

    def shuffle_orientadores(self):
        orientadores = self.orientadores_json
        random.shuffle(orientadores)
        return orientadores

    def em_andamento(self, usuario=None):
        self.carrega_infos()

        if len(self.desafios_em_andamento) == 0:
            return []

        if usuario:
            conn = sqlite3.connect(self.baseDeDados)
            c = conn.cursor()
            rows = c.execute(
                """
                SELECT da.idDesafio
                  FROM DesafiosEmAndamento da 
                  JOIN DesafiosConcluidos dc ON dc.idDesafio = da.idDesafio 
                  JOIN Usuarios u ON u.id = dc.idUsuario 
                 WHERE dc.data BETWEEN da.iniciaEm AND da.terminaEm AND datetime('now') BETWEEN da.iniciaEm AND da.terminaEm AND  u.nome = ?;
                """, [usuario]).fetchall()
            desafiosId = []
            for row in rows:
                desafiosId.append(row[0])
            conn.close()

            for d in self.desafios_em_andamento:
                d['concluido'] = d['desafio']['id'] in desafiosId

        return self.desafios_em_andamento

    def conclui_desafio(self, desafio, usuario):
        conn = sqlite3.connect(self.baseDeDados)
        c = conn.cursor()

        c.execute(
            "INSERT INTO DesafiosConcluidos(idUsuario, idDesafio, nomeOrientador) VALUES ( (SELECT id FROM Usuarios WHERE nome = ?), ?, ? );",
            [usuario, desafio['desafio']['id'], desafio['orientador']['name']])

        conn.commit()
        conn.close()


class FabricaDesafios(object):
    def cria(self, id):
        mapaObjetivos = {
            1: Desafio01(),
            2: Desafio02(),
            3: Desafio03(),
            4: Desafio04(),
            5: Desafio05(),
            6: Desafio06(),
            7: Desafio07(),
            8: Desafio08(),
            9: Desafio09(),
            10: Desafio10(),
            11: Desafio11(),
            12: Desafio12(),
            13: Desafio13(),
            14: Desafio14(),
            15: Desafio15(),
            16: Desafio16(),
            17: Desafio17(),
            18: Desafio18(),
            19: Desafio19(),
            20: Desafio20(),
            21: Desafio21(),
            22: Desafio22(),
            23: Desafio23(),
            24: Desafio24(),
            25: Desafio25(),
            26: Desafio26(),
            27: Desafio27(),
            28: Desafio28(),
            29: Desafio29(),
            30: Desafio30(),
            31: Desafio31(),
            32: Desafio32(),
        }

        return mapaObjetivos[id]


# @interface
class Desafio(object):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        return False


# Vença uma partida jogando contra pelo menos 3 computadores.
class Desafio01(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            if usuario == jogo.jogadorVencedor:
                if len(jogo.cpus) >= 3:
                    return True
        return False


# Vença uma partida jogando contra pelo menos 4 computadores.
class Desafio02(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            if usuario == jogo.jogadorVencedor:
                if len(jogo.cpus) >= 4:
                    return True
        return False


# Vença uma partida jogando contra 5 computadores.
class Desafio03(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            if usuario == jogo.jogadorVencedor:
                if len(jogo.cpus) == 5:
                    return True
        return False


# Vença uma partida destruindo pelo menos 2 outros jogadores.
class Desafio04(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for k, usuarios in quemDestruiuQuem.items():
                if k == usuario:
                    return len(usuarios) >= 2
        return False


# Vença uma partida destruindo pelo menos 3 outros jogadores.
class Desafio05(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for k, usuarios in quemDestruiuQuem.items():
                if k == usuario:
                    return len(usuarios) >= 3
        return False


# Vença uma partida destruindo pelo menos 4 outros jogadores.
class Desafio06(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for k, usuarios in quemDestruiuQuem.items():
                if k == usuario:
                    return len(usuarios) >= 4
        return False


# Vença uma partida com pelo menos 20 territórios conquistados.
class Desafio07(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.territorios) >= 20
        return False


# Vença uma partida com pelo menos 24 territórios conquistados.
class Desafio08(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.territorios) >= 24
        return False


# Vença uma partida com pelo menos 28 territórios conquistados.
class Desafio09(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.territorios) >= 28
        return False


# Vença uma partida com pelo menos 60 tropas em um território.
class Desafio10(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    maior_quantidade = 0
                    for t in jogador.territorios:
                        if t.quantidadeDeTropas > maior_quantidade:
                            maior_quantidade = t.quantidadeDeTropas
                    return maior_quantidade >= 60
        return False


# Vença uma partida com pelo menos 120 tropas em um território.
class Desafio11(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    maior_quantidade = 0
                    for t in jogador.territorios:
                        if t.quantidadeDeTropas > maior_quantidade:
                            maior_quantidade = t.quantidadeDeTropas
                    return maior_quantidade >= 120
        return False


# Vença uma partida com pelo menos 180 tropas em um território.
class Desafio12(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    maior_quantidade = 0
                    for t in jogador.territorios:
                        if t.quantidadeDeTropas > maior_quantidade:
                            maior_quantidade = t.quantidadeDeTropas
                    return maior_quantidade >= 180
        return False


# Vença uma partida com pelo menos 1 continente.
class Desafio13(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.gruposTerritorio()) >= 1
        return False


# Vença uma partida com pelo menos 2 continentes.
class Desafio14(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.gruposTerritorio()) >= 2
        return False


# Vença uma partida com pelo menos 3 continentes.
class Desafio15(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    return len(jogador.gruposTerritorio()) >= 3
        return False


# Vença uma partida com o continente Am. do Sul conquistado.
class Desafio16(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.AmericaDoSul in jogador.gruposTerritorio()
        return False


# Vença uma partida com o continente África conquistado.
class Desafio17(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.Africa in jogador.gruposTerritorio()
        return False


# Vença uma partida com o continente Oceania conquistado.
class Desafio18(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.Oceania in jogador.gruposTerritorio()
        return False


# Vença uma partida com o continente Am. do Norte conquistado.
class Desafio19(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.AmericaDoNorte in jogador.gruposTerritorio()
        return False


# Vença uma partida com o continente Europa conquistado.
class Desafio20(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.Europa in jogador.gruposTerritorio()
        return False


# Vença uma partida com o continente Ásia conquistado.
class Desafio21(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for posicao, jogador in jogo.jogadores.items():
                if jogador.usuario == usuario:
                    return GrupoTerritorio.Asia in jogador.gruposTerritorio()
        return False


# Termine 1 partida sem ser destruído.
class Desafio22(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        return not jogo.usuarioFoiDestruidoPorAlguem(usuario, quemDestruiuQuem)


# Vença uma partida destruindo o jogador {usuario}.
# {
#   "id": 23,
#   "name": "",
#   "description": "Vença uma partida destruindo o jogador {usuario}.",
#   "xp": 150
# },
class Desafio23(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        #         if venceu:
        #             return jogo.usuarioDestruiOutroUsuario(usuario, 'alvo', quemDestruiuQuem)
        return False


# Vença uma partida em até 30 turnos.
class Desafio24(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            return jogo.turno.numero <= 30
        return False


# Vença uma partida em até 20 turnos.
class Desafio25(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            return jogo.turno.numero <= 20
        return False


# Vença uma partida em até 10 turnos.
class Desafio26(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            return jogo.turno.numero <= 10
        return False


# Vença uma partida com pelo menos 50 tropas em Moscou.
class Desafio27(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.Moscou and t.quantidadeDeTropas >= 50:
                            return True
        return False


# Vença uma partida com pelo menos 100 tropas em Moscou.
class Desafio28(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.Moscou and t.quantidadeDeTropas >= 100:
                            return True
        return False


# Vença uma partida com pelo menos 150 tropas em Moscou.
class Desafio29(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.Moscou and t.quantidadeDeTropas >= 150:
                            return True
        return False


# Vença uma partida com pelo menos 50 tropas no Oriente Médio.
class Desafio30(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.OrienteMedio and t.quantidadeDeTropas >= 50:
                            return True
        return False


# Vença uma partida com pelo menos 100 tropas no Oriente Médio.
class Desafio31(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.OrienteMedio and t.quantidadeDeTropas >= 100:
                            return True
        return False


# Vença uma partida com pelo menos 150 tropas no Oriente Médio.
class Desafio32(Desafio):
    def completou(self, jogo, usuario, venceu, quemDestruiuQuem):
        if venceu:
            for jogador in jogo.jogadores.values():
                if jogador.usuario == usuario:
                    for t in jogador.territorios:
                        if t.codigo == CodigoTerritorio.OrienteMedio and t.quantidadeDeTropas >= 150:
                            return True
        return False
