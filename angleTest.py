import math

def getDistanceByCoordinates(latI,longI,latF,longF):
    earthRadius = 3958.75
    latDiff = math.radians(latF-latI)
    lngDiff = math.radians(longF-longI)
    a = math.sin(latDiff /2) * math.sin(latDiff /2) + math.cos(math.radians(latI)) * math.cos(math.radians(latF)) * math.sin(lngDiff /2) * math.sin(lngDiff /2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earthRadius * c

    meterConversion = 1609

    distance = distance * meterConversion
    print "Distancia: ",distance

    return distance

def getDestinoDirection(latI,longI,latA,longA,latF,longF):
    return ( longF - longI ) * ( latA - latI ) - ( latF - latI ) * ( longA - longI )

def getCoefAng(latI,longI,latF,longF):
    if (longI==longF):
        longF = longF + 0.000001
    return ( ( latF - latI ) / ( longF - longI ) )

def getAngle(latI,longI,latA,longA,latF,longF):
    
    print "Inicio: ",latI,", ",longI
    print "Atual: ",latA,", ",longA
    print "Destino: ",latF,", ",longF

    direction = getDestinoDirection(latI,longI,latA,longA,latF,longF)

    sentido = True #Direita = True / Esquerda = False
    if (direction == 0):
    	return 0
    elif (direction < 0):
    	sentido = False
		
    coefAngI = getCoefAng(latI, longI, latA, longA)
    print "Coeficiente da Inicial: ",coefAngI
    coefAngF = getCoefAng(latA, longA, latF, longF)
    print "Coeficiente da Final: ",coefAngF

    tangAngulo = ( ( coefAngI - coefAngF ) / ( 1 + ( coefAngI * coefAngF ) ) )
    print "Tangente do Angulo: ",tangAngulo

    if(tangAngulo < 0):
        tangAngulo = tangAngulo*(-1)

    angulo = math.degrees(math.atan(tangAngulo))

    #se o ponto de destino for mais perto do inicial que do atual
	#usar complemento do angulo em 180
    distFim = getDistanceByCoordinates(latI,longI,latF,longF)
    distAtual = getDistanceByCoordinates(latA,longA,latF,longF)
	
    if(distFim < distAtual):
		angulo = 180-angulo
	
    if(angulo>170):
        print "Angulo corrigido de ",angulo," para 170 por limitacao da biblioteca"
        angulo = 170 #limitacao de biblioteca descrita na documentacao

    if((sentido==False)and(angulo>0)):
        angulo = angulo*(-1)

    print "Angulo de curvatura: ",angulo

    return angulo


def main():

    #LAT-LONG -> esquerda
    getAngle(-12.893271, -38.457557,-12.893344, -38.457495,-12.892784, -38.457510)
    #LAT-LONG -> direita
    #getAngle(-12.893360, -38.457702,-12.893344, -38.457495,-12.893924, -38.457470)
    #LONG-LAT -> esquerda
    #getAngle(-38.458396,-12.893347, -38.457495,-12.893344, -38.457510,-12.892784)
    #LONG-LAT -> direita
    #getAngle(-38.458396,-12.893347, -38.457495,-12.893344, -38.457470,-12.893924)
    
    #y-x -> esquerda _ -135 _ -135
    #getAngle(-1,-1,1,1,1,-1)
    #y-x -> direta _ 45 _ 45
    #getAngle(-1,-1,1,1,1,2)
    #x-y -> esquerda _ 135 _ 135
    #getAngle(-1,-1,1,1,-1,1)
    #x-y -> direta _ -45 _ -45
    #getAngle(-1,-1,1,1,2,1)
    
if __name__ == "__main__": main()
