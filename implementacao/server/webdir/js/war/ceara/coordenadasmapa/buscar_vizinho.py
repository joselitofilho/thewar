# -*- coding: utf-8 -*-
import xml.dom.minidom

def lerTerritorios(territorio):
    linhasDoArquivo = []
    f = open('Municipios_CE.kml')
    for linha in f:
        linhasDoArquivo.append(linha.rstrip())
    f.close()  

    xmldoc = xml.dom.minidom.parse('Municipios_CE.kml')

    placemarkerList = xmldoc.getElementsByTagName('Placemark')
    for placemarker in placemarkerList:
        filhos = [no for no in placemarker.childNodes if no.nodeType == xmldoc.ELEMENT_NODE]
        
        if filhos[0].firstChild:
            nome = filhos[0].firstChild.nodeValue
            if nome == territorio:
                coord = str(filhos[1].firstChild.nodeValue).replace('\n', '')
                break
    
    linhas = []
    for c in coord.split(' '):
        for i in range(len(linhasDoArquivo)):
            if c in linhasDoArquivo[i] and i+1 not in linhas:
                linhas.append(i+1)
                
    print linhas
        
        
lerTerritorios("Pereiro")
