import sys
sys.path.append(".")
from pygameJoystick import pyGameJoystick
#from motors_control import motor_Controller
from roboSocketCom import RoboSocketCom
import json
#import jsonpickle
import pygame
import time
import asyncio
import websockets

class jsonController:

    def __init__(self,roboSocketCom=None,joyStick=None,joystickIdName=None):
        self.roboSocketCom=roboSocketCom
        self.joystcik=joyStick
        self.joystickIdName=joystickIdName
        
        "class her seferinde çağrıldığında verilerin sıfır olarak gelmesi gerekmektedir..."
        self.data={
            "motor_x_axis":0.0,
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
            "robot_run":0,
            "gripper_negative":0,
            "gripper_positive":0,
        }

    def controlJsonRead(self):
        pass
        data=list(self.joystcik.joysctikNumAxes())
        with open("control.json","w") as jsonFile:
            for index in range(len(data)):
                print(self.joystcikAxisValueJson(self.joystcikControllerNameSwitch(id=0,index=index),data[index]))
                #jsonFile.write(self.joystcikAxisValueJson(self.joystcikControllerNameSwitch(id=0,index=index),data[index]))
                json.dump(self.joystcikAxisValueJson(self.joystcikControllerNameSwitch(id=0,index=index),data[index]),jsonFile)
            jsonFile.close()

    def controlJsonWrite(self,roboSocketCom=None,joyStick=None):
        
        """Socket bağlantılarını başlatarak ilgili aracımızın control işlemlerini
            yapmayı başlatıyoruz ve böylelikle aramız online bağlantı yaparak başlıyor...
        """

        "roboSocket boş ise veya dolu ise istenilen socketi atayalım"
        if self.roboSocketCom==None or roboSocketCom:
            self.roboSocketCom=roboSocketCom

        "joystick boş ise ya da dolu ise istenilen joystick atansın..."
        if self.joystcik==None or joyStick:
            self.joystcik=joyStick
        else :
            """
            bu bölümde pygame den gelen joystick verileri okunmakta ve aynı zamanda 
            bir list işlemine sokularak veriler atanmakta
            """
            self.joystcik.pyGame.event.get()
            dataAxis=list(self.joystcik.joysctikNumAxes())
            self.joystcik.pyGame.event.get()
            dataButton=list(self.joystcik.joysctikNumButtons())
            
            try :
                "hata oluşmaz  ise bu bölümde server a verilerimizi transfer edeceğiz"
                asyncio.get_event_loop().run_until_complete(self.roboSocketCom.startRoboServerConnect(sendMessage=self.joystcikAxisValueJson(self.joystcikControllerNameSwitch(id=0),dataAxis)))
                asyncio.get_event_loop().run_until_complete(self.roboSocketCom.startRoboServerConnect(sendMessage=self.joystcikAxisValueJson(self.joystcikControllerNameSwitch(id=1),dataButton)))
            except Exception as exp:
                print("controlJsonWrite içinde startRoboServerConnect ile veri aktalırken bir hata oluştu hata kodu : ",exp)
            
    def joystcikAxisValueJson(self,jsonKey,value):
        """ 
        bu bölümde buton ve joystickten gelen bilgiler okunmakta json bilgisine göre 
        veriler atanarak websocket bağlantısı ile karşı tarafa bilgi transferi edilmektedir...
        """
        for key in jsonKey:
            if len(value)==4:
                for index in range(len(value)):
                    if (key=="motor_x_axis") and (index==0):
                        self.data[key]=value[index]
                    elif (key=="motor_y_axis") and (index==1):
                        self.data[key]=value[index]
                    elif (key=="cam_x_axis") and (index==2):
                        self.data[key]=value[index]
                    elif (key=="cam_y_axis") and (index==3):
                        self.data[key]=value[index]
            else :
                for index in range(len(value)) :
                    #print(value)
                    if 2>index:
                        #print(value[index])
                        pass
                    else :
                       # print(value[2])
                        for i in range(len(value[2])):
                            # print("liste sayısı : ",len(value[2])," elimiz de lki sayı ",i," değerimiz : ",value[2][i])
                            
                            if (key=="robot_arm_y_positive") and (i==0):
                                self.data[key]=value[2][i]
                            elif (key=="robot_arm_x_positive") and (i==1):
                                self.data[key]=value[2][i]
                            elif (key=="robot_arm_y_negative") and (i==2):
                                self.data[key]=value[2][i]
                            elif (key=="robot_arm_x_negative") and (i==3):
                                self.data[key]=value[2][i]
                            elif (key=="clock_right_motor") and (i==4):
                                self.data[key]=value[2][i]
                            elif (key=="robot_arm_z_positive") and (i==5):
                                self.data[key]=value[2][i]
                            elif (key=="clock_left_motor") and (i==6):
                                self.data[key]=value[2][i]
                            elif (key=="robot_arm_z_negative") and (i==7):
                                self.data[key]=value[2][i]
                            #elif (key=="None") and (i==8):
                            #    self.data[key]=value[2][i]
                            elif (key=="robot_stop") and (i==8):
                                self.data[key]=value[2][i]
                            elif (key=="robot_run") and (i==9):
                                self.data[key]=value[2][i]
                            elif (key=="gripper_negative") and (i==10):
                                self.data[key]=value[2][i]
                            elif (key=="gripper_positive") and (i==11):
                                self.data[key]=value[2][i]

        #print("gönderilen json veri yapısı : ",self.data)
        return json.dumps(self.data)

    # def JoystickEvent(self):
    #
    #     return self.joystcik.pyGame.event.get()
            
    def joystcikControllerNameSwitch(self,id=None,index=None):
        """
        diğer yazılım dillerine cevap verebilmek adına her yerden kontrol edebilmek adına
        joystik ten gelen bilgileri websocket bağlantısı ile transfer edeilmek için 
        ad landırma yaparak daha verimli sonuçlar elde edebilmek adına böyle bir yol izlenmiştir

        Joystick -------> buton adlandırma --------> Json diline çevirme -------> websockets ile server bağlantı -------> araç kontrol

        """
        switch=[
            [
                "motor_x_axis",
                "motor_y_axis",
                "cam_x_axis",
                "cam_y_axis",
            ],
            [
                "robot_arm_y_positive",
                "robot_arm_x_positive",
                "robot_arm_y_negative",
                "robot_arm_x_negative",
                "clock_right_motor",
                "robot_arm_z_positive",
                "clock_left_motor",
                "robot_arm_z_negative",
                "None",
                "robot_stop",
                "robot_run",
                "gripper_negative",
                "gripper_positive",
            ]
        ]
        return switch[id]

if __name__ == '__main__':
    pygame.init()
    try:
        joystcik=pyGameJoystick(pyGame=pygame)
    except Exception as exp:
        print("joytcik başlatılırken bir sorun çıktı sorun... : ",exp)
    try:
        roboSocketCom=RoboSocketCom(clientHost="127.0.0.1",clientPort=5000)
        # roboSocketCom=RoboSocketCom(clientHost="172.19.96.191",clientPort=65432)
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ",exp)

    try:
        json_Controller=jsonController(joyStick=joystcik,roboSocketCom=roboSocketCom)
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ",exp)
        
    while True :
        try :
            # # print(joystcik.pyGame.event.get())
            # print(pygame.event.get())
            # if joystcik.pyGame.event.get()!=[]:
            json_Controller.controlJsonWrite()
            
        except Exception as exp:
            print("json_Controllerinde bir hata yakalandı : ",exp)
