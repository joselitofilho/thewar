from territorio import *

class CartaForma:
    Bola = "Bola"
    Quadrado = "Quadrado"
    Triangulo = "Triangulo"
    Todas = "Todas"

class CartaCor:
    Azul = "Azul"
    Amarela = "Amarela"
    Vermelha = "Vermelha"
    Todas = "Todas"

class CartasTerritorio(object):
    Coringa = "Coringa"

    @staticmethod
    def Todas():
        todas = []
        # America do Sul
        todas.append(CartaTerritorio(CodigoTerritorio.Argentina, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Brasil, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Chile, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Colombia, CartaForma.Triangulo, CartaCor.Vermelha))

        # America do Norte
        todas.append(CartaTerritorio(CodigoTerritorio.Alaska, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.California, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Groelandia, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Labrador, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Mackenzie, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Mexico, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.NovaYork, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Ottawa, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Vancouver, CartaForma.Triangulo, CartaCor.Vermelha))

        # Europa
        todas.append(CartaTerritorio(CodigoTerritorio.Alemanha, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Inglaterra, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Islandia, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Moscou, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Polonia, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Portugal, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Suecia, CartaForma.Bola, CartaCor.Azul))

        # Africa
        todas.append(CartaTerritorio(CodigoTerritorio.AfricaDoSul, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Argelia, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Congo, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Egito, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Madagascar, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Sudao, CartaForma.Quadrado, CartaCor.Amarela))

        # Asia
        todas.append(CartaTerritorio(CodigoTerritorio.Aral, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.China, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Dudinka, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.India, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Mongolia, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Japao, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Omsk, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.OrienteMedio, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.Siberia, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Tchita, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Vietna, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Vladivostok, CartaForma.Bola, CartaCor.Azul))
        
        # Oceania
        todas.append(CartaTerritorio(CodigoTerritorio.Australia, CartaForma.Triangulo, CartaCor.Vermelha))
        todas.append(CartaTerritorio(CodigoTerritorio.Borneo, CartaForma.Quadrado, CartaCor.Amarela))
        todas.append(CartaTerritorio(CodigoTerritorio.NovaGuine, CartaForma.Bola, CartaCor.Azul))
        todas.append(CartaTerritorio(CodigoTerritorio.Sumatra, CartaForma.Quadrado, CartaCor.Amarela))
        
        # 2 cartas Coringa
        todas.append(CartaTerritorio(CartasTerritorio.Coringa, CartaForma.Todas, CartaCor.Todas))
        todas.append(CartaTerritorio(CartasTerritorio.Coringa, CartaForma.Todas, CartaCor.Todas))

        return todas

class CartaTerritorio(object):
    def __init__(self, codigoTerritorio, forma, cor):
        self.codigoTerritorio = codigoTerritorio
        self.forma = forma
        self.cor = cor
