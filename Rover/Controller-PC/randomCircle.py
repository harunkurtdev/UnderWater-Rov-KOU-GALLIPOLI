import websockets,asyncio,time,json,cv2,base64
import numpy as np
from shapeDetectionClass import ShapeDetection
from websocket import create_connection

async def startRoboServerConnect( clientHost=None, clientPort=None, sendMessage=None):
    global distanceData
    async with websockets.connect(
            "ws://" + str(clientHost) + ":" + str(clientPort)) as roboClientWebSocket:
        try:
            print(sendMessage)
            roboClientWebSocket = roboClientWebSocket
            # sendMessage=json.dumps(sendMessage)
            await roboClientWebSocket.send(str(sendMessage).encode("utf-8"))
            print(sendMessage)
            "server dan gelen veriyi dinleme işlemi"
            distanceData=await roboClientWebSocket.recv()
        except Exception as hata:
            print("startRoboServerConnect bölümünde veriler iletilirken bir hata ile karışılaşıldı hata kodu : ",
                  hata)


def connect(url,port):
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def main():
    global  data
    true1=False
    true2=False
    true3=False
    true4=True
    eskizaman=time.time()

    ileri=1
    saga=3
    sola=2
    cap = cv2.VideoCapture(0)  ##change this later to the name of the video
    while True:
        direction = 0
        yState1 = False
        yState2 = False

        # ret,img=cap.read()
        img = connect(ip, 5002)
        # arm=connect(ip,5001)
        # display_stabilize=connect(ip,5003)

        # asyncio.get_event_loop().run_until_complete(startRoboServerConnect(clientHost=ip,clientPort=5000,sendMessage=data))
        # distanceData=connectJsonControl(url=ip, port=5000, sendMessage=data.enc)
        # print(distanceData)
        # if distanceData!=None and distanceData!="{}" and distanceData!="":
        #     # distanceData=json.dumps(distanceData)
        #     distanceData=json.loads(distanceData)
        #     print(distanceData)
        # rovDistance=rov_distance_paint.mainDistance(int(distanceData["distanceFront"]),(distanceData["distanceDown"]),distanceData["distanceRight"],distanceData["distanceLeft"])
        # cv2.imshow("asaa",rovDistance)
        img = img
        frame = img.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # --------
        # define range of blue color in HSV
        # lower_blue = np.array([110,50,50])
        lower_blue = np.array([99,237,131])#Sualtın da ki nesne
        # lower_blue = np.array([91, 237, 131])  # Sualtında ki Çember #--------
        # lower_blue = np.array([91, 159, 255])  # Sualtında ki Çember
        # upper_blue = np.array([130,255,255])
        upper_blue = np.array([180, 251, 255])  # Sualtında ki nesne
        # upper_blue = np.array([112, 255, 255])  # Sualtında ki Çember
        # upper_blue = np.array([112, 255, 255])  # Sualtında ki Çember#--------
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)  # --------
        # Bitwise-AND mask and original image
        kernel = np.ones((5, 5), np.uint8)  # --------
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # --------
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # mask=cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel1)
        # kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.erode(img, kernel, iterations=1)
        # resimGray = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
        res = cv2.bitwise_and(frame, frame, mask=mask)  # --------

        # resim=cv2.threshold(hsv,100,255,cv2.THRESH_BINARY)
        # cv2.imshow('res', frame)
        # cv2.imshow('mask', img)
        # print(mask.shape)
        # print(frame.shape)
        # cv2.imshow('mask', resimGray)
        h, w, _ = img.shape
        h = int(h / 2)
        w = int(w / 2)
        # cv2.imshow("res resimi",img)
        shapeCircle, Circles = shape.imgRead(img=res, imgContour=frame)
        cv2.imshow('res', frame)
        object = False
        x, y = 0, 0
        for cX, cY in shapeCircle:
            print(f"sekil dairenin X ekseni {cX} y ekseni {cY}")
            # for dX, dY in Circles:
            #     print(f"Dairenin X ekseni {dX} y ekseni {dY}")
            #     if (abs(cX - dX) < 50) or (abs(dY - cY) < 50):
            #         print("daire bulundu")
            #         x = int((cX + dX) / 2)
            #         y = int((dX + cY) / 2)
            #         dataObject = {
            #             "sekilX": cX,
            #             "sekilY": cY,
            #             "daireX": dX,
            #             "daireY": dY
            #         }
            #         object = True
            #
            x = cX
            y = cY
            object = True
            # print(dataObject)

        if object == True:
            # print(data)
            if abs(w - x) <= 75 and abs(h - y) <= 75:
                print("5. Durum araç x - y ekseninde sabit kalarak ileri doğru gidiyor")
                # data["frontSpeed"] = True
                center = True
                direction=ileri
            else:
                center = False

            # if abs(w-x)<=50 and h>=y and center==False:
            #     print("2. Durum X ekseninde sabit kalıp yukarı doğru çıkıyor")
            #     # data["robot_arm_y_positive"] = 1
            #     # data["robot_arm_z_positive"] = 1
            #     yState1 = True
            # else:
            #     yState1 = False

            if abs(h - y) <= 50 and w >= x and center == False:
                print("4. Durum y ekseninde sabit kalıp- x ekseninde sola doğru gidiyor")
                # data["goLeftSpeed"] = True
                # data["goRightSpeed"] = False
                xState1 = True
                direction=sola
            else:
                xState1 = False

            if abs(h - y) <= 50 and x >= w and center == False:
                print("6. Durum y ekseninde sabit kalıp- x ekseninde sağa doğru gidiyor")
                # data["goRightSpeed"] = True
                # data["goLeftSpeed"] = False
                xState2 = True
                direction=saga
            else:
                xState2 = False

            # if  abs(w-x)<=50 and y>=h and center==False:
            #     print("8. Durum X ekseninde sabit kalıp yukarı doğru çıkıyor")
            #     # data["robot_arm_y_negative"] = 1
            #     # data["robot_arm_z_negative"] = 1
            #     yState2 = True
            # else:
            #     yState2 = False

            if w >= x and h >= y and center == False and yState1 == False and xState1 == False:
                print("1. Durum x ekseninde sola doğru - y ekseninde yukarı doğru çıkıyor")
                # data["robot_arm_y_positive"]=1
                # data["robot_arm_z_positive"]=1
                # data["robotHeightPositive"] = True
                # data["goLeftSpeed"] = True
                direction=sola

            if x >= w and h >= y and center == False and xState2 == False and yState1 == False:
                print("3. Durum x ekseninde sağa doğru dönüyor - y ekseninde yukarı doğru çıkıyor")
                # data["robot_arm_y_positive"] = 1
                # data["robot_arm_z_positive"] = 1
                # data["robotHeightSpeed"] = True
                # data["goRightSpeed"] = True
                direction=saga

            if w >= x and y >= h and center == False and xState1 == False and yState2 == False:
                print("7. Durum X ekseninde sola doğru dönüyor - y ekseninde aşağı doğru iniyor")
                # data["robot_arm_y_negative"] = 1
                # data["robot_arm_z_negative"] = 1
                # data["robotHeightNegative"] = True
                # data["goLeftSpeed"] = True
                direction=sola
            if x >= w and y >= h and center == False and xState2 == False and yState2 == False:
                print("9. Durum X ekseninde sağa doğru dönüyor - y ekseninde aşağı doğru iniyor")
                # data["robot_arm_y_negative"] = 1
                # data["robot_arm_z_negative"] = 1
                # data["robotHeightNegative"] = True
                # data["goRightSpeed"] = True
                direction=saga
        else:
            "2 metre ileri"
            # print(time.time(),eskizaman)
            # print(true1,true2,true3,true4)
            if time.time()-eskizaman>=15 and true4==True:

                eskizaman=time.time()
                true1=True
                true4 =False
            elif true4==True:

                direction=ileri

            if time.time() - eskizaman >= 15 and true1==True:
                true2=True
                true4=False
                true1=False
                eskizaman=time.time()
            elif true1==True:
                direction=saga

            if time.time() - eskizaman >= 2 and true2==True:
                true3 = True
                true2=False
                eskizaman = time.time()
            # time.sleep(4)
            elif true2==True:
                direction=sola

            if time.time() - eskizaman >= 30 and true3==True:
                true4=True
                true3=False
                eskizaman = time.time()
            elif true3 == True:
                direction=ileri
        asyncio.get_event_loop().run_until_complete(
            startRoboServerConnect(clientHost=ip, clientPort=5000, sendMessage=direction))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            print("bitti")
            break

if __name__ == '__main__':
    ip="192.168.1.42"
    # ip="127.0.0.1"
    shape = ShapeDetection()
    main()