from src.jogador import *
from src.territorio import *


class FabricaObjetivo(object):
    def cria(self, codigo):
        mapaObjetivos = {
            0: Objetivo01(),
            1: Objetivo02(),
            2: Objetivo03(),
            3: Objetivo04(),
            4: Objetivo05(),
            5: Objetivo06(),
            # 6: Objetivo07(),  # 18 territores com 2 tropas em cada.
            6: Objetivo08(),
            7: Objetivo09(),
            8: Objetivo10(),
            9: Objetivo11(),
            10: Objetivo12(),
            11: Objetivo13(),
            12: Objetivo14(),
        }

        return mapaObjetivos[codigo]


class Objetivo(object):
    def completou(self, jogador, jogadores):
        raise NotImplementedError("Nao tem implementacao para este objetivo")


# Destruir o exercitos amarelo. Se voce for o exercito amarelo, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo01(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(5):
            venceu = True
        elif 5 in jogadores.keys():
            if jogador.posicao == 5:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[5].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Destruir o exercitos azul. Se voce for o exercito azul, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo02(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(1):
            venceu = True
        elif 1 in jogadores.keys():
            if jogador.posicao == 1:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[1].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Destruir o exercitos branco. Se voce for o exercito branco, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo03(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(4):
            venceu = True
        elif 4 in jogadores.keys():
            if jogador.posicao == 4:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[4].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Destruir o exercitos preto. Se voce for o exercito preto, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo04(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(3):
            venceu = True
        elif 3 in jogadores.keys():
            if jogador.posicao == 3:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[3].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Destruir o exercitos verde. Se voce for o exercito verde, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo05(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(2):
            venceu = True
        elif 2 in jogadores.keys():
            if jogador.posicao == 2:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[2].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Destruir o exercitos vermelho. Se voce for o exercito vermelho, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo06(Objetivo):
    def completou(self, jogador, jogadores):
        venceu = False
        if jogador.destruiuJogador(0):
            venceu = True
        elif 0 in jogadores.keys():
            if jogador.posicao == 0:
                venceu = len(jogador.territorios) >= 24
            else:
                venceu = len(jogador.territorios) >= 24 and len(jogadores[0].territorios) == 0
        else:
            venceu = len(jogador.territorios) >= 24

        return venceu


# Conquistar 18 territorios com pelo menos 2 tropas em cada.
class Objetivo07(Objetivo):
    def completou(self, jogador, jogadores):
        qtd = 0
        if len(jogador.territorios) >= 18:
            for t in jogador.territorios:
                if t.quantidadeDeTropas >= 2:
                    qtd = qtd + 1
        return qtd >= 18


# Conquistar 24 territorios a sua escolha.
class Objetivo08(Objetivo):
    def completou(self, jogador, jogadores):
        return len(jogador.territorios) >= 24


# Conquistar a Asia e a America do Sul.
class Objetivo09(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.Asia in gruposTerritorio and \
               GrupoTerritorio.AmericaDoSul in gruposTerritorio


# Conquistar a Europa, America do Sul e um terceiro continente a sua escolha.
class Objetivo10(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.Europa in gruposTerritorio and \
               GrupoTerritorio.AmericaDoSul in gruposTerritorio and \
               len(gruposTerritorio) > 2


# Conquistar a Europa, Oceania e um terceiro continente a sua escolha.
class Objetivo11(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.Europa in gruposTerritorio and \
               GrupoTerritorio.Oceania in gruposTerritorio and \
               len(gruposTerritorio) > 2


# Conquistar a Asia e a Africa.
class Objetivo12(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.Asia in gruposTerritorio and \
               GrupoTerritorio.Africa in gruposTerritorio


# Conquistar a America do Norte e a Africa.
class Objetivo13(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.AmericaDoNorte in gruposTerritorio and \
               GrupoTerritorio.Africa in gruposTerritorio


# Conquistar a America do Norte e a Oceania.
class Objetivo14(Objetivo):
    def completou(self, jogador, jogadores):
        gruposTerritorio = jogador.gruposTerritorio()
        return GrupoTerritorio.AmericaDoNorte in gruposTerritorio and \
               GrupoTerritorio.Oceania in gruposTerritorio
