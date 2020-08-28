from rovpy import rovpy

rovpy.connectrov("STABILIZE","udpin:0.0.0.0:14550") #connectrov(mode,port or udp url)

rovpy.arm()
a = 0
while(a < 1000):
	a+1
	rovpy.forward(0.5) # forward(speed) 0.5 is half speed
	''' if you can want use this commands
	rovpy.pitch(speed)
	rovpy.roll(speed):
	rovpy.throttle(speed)
	rovpy.yaw(speed)
	rovpy.forward(speed)
	rovpy.lateral(speed)
	rovpy.camerapan(speed)
	rovpy.cameratilt(speed)
	rovpy.light1level(power)
	rovpy.light2level(power)
	rovpy.videoswitch(speed)
	'''
	rovpy.disarm()