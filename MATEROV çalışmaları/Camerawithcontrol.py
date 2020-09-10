import cv2
import threading
import pygame
from DriveClass import Drive
import serial
#Create a class so that multiple video displays can run together
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(3,1920)
    cam.set(4,1080)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads of camera display and intialize all necessary variables
size = [1,1]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
thread1 = camThread("Camera 1", 3)
thread2 = camThread("Camera 2", 2)
thread1.start()
thread2.start()
rollspeed = 0.75
t = Drive()
#ser = serial.Serial("COM3", baudrate=9600,  timeout=0)
#serB = serial.Serial("/dev/ttyUSB1", baudrate=9600,  timeout=0)
done = False
pilotInput = [0 for i in range(0,6)]
t.updatecoefficents()
while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done=True 
    #Take in input from the controller and adjust motor speeds accordingly
    pilotInput[0] = joystick.get_axis(0)
    pilotInput[1] = -1.0 * joystick.get_axis(1)
    pilotInput[2] = -1.0 * joystick.get_axis(2) #Right is up
    pilotInput[3] = joystick.get_axis(3)
    #pilotInput[4] = -1.0 * joystick.get_axis(4)
    pilotInput[5] = joystick.get_hat(0)[0] * rollspeed
    for i in range(0,6):
        if(abs(pilotInput[i]) < 0.2):
           pilotInput[i] = 0
    motorv = t.getsolution(pilotInput)
    motorvs = ""
    for i in range(0,5):
        motorvs += str(motorv[i]) + ","
    motorvs += str(motorv[5]) + ";"
    #ser.write(motorvs.encode("utf-8"))
    #temp = str(motorv[4]) + "," + str(motorv[5]) + ";"
    #serB.write(temp.encode("utf-8"))
    print(motorvs)
    #print(serB.readline())
    #pygame.display.flip()
    clock.tick(5)
pygame.quit()
