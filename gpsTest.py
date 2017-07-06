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

def getCoefAng(latI,longI,latF,longF):
    if (latI==latF):
        latF = latF + 0.000001
    return ( ( longF - longI ) / ( latF - latI ) )

def getAngle(latI,longI,latA,longA,latF,longF):
                #Multiplicando por 10000 pois se notou que para distancias curtas de poucos $
                #       a variacao das cordenadas se da a partir da quarta casa decimal

    print "Inicio: ",latI,", ",longI
    print "Atual: ",latA,", ",longA
    print "Destino: ",latF,", ",longF

    coefAngI = getCoefAng(latI, longI, latA, longA)
    print "Coeficiente da Inicial: ",coefAngI
    coefAngF = getCoefAng(latA, longA, latF, longF)
    print "Coeficiente da Final: ",coefAngF

    tangAngulo = ( ( coefAngI - coefAngF ) / ( 1 + ( coefAngI * coefAngF ) ) )
    print "Tangente do Angulo: ",tangAngulo

    sentido = True #Direita = True / Esquerda = False
    if(tangAngulo < 0):
        tangAngulo = tangAngulo*(-1)
        print "vai pra esquerda"
        sentido = False

    angulo = math.degrees(math.atan(tangAngulo))

    distFim = getDistanceByCoordinates(latI,longI,latF,longF)
    distAtual = getDistanceByCoordinates(latI,longI,latA,longA)
	
    if(distFim < distAtual):
		angulo = 180-angulo
	
    if(angulo>170):
        print "Angulo corrigido de ",angulo," para 170 por limitacao da biblioteca"
        angulo = 170 #limitacao de biblioteca descrita na documentacao

    if(sentido==False):
        angulo = angulo*(-1)

    print "Angulo de curvatura: ",angulo

    return angulo


def main():

   getAngle(-12.893356, -38.458330, -12.893351, -38.457493, -12.893923, -38.457504)

if __name__ == "__main__": main()

