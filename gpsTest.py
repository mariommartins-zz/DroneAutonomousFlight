import GPSController

def main():
    gpsc = GpsController()
    gpsc.start()

    print "latitude: "+gpsc.fix.latitude
    print "longitude: "+gpsc.fix.longitude

    gpsc.stopController()

if __name__ == "__main__": main()
