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
        CodigoTerritorio.Colombia: [CodigoTerritorio.Brasil, CodigoTerritorio.Chile, CodigoTerritorio.Mexico],

        CodigoTerritorio.Mexico: [CodigoTerritorio.Colombia, CodigoTerritorio.NovaYork, CodigoTerritorio.California],
        CodigoTerritorio.California: [CodigoTerritorio.Mexico, CodigoTerritorio.NovaYork, CodigoTerritorio.Vancouver, CodigoTerritorio.Ottawa],
        CodigoTerritorio.NovaYork: [CodigoTerritorio.Mexico, CodigoTerritorio.Ottawa, CodigoTerritorio.Labrador, CodigoTerritorio.California],
        CodigoTerritorio.Vancouver: [CodigoTerritorio.California, CodigoTerritorio.Ottawa, CodigoTerritorio.Alaska, CodigoTerritorio.Mackenzie],
        CodigoTerritorio.Ottawa: [CodigoTerritorio.Mackenzie, CodigoTerritorio.Vancouver, CodigoTerritorio.California, CodigoTerritorio.NovaYork, CodigoTerritorio.Labrador],
        CodigoTerritorio.Labrador: [CodigoTerritorio.Groelandia, CodigoTerritorio.Ottawa, CodigoTerritorio.NovaYork],
        CodigoTerritorio.Alaska: [CodigoTerritorio.Mackenzie, CodigoTerritorio.Vancouver, CodigoTerritorio.Vladivostok],
        CodigoTerritorio.Mackenzie: [CodigoTerritorio.Alaska, CodigoTerritorio.Vancouver, CodigoTerritorio.Ottawa, CodigoTerritorio.Groelandia],
        CodigoTerritorio.Groelandia: [CodigoTerritorio.Mackenzie, CodigoTerritorio.Labrador, CodigoTerritorio.Islandia],
        
        CodigoTerritorio.Islandia: [CodigoTerritorio.Groelandia, CodigoTerritorio.Inglaterra],
        CodigoTerritorio.Inglaterra: [CodigoTerritorio.Islandia, CodigoTerritorio.Portugal, CodigoTerritorio.Alemanha, CodigoTerritorio.Suecia],
        CodigoTerritorio.Suecia: [CodigoTerritorio.Inglaterra, CodigoTerritorio.Moscou],
        CodigoTerritorio.Moscou: [CodigoTerritorio.Suecia, CodigoTerritorio.Polonia, CodigoTerritorio.OrienteMedio, CodigoTerritorio.Aral, CodigoTerritorio.Omsk],
        CodigoTerritorio.Polonia: [CodigoTerritorio.Moscou, CodigoTerritorio.Portugal, CodigoTerritorio.OrienteMedio, CodigoTerritorio.Egito, CodigoTerritorio.Alemanha],
        CodigoTerritorio.Alemanha: [CodigoTerritorio.Portugal, CodigoTerritorio.Polonia, CodigoTerritorio.Inglaterra],
        CodigoTerritorio.Portugal: [CodigoTerritorio.Alemanha, CodigoTerritorio.Inglaterra, CodigoTerritorio.Polonia, CodigoTerritorio.Argelia, CodigoTerritorio.Egito],
        
        CodigoTerritorio.Argelia: [CodigoTerritorio.Portugal, CodigoTerritorio.Brasil, CodigoTerritorio.Congo, CodigoTerritorio.Sudao, CodigoTerritorio.Egito],
        CodigoTerritorio.Egito: [CodigoTerritorio.Argelia, CodigoTerritorio.Sudao, CodigoTerritorio.OrienteMedio, CodigoTerritorio.Polonia, CodigoTerritorio.Portugal],
        CodigoTerritorio.Sudao: [CodigoTerritorio.Egito, CodigoTerritorio.Argelia, CodigoTerritorio.Congo, CodigoTerritorio.AfricaDoSul, CodigoTerritorio.Madagascar],
        CodigoTerritorio.Congo: [CodigoTerritorio.Argelia, CodigoTerritorio.AfricaDoSul, CodigoTerritorio.Sudao],
        CodigoTerritorio.AfricaDoSul: [CodigoTerritorio.Congo, CodigoTerritorio.Sudao, CodigoTerritorio.Madagascar],
        CodigoTerritorio.Madagascar: [CodigoTerritorio.Sudao, CodigoTerritorio.AfricaDoSul],
        
        CodigoTerritorio.OrienteMedio: [CodigoTerritorio.Egito, CodigoTerritorio.Polonia, CodigoTerritorio.Moscou, CodigoTerritorio.Aral, CodigoTerritorio.India],
        CodigoTerritorio.India: [CodigoTerritorio.Sumatra, CodigoTerritorio.Vietna, CodigoTerritorio.China, CodigoTerritorio.Aral, CodigoTerritorio.OrienteMedio],
        CodigoTerritorio.Vietna: [CodigoTerritorio.Borneo, CodigoTerritorio.China, CodigoTerritorio.India],
        CodigoTerritorio.Aral: [CodigoTerritorio.Moscou, CodigoTerritorio.Omsk, CodigoTerritorio.China, CodigoTerritorio.India, CodigoTerritorio.OrienteMedio],
        CodigoTerritorio.China: [CodigoTerritorio.Vietna, CodigoTerritorio.Japao, CodigoTerritorio.Vladivostok, CodigoTerritorio.Tchita, CodigoTerritorio.Mongolia, CodigoTerritorio.Omsk, CodigoTerritorio.Aral, CodigoTerritorio.India],
        CodigoTerritorio.Japao: [CodigoTerritorio.Vladivostok, CodigoTerritorio.China],
        CodigoTerritorio.Omsk: [CodigoTerritorio.Moscou, CodigoTerritorio.Aral, CodigoTerritorio.China, CodigoTerritorio.Mongolia, CodigoTerritorio.Dudinka],
        CodigoTerritorio.Mongolia: [CodigoTerritorio.Dudinka, CodigoTerritorio.Omsk, CodigoTerritorio.China, CodigoTerritorio.Tchita],
        CodigoTerritorio.Dudinka: [CodigoTerritorio.Omsk, CodigoTerritorio.Mongolia, CodigoTerritorio.Tchita, CodigoTerritorio.Siberia],
        CodigoTerritorio.Tchita: [CodigoTerritorio.Siberia, CodigoTerritorio.Dudinka, CodigoTerritorio.Mongolia, CodigoTerritorio.Vladivostok, CodigoTerritorio.China],
        CodigoTerritorio.Siberia: [CodigoTerritorio.Dudinka, CodigoTerritorio.Tchita, CodigoTerritorio.Vladivostok],
        CodigoTerritorio.Vladivostok: [CodigoTerritorio.Siberia, CodigoTerritorio.Tchita, CodigoTerritorio.China, CodigoTerritorio.Japao, CodigoTerritorio.Alaska],
        
        CodigoTerritorio.Australia: [CodigoTerritorio.NovaGuine, CodigoTerritorio.Sumatra, CodigoTerritorio.Borneo],
        CodigoTerritorio.NovaGuine: [CodigoTerritorio.Australia, CodigoTerritorio.Borneo],
        CodigoTerritorio.Borneo: [CodigoTerritorio.NovaGuine, CodigoTerritorio.Australia, CodigoTerritorio.Vietna],
        CodigoTerritorio.Sumatra: [CodigoTerritorio.India, CodigoTerritorio.Australia]
    }
    
    @staticmethod
    def TemFronteira(territorio1, territorio2):
        return territorio2 in FronteiraTerritorio.Fronteiras[territorio1]

class Territorio(object):
    
    def __init__(self, codigo):
        self.codigo = codigo
        self.quantidadeDeTropas = 1
