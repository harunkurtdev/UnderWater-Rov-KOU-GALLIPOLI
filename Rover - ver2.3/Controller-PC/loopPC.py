from pygameJoystick import pyGameJoystick
from roboSocketCom import RoboSocketCom
from jsonController import jsonController
from webSocketsOpencvServer import WebSocketsOpencvServer
import json,pygame,time,asyncio,websockets,threading


def SocketsOpencv(ipAdress,port):
    WebSocketsOpencvServer(serverHost=ipAdress,serverPort=port)

if __name__ == '__main__':
    try:
        socketsOpencv =threading.Thread(target=SocketsOpencv,args=("0.0.0.0",5001,))
        socketsOpencv.run()
    except threading.ThreadError as exp:
        print("WebSocketsOpencvServer Thread ta bir sorun ile karşılaşıldı...",exp)
    try:
        pygame.init()
        joystcik = pyGameJoystick(pyGame=pygame)
    except Exception as exp:
        print("joytcik veya pygame başlatılırken bir sorun çıktı sorun... : ", exp)
    try:
        roboSocketCom = RoboSocketCom(clientHost="172.19.96.227", clientPort=5000)
    except Exception as exp:
        print("RoboSocketCom sunucuya bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

    try:
        json_Controller = jsonController(joyStick=joystcik, roboSocketCom=roboSocketCom)
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

