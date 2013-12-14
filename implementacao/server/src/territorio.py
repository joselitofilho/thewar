class CodigoTerritorio:
    AfricaDoSul = "AfricaDoSul"
    Alaska = "Alaska"
    Alemanha = "Alemanha"
    Aral = "Aral"
    Argelia = "Argelia"
    Argentina = "Argentina"
    Australia = "Australia"
    Borneo = "Borneo"
    Brasil = "Brasil"
    California = "California"
    Chile = "Chile"
    China = "China"
    Colombia = "Colombia"
    Congo = "Congo"
    Dudinka = "Dudinka"
    Egito = "Egito"
    Groelandia = "Groelandia"
    India = "India"
    Inglaterra = "Inglaterra"
    Islandia = "Islandia"
    Japao = "Japao"
    Labrador = "Labrador"
    Mackenzie = "Mackenzie"
    Madagascar = "Madagascar"
    Mongolia = "Mongolia"
    Mexico = "Mexico"
    Moscou = "Moscou"
    NovaGuine = "NovaGuine"
    NovaYork = "NovaYork"
    Omsk = "Omsk"
    OrienteMedio = "OrienteMedio"
    Ottawa = "Ottawa"
    Polonia = "Polonia"
    Portugal = "Portugal"
    Siberia = "Siberia"
    Sudao = "Sudao"
    Suecia = "Suecia"
    Sumatra = "Sumatra"
    Tchita = "Tchita"
    Vancouver = "Vancouver"
    Vietna = "Vietna"
    Vladivostok = "Vladivostok"
    
    Lista = [AfricaDoSul,Alaska,Alemanha,Aral,Argelia,Argentina,Australia,Borneo,Brasil,California,Chile,China,Colombia,Congo,Dudinka,Egito,Groelandia,India,Inglaterra,Islandia,Japao,Labrador,Mackenzie,Madagascar,Mongolia,Mexico,Moscou,NovaGuine,NovaYork,Omsk,OrienteMedio,Ottawa,Polonia,Portugal,Siberia,Sudao,Suecia,Sumatra,Tchita,Vancouver,Vietna,Vladivostok]

class GrupoTerritorio:
    Asia = "Asia"
    AmericaDoNorte = "AmericaDoNorte"
    Europa = "Europa"
    Africa = "Africa"
    AmericaDoSul = "AmericaDoSul"
    Oceania = "Oceania"

    ListaAsia = [CodigoTerritorio.Aral,CodigoTerritorio.China,CodigoTerritorio.Dudinka,CodigoTerritorio.India,CodigoTerritorio.Japao,CodigoTerritorio.Mongolia,CodigoTerritorio.Omsk,CodigoTerritorio.OrienteMedio,CodigoTerritorio.Siberia,CodigoTerritorio.Tchita,CodigoTerritorio.Vietna,CodigoTerritorio.Vladivostok]
    
    ListaAmericaDoNorte = [CodigoTerritorio.Alaska,CodigoTerritorio.California,CodigoTerritorio.Groelandia,CodigoTerritorio.Labrador,CodigoTerritorio.Mackenzie,CodigoTerritorio.Mexico,CodigoTerritorio.NovaYork,CodigoTerritorio.Ottawa,CodigoTerritorio.Vancouver]
    
    ListaEuropa = [CodigoTerritorio.Alemanha,CodigoTerritorio.Inglaterra,CodigoTerritorio.Islandia,CodigoTerritorio.Moscou,CodigoTerritorio.Polonia,CodigoTerritorio.Portugal,CodigoTerritorio.Suecia]

    ListaAfrica = [CodigoTerritorio.AfricaDoSul,CodigoTerritorio.Argelia,CodigoTerritorio.Congo,CodigoTerritorio.Egito,CodigoTerritorio.Madagascar,CodigoTerritorio.Sudao]
    
    ListaAmericaDoSul = [CodigoTerritorio.Argentina,CodigoTerritorio.Brasil,CodigoTerritorio.Chile,CodigoTerritorio.Colombia]

    ListaOceania = [CodigoTerritorio.Australia,CodigoTerritorio.Borneo,CodigoTerritorio.NovaGuine,CodigoTerritorio.Sumatra]
    
    Dicionario = {
        Asia: ListaAsia,
        AmericaDoNorte: ListaAmericaDoNorte,
        Europa: ListaEuropa,
        Africa: ListaAfrica,
        AmericaDoSul: ListaAmericaDoSul,
        Oceania: ListaOceania
    }

    BonusPorGrupo = { Asia: 7, AmericaDoNorte: 5, Europa: 5, Africa: 3, AmericaDoSul: 2, Oceania: 2}

class FronteiraTerritorio(object):
    
    Fronteiras = {
        CodigoTerritorio.Argentina: [CodigoTerritorio.Brasil, CodigoTerritorio.Chile],
        CodigoTerritorio.Brasil: [CodigoTerritorio.Argentina, CodigoTerritorio.Chile, CodigoTerritorio.Colombia, CodigoTerritorio.Argelia],
        CodigoTerritorio.Chile: [CodigoTerritorio.Argentina, CodigoTerritorio.Brasil, CodigoTerritorio.Colombia],
        CodigoTerritorio.Colombia: [CodigoTerritorio.Brasil, CodigoTerritorio.Chile, CodigoTerritorio.Mexico]
    }
    
    @staticmethod
    def TemFronteira(territorio1, territorio2):
        return territorio2 in FronteiraTerritorio.Fronteiras[territorio1]

class Territorio(object):
    codigo = None
    quantidadeDeTropas = None
    
    def __init__(self, codigo):
        self.codigo = codigo
        self.quantidadeDeTropas = 1

    @property
    def Codigo(self):
        return self.codigo
    @Codigo.setter
    def Codigo(self, codigo):
        self.codigo = codigo

    @property
    def QuantidadeDeTropas(self):
        return self.quantidadeDeTropas
    @QuantidadeDeTropas.setter
    def QuantidadeDeTropas(self, quantidadeDeTropas):
        self.quantidadeDeTropas = quantidadeDeTropas
