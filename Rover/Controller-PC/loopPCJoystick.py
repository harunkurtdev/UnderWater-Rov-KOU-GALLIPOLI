from roboSocketCom import RoboSocketCom
from websocket import create_connection
from jsonController import jsonController
from pygameJoystick import pyGameJoystick
from shapeDetectionClass import ShapeDetection

import pygame,base64,cv2,threading,json,rov_distance_paint,asyncio,jsonControllerConsole
import concurrent.futures
import numpy as np

async def futureOpencv(future,url,port):
    # while True:
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    future.set_result(img)


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
def armOpencv(url,port):
    global armImg
    ws = create_connection("ws://" + str(url) + ":" + str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    armImg = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#
img=np.zeros(([300,300,3]))
# rovDistance=np.zeros(([300,300,3]))
# arm=np.zeros(([300,300,3]))
def imgOpencv(url,port):
    global img
    ws = create_connection("ws://" + str(url) + ":" + str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

controllerMessage=""
def connectJsonControl(url,port,sendMessage):
    global controllerMessage
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send(sendMessage)
    controllerMessage = ws.recv()
    ws.close()

    return  controllerMessage

def mainLoop():
    pygame.init()
    global img
    global rovDistance
    try:
        joystcik = pyGameJoystick(pyGame=pygame)
    except Exception as exp:
        print("joytcik başlatılırken bir sorun çıktı sorun... : ", exp)
    try:
        # roboSocketCom = RoboSocketCom(clientHost=ip, clientPort=5000)
        # roboSocketCom=RoboSocketCom(clientHost="172.19.96.191",clientPort=65432)
        pass
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

    try:
        # json_Controller = jsonController(joyStick=joystcik, roboSocketCom=roboSocketCom)
        pass
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)
    consol=False
    while True:
        try:
            img=connect(ip,5001)
            arm=connect(ip,5002)
            display_stabilize=connect(ip,5003)
            data={"distanceFront": 20, "distanceDown": 0, "distanceLeft": 0, "distanceRight": 0}
            if (cv2.waitKey(1) &0xFF==ord("c")) or (consol==True):
                # consol=True
                # axis,buttons,_=json_Controller.controlJsonWrite()
                # message=connectJsonControl(url=ip,port=5000,sendMessage=axis)
                # message=json.dumps(message)
                # if message!=None and message!="{}":
                #     message=jwson.loads(message)
                rovDistance=rov_distance_paint.mainDistance(100,50,100,80)
                # print(message)
                consol = True
            # if (cv2.waitKey(1) &0xFF==ord("x")) or (consol==False) :
            #     print(consol)
            #     # cv2.imshow("Resim", img)
            #     img = img
            #     frame = img.copy()
            #     h, w, _ = img.shape
            #     h = int(h / 2)
            #     w = int(w / 2)
            #     data = None
            #     shapeCircle, Circles = shape.imgRead(img=img, imgContour=frame)
            #     object = False
            #     x, y = None, None
            #     for cX, cY in shapeCircle:
            #         # print(f"sekil dairenin X ekseni {cX} y ekseni {cY}")
            #         for dX, dY in Circles:
            #             # print(f"Dairenin X ekseni {dX} y ekseni {dY}")
            #             if (abs(cX - dX) < 50) and (abs(dY - cY) < 50):
            #                 # print("daire bulundu")
            #                 x = int((cX + dX) / 2)
            #                 y = int((dX + cY) / 2)
            #                 data = {
            #                     "sekilX": cX,
            #                     "sekilY": cY,
            #                     "daireX": dX,
            #                     "daireY": dY
            #                 }
            #                 object = True
            #                 # print(data)
            #
            #     if object == True:
            #         # print(data)
            #         if w > x and h > y:
            #             print("x ekseninde sola doğru - y ekseninde yukarı doğru çıkıyor")
            #         if x > w and h > y:
            #             print("x ekseninde sağa doğru dönüyor - y ekseninde yukarı doğru çıkıyor")
            #         if w > x and y > h:
            #             print("x ekseninde sola doğru dönüyor - y ekseninde aşağı doğru iniyor")
            #         if x > w and y > h:
            #             print("x ekseninde sağa doğru dönüyor - y ekseninde aşağı doğru iniyor")
            #     else:
            #         print("tarama ya geçiliyor")
            #
            # consol=False
            #
            # display_stabilize=np.zeros_like(img)
            # # arm=np.zeros_like(img)
            #
            #
            # if consol==True:
            #     imgStack = stackImages(0.6, ([img,arm,rovDistance]))
            # else:
            #     imgStack = stackImages(0.4, ([frame,img,arm]
            #                                 ))
            print(img)
            cv2.imshow("Gorev Ekrani", img)
            #cv2.imshow("Gorev Ekrani1", arm)
            #cv2.imshow("Gorev Ekrani2", display_stabilize)
            # cv2.imshow("Gorev Ekrani2", rovDistance)

            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
                break
        except Exception as exp:
            print("json_Controllerinde bir hata yakalandı : ", exp)

async def mainLoopAsync1():

    loop=asyncio.get_running_loop()
    futureImg=loop.create_future()
    # futureArm=loop.create_future()
    # futureDisplay=loop.create_future()
    # while True:
    loop.create_task(futureOpencv(futureImg,ip,5002))
    # loop.create_task(futureOpencv(futureArm,ip,5001))
    # loop.create_task(futureOpencv(futureDisplay,ip,5003))
    cv2.imshow("resim 1", await futureImg)
    # cv2.imshow("resim 2", await futureArm)
    # cv2.imshow("resim 3", await futureDisplay)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        print("bitti")

def threadMainLoop1():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        global armImg
        while True:
            futureArm = executor.submit(connect, ip,5001)
            # futureImg = executor.submit(connect, ip,5002)
            # futureDisplayStabilize = executor.submit(connect, ip,5003)
            # futureImg = futureImg.result()
            armImg = futureArm.result()
            # futureDisplayStabilize = futureDisplayStabilize.result()
            cv2.imshow("resim 1",armImg)
            # cv2.imshow("resim2",futureImg)
            # cv2.imshow("resim3 ",futureDisplayStabilize)
            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
            # print(return_value)

def threadMainLoop2():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        global img
        while True:
            # futureArm = executor.submit(connect, ip,5001)
            futureImg = executor.submit(connect, ip,5002)
            # futureDisplayStabilize = executor.submit(connect, ip,5003)
            img = futureImg.result()
            # futureArm = futureArm.result()
            # futureDisplayStabilize = futureDisplayStabilize.result()
            # cv2.imshow("resim 1",futureArm)
            # cv2.imshow("resim2",img)
            # cv2.imshow("resim3 ",futureDisplayStabilize)
            height, width = img.shape[:2]
            res = cv2.resize(img, (2 * width, 2 * height), interpolation=cv2.INTER_CUBIC)
            cv2.imshow("Ana kamera",res)
            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
            # print(return_value)

futureDisplayStabilize=np.zeros([300,300,3])
def threadMainLoop3():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        global  futureDisplayStabilize
        while True:

            # futureArm = executor.submit(connect, ip,5001)
            # futureImg = executor.submit(connect, ip,5002)
            futureDisplayStabilize = executor.submit(connect, ip,5003)
            # futureImg = futureImg.result()
            # futureArm = futureArm.result()
            futureDisplayStabilize = futureDisplayStabilize.result()
            height, width = futureDisplayStabilize.shape[:2]
            futureDisplayStabilize = cv2.resize(futureDisplayStabilize, (2 * width, 2 * height),
                                                interpolation=cv2.INTER_CUBIC)

            # cv2.imshow("resim 1",futureArm)
            # cv2.imshow("resim2",futureImg)
            cv2.imshow("resim3 ",futureDisplayStabilize)
            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
            # print(return_value)
if __name__ == '__main__':
    # ip="192.168.43.178"
    ip="192.168.1.42"
    # ip="127.0.0.1"
    shape = ShapeDetection()

    t1 = threading.Thread(target=threadMainLoop1)
    t1.start()
    t2 = threading.Thread(target=threadMainLoop2)
    t2.start()
    t3 = threading.Thread(target=threadMainLoop3)
    t3.start()

    while True:
        # imgStack = stackImages(0.4, ([futureDisplayStabilize,img]
        #                                 ))
        # print("veri")
        # cv2.imshow("imgStack",imgStack)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            print("bitti")
    # mainLoop()

    # while True:
    #     asyncio.run(mainLoopAsync())
    pass