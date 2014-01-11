pais = "teste"

# NOTE: Preencher com os dados no formato:
#   "lng1,lat1 lng2,lat2 lng3,lat3"
strs = [

]

def lastIndex(lista, item):
    lastIndexOf = -1
    for index, val in enumerate(lista):
        if val==item:
            lastIndexOf = index
            
    return lastIndexOf
    
def concatenar(str_1, str_2):
    pais_1 = str_1.split(' ')
    pais_2 = str_2.split(' ')

    result = []
    intercesao = []

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
            
            
    print "Proibidos: ", proibidos
    print str(indexInicioP1) + " - " + str(indexFimP1)
    print str(indexInicioP2) + " - " + str(indexFimP2)

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
        #print str(lng) + "," + str(lat)
        
        formatado += str(lng) + "," + str(lat) + " "

    return formatado.strip()

################################################################################

s1 = strs[0]
for i in range(1, len(strs)):
    s1 = str(concatenar(s1, strs[i])).strip()

for coord in s1.split(' '):
    print coord
