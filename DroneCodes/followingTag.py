##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                                # Import PS-Drone

drone = ps_drone.Drone()                                       # Start using drone
drone.startup()                                                # Connects to drone and starts subprocesses

drone.reset()                                                  # Sets the drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == - 1):   time.sleep(0.1)        # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])    # Gives a battery-status
drone.useDemoMode(True)                                        # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo","vision_detect"])                   # Packets, which shall be decoded
time.sleep(0.5)                                                # Give it some time to awake fully after reset

##### Mainprogram begin #####
# Setting up detection...
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
drone.setConfig("detect:detect_type", "3")                     # Enable universal detection
drone.setConfig("detect:detections_select_h", "128")           # Detect "Oriented Roundel" with front-camera
drone.setConfig("detect:detections_select_v", "0")             # No detection with ground cam
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

# Get detections
stop = False
x = 450
z = 102
moveZ = z
moveX = x;

while not stop:
	key = drone.getKey()
	if key == " ":
		if drone.NavData["demo"][0][2] and not drone.NavData["demo"][0][3]: 
			drone.takeoff()
			while drone.NavData["demo"][0][2]: time.sleep(0.1)
			drone.moveUp()
			time.sleep(4.5)
			drone.stop()
			time.sleep(1)
		else :
			drone.land() 
			stop = True
	if moveZ != z:
		if moveZ > 105:
			drone.moveForward(0.1)           # Drone flies forward...
			time.sleep(1)
			drone.stop()
			time.sleep(1)
		elif moveZ < 100:
			drone.moveBackward(0.1)          # Drone flies Backward...
			time.sleep(1)
			drone.stop()
			time.sleep(1)
		moveZ = z

	if moveX != x:

		if moveX < 400:
			drone.turnAngle(-20,1)           # Drone flies Left...
			time.sleep(1)
		elif moveX > 500:
			drone.turnAngle(20,1)           # Drone flies Right...
			time.sleep(1)
		moveX = x

    	NDC = drone.NavDataCount
	while NDC == drone.NavDataCount:   time.sleep(0.01)
	# Loop ends when key was pressed
	tagNum = drone.NavData["vision_detect"][0]                 # Number of found tags
	tagX =   drone.NavData["vision_detect"][2]                 # Horizontal position(s)
	tagY =   drone.NavData["vision_detect"][3]                 # Vertical position(s)
	tagZ =   drone.NavData["vision_detect"][6]                 # Distance(s)
	tagRot = drone.NavData["vision_detect"][7]                 # Orientation(s)

	# Show detections
	if tagNum:
		for i in range (0,tagNum):
			moveZ = tagZ[i]
			moveX = tagX[i]
			print "Tag no "+str(i)+" : X= "+str(tagX[i])+"  Y= "+str(tagY[i])+"  Dist= "+str(tagZ[i])+"  Orientation= "+str(tagRot[i])
    	else:
		moveZ = z
		moveX = x
