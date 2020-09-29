from roboSocketCom import RoboSocketCom
from websocket import create_connection
from jsonController import jsonController
from pygameJoystick import pyGameJoystick
from shapeDetectionClass import ShapeDetection

import pygame,base64,cv2,threading,json,rov_distance_paint,asyncio,websockets,time
import numpy as np

"Sensörler okumuyor random atılıyor"
import random

distanceData = {"distanceFront": 100, "distanceDown": 300, "distanceLeft": 50, "distanceRight": 100}

data={  "motor_x_axis":0.0,
        "motor_y_axis":0.0,
        "cam_x_axis":0.0,
        "cam_y_axis":0.0,
        "robot_arm_y_positive":0,
        "robot_arm_x_positive":0,
        "robot_arm_y_negative":0,
        "robot_arm_x_negative":0,
        "clock_right_motor":0,
        "robot_arm_z_positive":0,
        "clock_left_motor":0,
        "robot_arm_z_negative":0,
        "robot_stop":0,
        "robot_run":1,
        "gripper_negative":0,
        "gripper_positive":0,
        "xNumHat": 0,
        "yNumHat": 0
}

async def startRoboServerConnect( clientHost=None, clientPort=None, sendMessage=None):
    global distanceData
    async with websockets.connect(
            "ws://" + str(clientHost) + ":" + str(clientPort)) as roboClientWebSocket:
        try:
            roboClientWebSocket = roboClientWebSocket
            sendMessage=json.dumps(sendMessage)
            await roboClientWebSocket.send(sendMessage)
            "server dan gelen veriyi dinleme işlemi"
            distanceData=await roboClientWebSocket.recv()
        except Exception as hata:
            print("startRoboServerConnect bölümünde veriler iletilirken bir hata ile karışılaşıldı hata kodu : ",
                  hata)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def connect(url,port):
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img

armImg=np.zeros(([300,300,3]))

img=np.zeros(([300,300,3]))
rovDistance=np.zeros(([300,300,3]))
# arm=np.zeros(([300,300,3]))

controllerMessage=""
def connectJsonControl(url,port,sendMessage):
    global controllerMessage
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send(sendMessage)
    controllerMessage = ws.recv()
    ws.close()
    return  controllerMessage

