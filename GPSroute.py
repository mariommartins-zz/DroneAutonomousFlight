from gps import *
import time, sys
import threading
import math
import ps_drone # Import PS-Drone

class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites

def getDistanceByCoordinates(latI,longI,latF,longF):
    earthRadius = 3958.75
    latDiff = math.radians(latF-latI)
    lngDiff = math.radians(longF-longI)
    a = math.sin(latDiff /2) * math.sin(latDiff /2) + math.cos(math.radians(latI)) * math.cos(math.radians(latF)) * math.sin(lngDiff /2) * math.sin(lngDiff /2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earthRadius * c

    meterConversion = 1609

    distance = distance * meterConversion
    print "Distancia: "+distance

    return distance
#			Teste
#5570 m
#Coliseu
#-12.966275, -38.403925
#Farol de Itapua
#-12.957065, -38.353690

def getDestinoDirection(latI,longI,latA,longA,latF,longF):
    return ( longF - longI ) * ( latA - latI ) - ( latF - latI ) * ( longA - longI )

def getCoefAng(latI,longI,latF,longF):
    if (longI==longF):
        longF = longF + 0.000001
    return ( ( latF - latI ) / ( longF - longI ) )

def getAngle(latI,longI,latA,longA,latF,longF):
	
    direction = getDestinoDirection(latI,longI,latA,longA,latF,longF)

    sentido = True #Direita = True / Esquerda = False
    if (direction == 0):
    	return 0
    elif (direction < 0):
    	sentido = False
		
    coefAngI = getCoefAng(latI, longI, latA, longA)
    coefAngF = getCoefAng(latA, longA, latF, longF)
	
    tangAngulo = ( ( coefAngI - coefAngF ) / ( 1 + ( coefAngI * coefAngF ) ) )

    if(tangAngulo < 0):
        tangAngulo = tangAngulo*(-1)

    angulo = math.degrees(math.atan(tangAngulo))

    #se o ponto de destino for mais perto do inicial que o atual
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

#---------------COORDENADAS DO DESTINO----------------
#CASA
#latDest = -12.893525
#longDest = -38.459263
#IGREJINHA
#latDest = -12.901878
#longDest = -38.457580
#UFBA
latDest = -13.002755
longDest = -38.506940

if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start GPS controller
        gpsc.start()

        ##### Suggested clean drone startup sequence #####
        # start drone
        drone = ps_drone.Drone()                                       # Start using drone
        drone.startup()                                                # Connects to drone and starts subprocesses

        drone.reset()                                                  # Sets the drone's status to good (LEDs turn green when red)
        while (drone.getBattery()[0] == - 1):   time.sleep(0.1)        # Wait until the drone has done its reset
        print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])    # Gives a battery-status
        drone.useDemoMode(True)                                        # Just give me 15 basic dataset per second (is default anyway)
        drone.getNDpackage(["demo","vision_detect"])                   # Packets, which shall be decoded
        time.sleep(0.5)                                                # Give it some time to awake fully after reset

        while True:
            if ( len(gpsc.satellites) > 0 ):

                #-------LEVANTA VoO-----------------------------------------------------------
                drone.takeoff()
                print "Levantando voo..."
                while drone.NavData["demo"][0][2]: time.sleep(0.1)	#Aguarda takeoff acabar

                #-------VERIFICA SE POSIcaO INICIAL == DESTINO---------------------------------
                latAtual = gpsc.fix.latitude
                longAtual = gpsc.fix.longitude

                distancia = getDistanceByCoordinates(latAtual,longAtual,latDest,longDest)
                if distancia < 1:
                    drone.stop()
                    time.sleep(2)
                    drone.land() #Pousa
                    print "Chegou no destino"
                else:
                    #----------SE MOVE PARA AJUSTE INICIAL DE ANGULO -------------------------

                    latAnt = latAtual
                    longAnt = longAtual

                    drone.moveForward()
                    time.sleep(1)
                    drone.stop()
                    time.sleep(2)

                    latAtual = gpsc.fix.latitude
                    longAtual = gpsc.fix.longitude

                    angulo = getAngle(latAnt,longAnt,latAtual,longAtual,latDest,longDest)

                    drone.turnAngle(angulo,1,1)
                    time.sleep(4)

                    #---------INICIA LOOP PARA CORREcaO DE ROTA/VELOCIDADE ATe DESTINO
                    arrived = False
                    while not arrived:

                        latAnt = latAtual
                        longAnt = longAtual

                        latAtual = gpsc.fix.latitude
                        longAtual = gpsc.fix.longitude

                        # Calcula distancia
                        distancia = getDistanceByCoordinates(latAtual,longAtual,latDest,longDest)
                        if distancia < 1:
                            drone.stop()
                            time.sleep(2)
                            drone.land() #Pousa
                            arrived = True
                            print "Chegou no destino"
                        else:
                            # Calcula Velocidade
                            if distancia < 5:
                                drone.setSpeed(0.02)
                                print "Velocidade: 2%"

                            elif distancia < 10:
                                drone.setSpeed(0.1)
                                print "Velocidade: 10%"

                            elif distancia < 30:
                                drone.setSpeed(0.5)
                                print "Velocidade: 50%"

                            else:
                                drone.setSpeed(1)
                                print "Velocidade: 100%"

								drone.moveForward()
                            angulo = getAngle(latAnt,longAnt,latAtual,longAtual,latDest,longDest)
                            drone.turnAngle(angulo,1,1)

                            time.sleep(1)
            else:
                print "Procurando por satelites..."
            time.sleep(3)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        print "Pousando drone"
        drone.stop()
        time.sleep(4)
        drone.land() #Pousa
        #wait for the tread to finish
        gpsc.join()

    print "Done"
