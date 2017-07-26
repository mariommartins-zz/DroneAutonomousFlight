import time
import ps_drone                # Imports the PS-Drone-API

drone = ps_drone.Drone()       # Initializes the PS-Drone-API
drone.startup()                # Connects to the drone and starts subprocesses

print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status

drone.takeoff()                # Drone starts
time.sleep(7.5)                # Gives the drone time to start

drone.moveForward(0.25)            # Drone flies forward...
time.sleep(2)                  # ... for two seconds
drone.stop()                   # Drone stops...
time.sleep(3)                  # ... needs, like a car, time to stop

drone.turnAngle( 90,1)
time.sleep(2)
drone.turnAngle( 90,1)
time.sleep(2)

drone.moveForward(0.25)            # Drone flies forward...
time.sleep(2)                  # ... for two seconds
drone.stop()                   # Drone stops...
time.sleep(3)                  # ... needs, like a car, time to stop

drone.turnAngle( 90,1)
time.sleep(2)
drone.turnAngle( 90,1)
time.sleep(2)

drone.land()                   # Drone lands

