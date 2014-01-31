from jogador import *
from territorio import *

class FabricaObjetivo(object):
    def cria(self, codigo):
        if codigo == 0:
            return Objetivo01()
        elif codigo == 1:
            return Objetivo02()
        elif codigo == 2:
            return Objetivo03()
        elif codigo == 3:
            return Objetivo04()
        elif codigo == 4:
            return Objetivo05()
        elif codigo == 5:
            return Objetivo06()
        elif codigo == 6:
            return Objetivo07()
        elif codigo == 7:
            return Objetivo08()
        elif codigo == 8:
            return Objetivo09()
        elif codigo == 9:
            return Objetivo10()
        elif codigo == 10:
            return Objetivo11()
        elif codigo == 11:
            return Objetivo12()
        elif codigo == 12:
            return Objetivo13()
        elif codigo == 13:
            return Objetivo14()

class Objetivo(object):
    def completou(self, jogador, jogadores):
        raise NotImplementedError("Nao tem implementacao para este objetivo")

# Destruir o exercitos amarelo. Se voce for o exercito amarelo, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo01(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 5 and 5 in jogadores.keys():
            return jogador.destruiuJogador(5)
        else:
            return len(jogador.territorios) >= 24

        return False

# Destruir o exercitos azul. Se voce for o exercito azul, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo02(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 1 and 1 in jogadores.keys():
            return jogador.destruiuJogador(1)
        else:
            return len(jogador.territorios) >= 24

        return False

# Destruir o exercitos branco. Se voce for o exercito branco, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo03(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 4 and 4 in jogadores.keys():
            return jogador.destruiuJogador(4)
        else:
            return len(jogador.territorios) >= 24

        return False

# Destruir o exercitos preto. Se voce for o exercito preto, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo04(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 3 and 3 in jogadores.keys():
            return jogador.destruiuJogador(3)
        else:
            return len(jogador.territorios) >= 24

        return False

# Destruir o exercitos verde. Se voce for o exercito verde, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo05(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 2 and 2 in jogadores.keys():
            return jogador.destruiuJogador(2)
        else:
            return len(jogador.territorios) >= 24

        return False

# Destruir o exercitos vermelho. Se voce for o exercito vermelho, entao voce
# deve conquistar 24 territorios a sua escolha.
class Objetivo06(Objetivo):
    def completou(self, jogador, jogadores):
        if jogador.posicao != 0 and 0 in jogadores.keys():
            return jogador.destruiuJogador(0)
        else:
            return len(jogador.territorios) >= 24

        return False

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
