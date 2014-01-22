# -*- coding: utf-8 -*-
import xml.dom.minidom
import os.path

################################################################################

def lerTerritorios(territorios):
    poligonos = {}
    xmldoc = xml.dom.minidom.parse('Municipios_CE.kml')

    placemarkerList = xmldoc.getElementsByTagName('Placemark')
    for placemarker in placemarkerList:
        filhos = [no for no in placemarker.childNodes if no.nodeType == xmldoc.ELEMENT_NODE]
        
        if filhos[0].firstChild:
            nome = filhos[0].firstChild.nodeValue
            if nome in territorios:
                coord = str(filhos[1].firstChild.nodeValue).replace('\n', '')
                poligonos[nome] = coord
                
    return poligonos

################################################################################

def lastIndex(lista, item):
    lastIndexOf = -1
    for index, val in enumerate(lista):
        if val==item:
            lastIndexOf = index
            
    return lastIndexOf
    
def concatenar(str_1, str_2):
    pais_1 = str_1.split(' ')
    pais_2 = str_2.split(' ')

    estaEmIntersecao = False
    primeiraIntersecao = False
    p1UltimaIntersecao = None
            
    # Identificando posicoes que teem intersecao.
    proibidos = []
    for p1 in pais_1:
        if p1 not in pais_2:
            if estaEmIntersecao == True:
               estaEmIntersecao = False
               
               pos2 = pais_2.index(p1UltimaIntersecao)
               indexFimP1 = pais_1.index(p1UltimaIntersecao)
               indexInicioP2 = pos2
        else:
            if primeiraIntersecao == False:
                estaEmIntersecao = True
                primeiraIntersecao = True
                
                pos2 = lastIndex(pais_2, p1)
                indexInicioP1 = pais_1.index(p1)
                indexFimP2 = pos2
                
            p1UltimaIntersecao = p1
            proibidos.append(p1)
            
            
    #print "Proibidos: ", proibidos
    #print str(indexInicioP1) + " - " + str(indexFimP1)
    #print str(indexInicioP2) + " - " + str(indexFimP2)

    coords = []
    for i in range(0, indexInicioP1):
        if pais_1[i] not in proibidos:
            coords.append(pais_1[i])
    
    if (indexInicioP2 > indexFimP2):
        for i in range(indexFimP2, indexInicioP2):
            if pais_2[i] not in proibidos:
                coords.append(pais_2[i])
    else:
        for i in range(indexFimP2+1, len(pais_2)):
            if pais_2[i] not in proibidos:
                coords.append(pais_2[i])

        for i in range(0, indexInicioP2+1):
            if pais_2[i] not in proibidos:
                coords.append(pais_2[i])

    for i in range(indexFimP1, len(pais_1)):
        if pais_1[i] not in proibidos:
            coords.append(pais_1[i])

    formatado = ""
    for lnglat in coords:
        #lng, lat, lixo = lnglat.split(',')
        lng, lat = lnglat.split(',')
        
        formatado += str(lng) + "," + str(lat) + " "

    return formatado.strip()

################################################################################

def gerarArquivoJs(coords, nome, centro):
    coords_vetor = coords.split(' ')
    
    texto = ""
    
    texto += "var coordenada_" + nome.lower().replace(' ', '_') + " = {\n"
    texto += "    nome: \"" + nome.replace(' ', '') + "\",\n"
    texto += "    centro: new google.maps.LatLng("+centro+"),\n"
    texto += "    territorio: [\n"
    for lnglat in coords_vetor:
        lng, lat = lnglat.split(',')
        texto += "        new google.maps.LatLng(" + str(lat) + "," + str(lng) + "),\n"
    texto += "    ]\n"
    texto += "};\n"
    
    nome_arquivo = nome.lower().replace(' ', '-') + ".js"
    f = open(nome_arquivo, "w")
    f.write(texto)
    f.close()


################################################################################