def mainLoop():
    global data
    pygame.init()
    global img
    # global rovDistance
    global distanceData
    joystcik = pyGameJoystick(pyGame=pygame)
    json_Controller = jsonController(joyStick=joystcik)
    cap = cv2.VideoCapture(0)  ##change this later to the name of the video
    consol=False
    center = False
    while True:
        try:
            object = False
            xState1=False
            xState2=False
            yState1=False
            yState2=False

            # ret,img=cap.read()
            img=connect(ip,5002)
            # arm=connect(ip,5001)
            # display_stabilize=connect(ip,5003)

            asyncio.get_event_loop().run_until_complete(
                startRoboServerConnect(clientHost=ip, clientPort=5000, sendMessage=data))
            # distanceData=connectJsonControl(url=ip,port=5000,sendMessage=data)
            # distanceData=json.dumps(distanceData)
            if distanceData!=None and distanceData!="{}":
            #     distanceData=json.dumps(distanceData)
                distanceData=json.loads(distanceData)
            rovDistance=rov_distance_paint.mainDistance(distanceData["distanceFront"],distanceData["distanceDown"],distanceData["distanceRight"],distanceData["distanceLeft"])

            img = img
            frame = img.copy()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # define range of blue color in HSV
            # lower_blue = np.array([110,50,50])
            lower_red = np.array([0,200,180],np.uint8)#Sualtın da ki nesne
            # lower_red = np.array([0,191,0],np.uint8)#Sualtın da ki nesne
            # lower_blue = np.array([91, 159, 255])  # Sualtında ki Çember
            # upper_blue = np.array([130,255,255])
            # upper_red = np.array([15,255,255],np.uint8)#Sualtında ki nesne
            upper_red = np.array([15,255,255],np.uint8)#Sualtında ki nesne
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_red, upper_red)
            # Bitwise-AND mask and original image
            kernel = np.ones((12, 12), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # mask=cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
            # kernel = np.ones((5, 5), np.uint8)
            # mask = cv2.erode(img, kernel, iterations=1)
            #resimGray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
            res = cv2.bitwise_and(frame, frame, mask=mask)

            # kernal = np.ones((1, 1), "uint8")

            red = cv2.dilate(mask, kernel)
            res_red = cv2.bitwise_and(img, img, mask=red)
            h, w, _ = img.shape
            h = int(h / 2)
            w = int(w / 2)
            cv2.imshow("res resimi",res_red)

            cv2.circle(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)), 1,
                       (255, 0, 0), 5)
            cv2.line(frame, (int(frame.shape[1] / 2) - 50, int(frame.shape[0] / 2)),
                     (int(frame.shape[1] / 2) + 50, int(frame.shape[0] / 2)), (0, 255, 0), 1)
            cv2.line(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2) - 25),
                     (int(frame.shape[1] / 2), int(frame.shape[0] / 2) + 25), (0, 255, 0), 1)

            cv2.rectangle(frame,(int(frame.shape[1] / 2) - 75, int(frame.shape[0] / 2)),(int(frame.shape[1] / 2+75), int(frame.shape[0] / 2) -75),(0, 255, 0), 1)
            cv2.rectangle(frame,(int(frame.shape[1] / 2) - 75, int(frame.shape[0] / 2)),(int(frame.shape[1] / 2+75), int(frame.shape[0] / 2) +75),(0, 255, 0), 1)

            x, y = None, None
            for redImg,cX, cY in shape.objectDetection(red,frame):
                print(f"sekil dairenin X ekseni {cX} y ekseni {cY}")
                object = True
                frame=redImg
                x = cX
                y = cY
                print(x,y)
                # object = True
                        # print(dataObject)

            if object == True:
                # print(data)

                if abs(w-x)<=75 and abs(h-y)<=75 :
                    print("5. Durum araç x - y ekseninde sabit kalarak z ekseninde aşağı iniyor")
                    data["robot_arm_y_negative"] = 1
                    data["robot_arm_z_negative"] = 1
                    center=True
                else:
                    center=False

                if abs(w-x)<=25 and h>=y and center==False:
                    print("2. Durum X ekseninde sabit kalıp y ekseninde ileri doğru")
                    # data["robot_arm_y_positive"] = 1
                    # data["robot_arm_z_positive"] = 1
                    data["motor_y_axis"] = -0.1
                    yState1=True
                else:
                    yState1=False

                if abs(h-y)<=25 and w>=x  and center==False:
                    print("4. Durum y ekseninde sabit kalıp- x ekseninde sola doğru gidiyor")
                    data["motor_x_axis"] = -0.1
                    xState1=True
                else:
                    xState1=False

                if abs(h-y)<=25 and x>=w and center==False:
                    print("6. Durum y ekseninde sabit kalıp- x ekseninde sağa doğru gidiyor")
                    data["motor_x_axis"] = 0.1
                    xState2=True
                else:
                    xState2=False

                if  abs(w-x)<=25 and y>=h and center==False:
                    print("8. Durum X ekseninde sabit y ekseninde geri doğru gidiyor...")
                    # data["robot_arm_y_negative"] = 1
                    # data["robot_arm_z_negative"] = 1
                    data["motor_y_axis"] = 0.1
                    yState2=True
                else :
                    yState2=False

                if w >= x and h >= y and center==False and yState1==False and xState1==False:
                    print("1. Durum x ekseninde sola doğru - y ileri doğru")
                    # data["robot_arm_y_positive"]=1
                    # data["robot_arm_z_positive"]=1
                    data["motor_x_axis"] = -0.1
                    data["motor_y_axis"] = -0.1

                if x >= w and h >= y and center==False and xState2==False and yState1==False:
                    print("3. Durum x ekseninde sağa doğru gidiyor - y ekseninde ileri doğru gidiyor")
                    # data["robot_arm_y_positive"] = 1
                    # data["robot_arm_z_positive"] = 1
                    data["motor_x_axis"] = 0.1
                    data["motor_y_axis"] = -0.1

                if w >= x and y >= h and center==False and xState1==False and yState2==False:
                    print("7. Durum X ekseninde sola doğru dönüyor - y ekseninde geri doğru gidiyor")
                    # data["robot_arm_y_negative"] = 1
                    # data["robot_arm_z_negative"] = 1
                    data["motor_x_axis"] = -0.1
                    data["motor_y_axis"] = 0.1

                if x >= w and y >= h and center==False and xState2 ==False and yState2==False:
                    print("9. Durum X ekseninde sağa doğru gidiyor - y ekseninde geri doğru gidiyor ")
                    # data["robot_arm_y_negative"] = 1
                    # data["robot_arm_z_negative"] = 1
                    data["motor_y_axis"] = 0.1
                    data["motor_x_axis"] = 0.1

            else:
                leftObject=False
                rightObject=False
                turnObject=False
                # distanceFront = distanceData["distanceFront"]<=80
                # distanceLeft = distanceData["distanceLeft"]<=80
                # distanceRight = distanceData["distanceRight"]<=80
                randomFront=random.uniform(75,85)
                randomLeft=random.uniform(30,90)
                randomRight=random.uniform(30,90)
                distanceFront = randomFront<=80
                distanceLeft = randomLeft<=80
                distanceRight = randomRight<=80

                # print(distanceFront)
                if distanceFront==True:
                    if distanceData["distanceLeft"] > distanceData["distanceRight"]:
                        print("sola doğru dönüyor 33")
                        data["robot_arm_x_negative"] = 1
                    elif distanceData["distanceLeft"] < distanceData["distanceRight"]:
                        print("sağa doğru dönüyor 44")
                        data["robot_arm_x_positive"] = 1
                    else:
                        if distanceData["distanceFront"] >= 25:
                            print("sola doğru dönüyor 55")
                            data["robot_arm_x_negative"] = 1
                    #data["motor_y_axis"] = -3.0517578125e-05
                    data["robot_arm_x_negative"] = 1
                    turnObject=True
                else:
                    data["motor_y_axis"]=-0.2
                    print("ileri gidiliyor 1")


                if distanceLeft==True:
                    if distanceRight!=True:
                        print("araç sağa doğru dönüyor 2")
                        data["robot_arm_x_positive"]=1
                    else:
                        if distanceData["distanceLeft"] > distanceData["distanceRight"]:
                            print("sola doğru dönüyor 3")
                            data["robot_arm_x_negative"] = 1
                        elif distanceData["distanceLeft"] < distanceData["distanceRight"]:
                            print("sağa doğru dönüyor 4")
                            data["robot_arm_x_positive"] = 1
                        else:
                            if distanceData["distanceFront"]>=25:
                                print("sola doğru dönüyor 5")
                                data["robot_arm_x_negative"] = 1

                    # data["robot_arm_x_negative"] = 1
                    pass
                else:
                    leftObject=False
                    if distanceData["distanceFront"] >= 100 and distanceLeft==False:
                        print("araç ileri doğru gidiyor 6")
                    # data["robot_arm_x_negative"] = 1

                if distanceRight==True:
                    if distanceLeft!=True:
                        print("araç sola doğru dönüyor 7")
                    else:
                        if distanceData["distanceLeft"]>distanceData["distanceRight"]:
                            print("sola doğru dönüyor 8")
                            data["robot_arm_x_negative"] = 1
                        elif distanceData["distanceLeft"]<distanceData["distanceRight"]:
                            print("sağa doğru dönüyor 9")
                            data["robot_arm_x_positive"] = 1
                        else:
                            if distanceData["distanceFront"] > 25:
                                print("sola doğru dönüyor 10")
                                data["robot_arm_x_negative"] = 1

                    # data["robot_arm_x_positive"] = 1
                    # print("sola dönülüyor")
                else:
                    rightObject=False
                    if distanceData["distanceFront"] >= 100 and distanceRight == False:
                        print("araç ileri doğru gidiyor 7")
                    # data["robot_arm_x_positive"] = 1

                # if rightObject!= True and leftObject!=True and turnObject==True:
                #     print("sola doğru dönüyor 12")

                # data["motor_x_axis"]=-1.0
                # print(data)
            # data=json.dumps(data)
            # connectJsonControl(url=ip, port=5000, sendMessage=data)
            asyncio.get_event_loop().run_until_complete(
                startRoboServerConnect(clientHost=ip, clientPort=5000, sendMessage=data))
            time.sleep(2)
            # imgStack = stackImages(1, ([img,arm],
            #                            [rovDistance,display_stabilize]
            #                            ))
            print(data)
            # cv2.imshow("Gorev Ekrani", imgStack)
            cv2.imshow("Gorev Ekrani", frame)
            # cv2.imshow("Gorev Ekrani", res_red)
            # cv2.imshow("Gorev Ekrani1", arm)
            # cv2.imshow("Gorev Ekrani3", display_stabilize)
            # cv2.imshow("Gorev Ekrani2", rovDistance)

            data = {"motor_x_axis": 0,#3.0517578125e-05
                    "motor_y_axis": 0,#3.0517578125e-05
                    "cam_x_axis": 0.0,
                    "cam_y_axis": 0.0,
                    "robot_arm_y_positive": 0,
                    "robot_arm_x_positive": 0,
                    "robot_arm_y_negative": 0,
                    "robot_arm_x_negative": 0,
                    "clock_right_motor": 0,
                    "robot_arm_z_positive": 0,
                    "clock_left_motor": 0,
                    "robot_arm_z_negative": 0,
                    "robot_stop": 0,
                    "robot_run": 1,
                    "gripper_negative": 0,
                    "gripper_positive": 0,
                    "xNumHat": 0,
                    "yNumHat": 0
                    }
            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
                break
        except Exception as exp:
            print("json_Controllerinde bir hata yakalandı : ", exp)


if __name__ == '__main__':
    ip="192.168.1.42"
    # ip="127.0.0.1"
    shape = ShapeDetection()
    mainLoop()
    pass