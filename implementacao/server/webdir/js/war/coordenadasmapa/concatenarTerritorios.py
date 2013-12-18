pais = "teste"

str_2 = \
    "-69.77,11.7|-70.03,12.2|-70.24,11.63|-69.8,11.43|-71.5,10.96|-71.06,9.34|-71.62,9.04|-72.13,9.81|-71.58,10.71|-71.97,11.56|-71.32,11.85|-71.98,11.66|-72.49,11.12|-73.38,9.17|-72.78,9.08|-72,7.02|-70.12,6.98|-69.25,6.08|-67.45,6.19|-67.86,4.56|-67.29,3.4|-67.83,2.83|-67.19,2.39|-66.87,1.22|-65.52,0.65|-63.39,2.15|-64.05,2.48|-64.8,4.28|-62.88,3.56|-62.75,4.03|-60.99,4.52|-60.1,5.22|-60.15,4.52|-59.57,3.9|-59.99,2.69|-59.64,1.73|-58.81,1.19|-55.9,1.89|-55.97,2.53|-54.6,2.33|-54,3.45|-54.48,4.75|-54.17,5.35|-54.03,5.82|-55.13,5.82|-55.13,5.82|-56.97,6|-57.25,5.49|-57.25,5.49|-57.2,6.15|-58.31,6.89|-58.65,6.43|-58.47,7.35|-59.79,8.34|-59.79,8.34|-59.99,8.54|-59.99,8.54|-61.6,8.55|-60.85,9.44|-63.02,10.1|-62.62,10.12|-62.92,10.53|-61.88,10.73|-64.26,10.66|-63.7,10.49|-65.08,10.06|-66.24,10.64|-68.16,10.5|-68.42,11.18|-69.77,11.7"

str_1 = \
    "-71.56,12.45|-73.28,11.3|-74.16,11.33|-74.39,10.74|-74.86,11.13|-75.27,10.8|-75.63,9.45|-76.93,8.57|-76.76,7.92|-77.37,8.67|-77.22,7.94|-77.89,7.23|-77.34,6.57|-77.43,4.03|-77.03,3.92|-77.74,2.6|-78.57,2.43|-78.81,1.44|-78.59,1.24|-77.38,0.38|-75.29,-0.12|-73.56,-1.37|-72.88,-2.51|-71.7,-2.15|-70.29,-2.51|-70.72,-3.78|-69.96,-4.24|-69.38,-1.34|-70.04,0.59|-69.12,0.65|-69.84,1.07|-69.85,1.71|-67.91,1.75|-67.42,2.14|-66.87,1.22|-67.19,2.39|-67.83,2.83|-67.29,3.4|-67.86,4.56|-67.45,6.19|-69.25,6.08|-70.12,6.98|-72,7.02|-72.78,9.08|-73.38,9.17|-72.49,11.12|-71.98,11.66|-71.32,11.85|-71.56,12.45"

pais_1 = str_1.split('|')
pais_2 = str_2.split('|')

result = []
intercesao = []

estaEmIntersecao = False
primeiraIntersecao = False
p1UltimaIntersecao = None
        
# Identificando posicoes que teem intersecao.
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
            
            pos2 = pais_2.index(p1)
            indexInicioP1 = pais_1.index(p1)
            indexFimP2 = pos2
            
        p1UltimaIntersecao = p1

print str(indexInicioP1) + " - " + str(indexFimP1)
print str(indexInicioP2) + " - " + str(indexFimP2)

coords = []
for i in range(0, indexInicioP1):
    coords.append(pais_1[i])

for i in range(indexFimP2+1, len(pais_2)):
    coords.append(pais_2[i])
    
for i in range(0, indexInicioP2+1):
    coords.append(pais_2[i])
    
for i in range(indexFimP1, len(pais_1)):
    coords.append(pais_1[i])

formatado = ""
for lnglat in coords:
    #lng, lat, lixo = lnglat.split(',')
    lng, lat = lnglat.split(',')
    print str(lng) + "," + str(lat)
    
    formatado += str(lng) + "," + str(lat) + "|"

print ""
print formatado