territorios = {
    # Regiao 1 - Sul
    "Barro": {
        "ordem": ["Barro","Milagres","Mauriti","Abaiara","Brejo Santo","Jati","Penaforte"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Farias Brito": {
        "ordem": ["Aurora", "Caririacu", "Granjeiro", "Farias Brito", "Altaneira"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Juazeiro do Norte": {
        "ordem": ["Santana do Cariri", "Crato", "Nova Olinda", "Juazeiro do Norte", "Barbalha", "Missao Velha", "Jardim", "Porteiras"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Chapada do Araripe": {
        "ordem": ["Araripe", "Salitre", "Campos Sales", "Assare", "Potengi"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    #Regiao 2 - Sertao dos Inhamuns
    "Aiuaba": {
        "ordem": ["Aiuaba"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Parambu": {
        "ordem": ["Parambu"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Catarina": {
        "ordem": ["Arneiroz", "Catarina", "Saboeiro"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Taua": {
        "ordem": ["Taua"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Crateus": {
        "ordem": ["Crateus", "Novo Oriente", "Quiterianopolis"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Independencia": {
        "ordem": ["Independencia"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Catunda": {
        "ordem": ["Catunda"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Senador Pompeu": {
        "ordem": ["Mombaca", "Senador Pompeu"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Poranga": {
        "ordem": ["Ararenda", "Ipaporanga", "Poranga"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    # Regiao 3 - Noroeste
    "Croata": {
        "ordem": ["Sao Benedito", "Graca", "Carnaubal", "Guaraciaba do Norte", "Croata", "Ipueras"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Ibiapina": {
        "ordem": ["Ibiapina", "Ubajara"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Uruoca": {
        "ordem": ["Uruoca", "Moraujo"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Miraima": {
        "ordem": ["Santana do Acarau", "Miraima"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Sobral": {
        "ordem": ["Forquilha","Sobral", "Coreau", "Alcantaras", "Meruoca", "Massape"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Carire": {
        "ordem": ["Carire", "Groairas"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Reriutaba": {
        "ordem": ["Reriutaba"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Varjota": {
        "ordem": ["Varjota", "Pires Ferreira"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Ipu": {
        "ordem": ["Ipu"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Tejucuoca": {
        "ordem": ["Tejucuoca"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Caucaia": {
        "ordem": ["Itapipoca", "Trairi", "Paraipaba", "Paracuru", "Sao Goncalo do Amarante", "Caucaia"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Uruburetama": {
        "ordem": ["Itapaje", "Uruburetama", "Tururu", "Umirim", "Sao Luiz do Curu"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    # Regiao 4 - Norte
    "Granja": {
        "ordem": ["Granja", "Martinopoli"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Camocim": {
        "ordem": ["Chaval", "Barroquinha", "Camocim"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Jericoacoara": {
        "ordem": ["Jericoacoara", "Cruz", "Bela Cruz"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Acarau": {
        "ordem": ["Acarau", "Itarema"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    # Regiao 5 - Sertão Central
    "Pentecoste": {
        "ordem": ["Pentecoste", "Apuiares", "General Sampaio"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Paramoti": {
        "ordem": ["Paramoti"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Itatira": {
        "ordem": ["Itatira", "Madalena"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Choro": {
        "ordem": ["Choro"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Guaramiranga": {
        "ordem": ["Palmacia", "Pacoti", "Redencao", "Guaramiranga", "Mulungu", "Baturite"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Itapiuna": {
        "ordem": ["Aratuba", "Capistrano", "Itapiuna"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Quixada": {
        "ordem": ["Banabuiu", "Quixada", "Ibaretama"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    # Regiao 6 - Leste
    "Jaguaribe": {
        "ordem": ["Oros", "Pedrinhas", "Jaguaribe", "Jaguaribara"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Iracema": {
        "ordem": ["Alto Santo", "Iracema", "Potiretama", "Pereiro", "Erere"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Beberibe": {
        "ordem": ["Palhano", "Beberibe", "Fortim"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Aracati": {
        "ordem": ["Jaguaruana", "Itaicaba", "Aracati", "Icapui"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    },
    "Quixere": {
        "ordem": ["Quixere"],
        "centro": "0.0, 0.0",
        "concatenar": False,
        "sobrescreverSeExistir": True
    },
    "Morada Nova": {
        "ordem": ["Ibicuitinga", "Morada Nova"],
        "centro": "0.0, 0.0",
        "concatenar": True,
        "sobrescreverSeExistir": True
    }
}

for terriotrioAlvo in territorios.keys():
    if len(terriotrioAlvo) > 0:
        print "|", terriotrioAlvo
        sobrescreverSeExistir = territorios[terriotrioAlvo]["sobrescreverSeExistir"]
        
        nome_arquivo = terriotrioAlvo.lower().replace(' ', '-') + ".js"
        if not os.path.exists(nome_arquivo) or (os.path.exists(nome_arquivo) and sobrescreverSeExistir):
            centro = territorios[terriotrioAlvo]["centro"]
        
            # Parte 1
            ordem = territorios[terriotrioAlvo]["ordem"]
            poligonos = lerTerritorios(ordem)

            # Parte 2
            coords = poligonos[ordem[0]]
            
            if territorios[terriotrioAlvo]["concatenar"]:
                for i in range(1, len(poligonos)):
                    print "|----", ordem[i]
                    coords = str(concatenar(coords, poligonos[ordem[i]])).strip()
                #####
                saida = ""
                for c in coords.split(' '):
                    saida += c + '\n'
                arquivo_saida = open("saida/saida"+terriotrioAlvo+".txt", "w")
                arquivo_saida.write(saida)
                arquivo_saida.close()
            ###

            # Parte 3
            gerarArquivoJs(coords, terriotrioAlvo, centro)
        else:
            print "|---- Nao foi gerado."
