from roboSocketCom import RoboSocketCom
from websocket import create_connection
from jsonController import jsonController
from pygameJoystick import pyGameJoystick
from shapeDetectionClass import ShapeDetection

import pygame,base64,cv2
import numpy as np


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

def connectJsonControl(url,port,sendMessage):
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send(sendMessage)
    message = ws.recv()
    ws.close()
    return message


def mainLoop():
    pygame.init()
    try:
        joystcik = pyGameJoystick(pyGame=pygame)
    except Exception as exp:
        print("joytcik başlatılırken bir sorun çıktı sorun... : ", exp)
    try:
        roboSocketCom = RoboSocketCom(clientHost="127.0.0.1", clientPort=5000)
        # roboSocketCom=RoboSocketCom(clientHost="172.19.96.191",clientPort=65432)
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

    try:
        json_Controller = jsonController(joyStick=joystcik, roboSocketCom=roboSocketCom)
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)
    consol=False
    while True:
        try:
            img=connect("127.0.0.1",5001)
            arm=connect("127.0.0.1",5002)
            display_stabilize=connect("127.0.0.1",5003)

            if (cv2.waitKey(1) &0xFF==ord("c")) or (consol==True):
                consol=True
                axis,buttons=json_Controller.controlJsonWrite()
                mesage=connectJsonControl(url="127.0.0.1",port=5000,sendMessage=axis)
                print(mesage)
            if (cv2.waitKey(1) &0xFF==ord("x")) or (consol==False) :
                print(consol)
                # cv2.imshow("Resim", img)
                img = img
                frame = img.copy()
                shape.imgRead(img=img, imgContour=frame)
                consol=False

            if consol==True:
                imgStack = stackImages(0.6, ([img,img],
                                             [display_stabilize, arm]))
            else:
                imgStack = stackImages(0.4, ([frame,img],
                                             [display_stabilize,arm]))

            cv2.imshow("Gorev Ekrani", imgStack)

            if cv2.waitKey(20) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
                break
        except Exception as exp:
            print("json_Controllerinde bir hata yakalandı : ", exp)


if __name__ == '__main__':
    shape = ShapeDetection()
    mainLoop()
    pass