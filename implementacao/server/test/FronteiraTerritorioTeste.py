from src.territorio import *
import pytest

class FronteiraTerritorioTeste:
    
    def brasilTemFronteiraComChile(self):
        assert FronteiraTerritorio.TemFronteira(CodigoTerritorio.Brasil, 
            CodigoTerritorio.Chile) == True

    def brasilNaoTemFronteiraComMexico(self):
        assert FronteiraTerritorio.TemFronteira(CodigoTerritorio.Brasil, 
            CodigoTerritorio.Mexico) == False
