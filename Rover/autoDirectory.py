import asyncio
import websockets
import json
import numpy as np
import serial
import time


#
# port = serial.Serial("COM5"  # com girilmesi gerekli
#                          , baudrate=115200  # baund rate
#                          , timeout=0
#                          ,parity=serial.PARITY_NONE,
#                          bytesize=serial.EIGHTBITS,
#                          stopbits=serial.STOPBITS_ONE
#                      )  # zaman aşım

class RoboSocketCom:

    def __init__(self, serverHost=None, serverPort=None, clientHost=None, clientPort=None, serialPort=None):
        "gelen bilgiler atanmakta..."
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientHost = clientHost
        self.clientPort = clientPort
        self.serialPort = serialPort
        self.robot_working = None
        self.direction = None
        self.frontSpeed = 1500
        self.backSpeed = 1500
        self.goLeftSpeed = 1500
        self.goRightSpeed = 1500
        self.turnRightSpeed = 1500
        self.turnLeftSpeed = 1500
        self.gripper_arm = 1500
        self.robotHeightSpeed = 1500
        self.robotHeight = 0
        self.cam_x_position = 1500
        self.cam_y_position = 1500
        self.readJson = ""

        "socket bağlantılarını başlat"
        # self.socketRun()

    async def socketRun(self):

        """asyncio ile fonksiyonu başlatılmasını isteyerek burada fonksiyonu çağrıyoruz
        ve bölyelikle rahatlıkla socket bağlantımızın başlatılmasını sağlıyoruz ve istenilen bağlantı yapılmış
        oluyor...
        self.startRoboServer() yerine
        self.startserver da yazılabilirdi ancak fonksiyonu başlatmak gerekli...
        """

        "serverhost ve serverPort dolu ise server başlasın"
        if self.serverHost == None and self.serverPort == None:
            pass
        else:
            return await self.startRoboServer()
            # asyncio.get_event_loop().run_until_complete(self.startRoboServer())
            "clientHost ve clientPort dolu ise bağlanma işlemi başlasın"
            # asyncio.get_event_loop().run_forever()

        if self.clientHost == None and self.clientPort == None:
            pass
        else:
            "client bilgilerini burada doldurabilir connect işlemini başlatılabilir ancak hata alınmakta"
            pass
            # asyncio.get_event_loop().run_until_complete(self.startRoboServerConnect())

    async def startRoboServer(self, serverHost=None, serverPort=None):
        "server ın başlatılması gerektiğini dile getiyoruz gelen verileri roboResponse da yakalamamız gerektiğini istoyruz"
        if self.serverHost == None or self.serverPort == None:
            self.serverHost = serverHost
            self.serverPort = serverPort
        self.startserver = await websockets.serve(self.roboServer, self.serverHost, self.serverPort)
        print(f"""
   |----------------------------------------GALLIPOLI ROV RASPBERRY PI RoboSocketCom ----------------------------------------|
   |  RoboSocketCom Sunucusu Başlatılıyor -- MikroDenetleyici ile Haberleşmeye Hazırlanıyor...                               |
   |-------------------------------------------------------------------------------------------------------------------------|
   |  RoboSocketcom Sunucusunun Portu : {self.serverPort}                                                                                 |
   |-------------------------------------------------------------------------------------------------------------------------|
                  """)
        return self.startserver

    def motorSpeedMap(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    async def roboServer(self, websockets, path):
        """
        Burada bir algoritma üreterek ancak send veri gönderebiliriz... gelen verileri buradan
        recv ile yakalarız...
        """
        self.roboServerWebSocket = websockets

        """
        send() fonksiyonu ile gelen mesajlara karşılık verebiliriz...
        """
        # await websockets.send("server dan giden mesaj roboServerWebSocket")

        """gelen mesajları bu fonksiyon içerisinde recv() ile yakalayıp 
        ekrana basabiliriz...
        """
        self.message = await websockets.recv()
        "json.loads methodunu kullanmak zorundasın aksi halde hata alırsın"
        value = json.loads(self.message)

        try:
            # print("client ten gelen : ",self.message)
            self.direction = "0"

            if value != None:
                if value["goLeftSpeed"] ==True:
                    self.direction = "1"
                    self.goLeftSpeed = 1600
                    self.goRightSpeed = 1400

                if value["goRightSpeed"] ==True:
                    self.direction = "2"
                    self.goRightSpeed = 1600
                    self.goLeftSpeed = 1400

                if value["backSpeed"]==True:
                    self.direction = "4"
                    self.backSpeed = 1400
                    self.frontSpeed = 1400

                if value["frontSpeed"]==True:
                    self.direction = "3"
                    self.frontSpeed = 1600
                    self.backSpeed = 1600
                    # self.frontSpeed = self.motorSpeedMap(-value["motor_y_axis"], 0.0, 1.0, 1100, 1900)

                if (0 < float(value["cam_y_axis"]) <= 0.999969482421875):
                    self.cam_y_position = self.motorSpeedMap(value["cam_y_axis"], 0.0, 0.999969482421875, 1500, 1100)

                elif (0 > float(value["cam_y_axis"]) >= -1.0) and value["cam_y_axis"] != -3.0517578125e-05 and value[
                    "cam_y_axis"] != -0.007843017578125:
                    self.cam_y_position = self.motorSpeedMap(-value["cam_y_axis"], 0.0, 1.0, 1500, 1900)

                if (0 < float(value["cam_x_axis"]) <= 0.999969482421875):
                    self.cam_x_position = self.motorSpeedMap(value["cam_x_axis"], 0.0, 0.999969482421875, 1500, 1100)

                elif (0 > float(value["cam_x_axis"]) >= -1.0) and value["cam_x_axis"] != -3.0517578125e-05 and value[
                    "cam_x_axis"] != -0.007843017578125:
                    self.cam_x_position = self.motorSpeedMap(-value["cam_x_axis"], 0.0, 1.0, 1500, 1900)

                if value["turnLeftSpeed"]==True:
                    self.direction = "5"
                    self.turnLeftSpeed = 1400
                    self.turnRightSpeed = 1600

                if value["turnRightSpeed"] ==True:
                    self.direction = "6"
                    self.turnRightSpeed = 1400
                    self.turnLeftSpeed = 1600

                if -1001 < self.robotHeight <= 0:
                    self.robotHeightSpeed = self.motorSpeedMap(self.robotHeight, 0, -1000, 1500, 1100)

                if 1001 > self.robotHeight >= 0:
                    self.robotHeightSpeed = self.motorSpeedMap(self.robotHeight, 0, 1000, 1500, 1900)

                if value["robotHeightStop"]==True:
                    self.robotHeight = 0
                    self.robotHeightSpeed = 1500

                if value["robotHeightPositive"]==True:
                    self.robotHeight += 10

                if value["robotHeightNegative"]==True:
                    self.robotHeight -= 10

                writeJson = {
                    "direction": self.direction,
                    "frontSpeed": self.frontSpeed,
                    "backSpeed": self.backSpeed,
                    "goLeftSpeed": self.goLeftSpeed,
                    "goRightSpeed": self.goRightSpeed,
                    "turnRightSpeed": self.turnRightSpeed,
                    "turnLeftSpeed": self.turnLeftSpeed,
                    "robotHeightSpeed": self.robotHeightSpeed,
                    "gripper_arm": 1900,
                    "cam_x_position": 1900,
                    "cam_y_position": self.cam_y_position,
                }
                writeJson = json.dumps(writeJson)
                print(writeJson)

                if value["robot_stop"] == 1 or value["robot_stop"] == True or self.robot_working == False:
                    # print("durdu")
                    self.robot_working = False
                if value["robot_run"] == 1 or value["robot_run"] == True or self.robot_working == True:
                    # print("çalışıyor")
                    # print(json.loads(writeJson))
                    if self.serialPort.isOpen():
                        try:
                            # self.serialPort.flush()
                            # print(writeJson)
                            self.serialPort.write(str(writeJson + "\n").encode("utf-8"))
                            self.readJson = self.serialPort.readline().decode("utf-8")
                            print("--" + self.readJson + "--")
                            if self.readJson != None and self.readJson != "{}" and self.readJson != "":
                                # print( "gelen veri :---"+ self.readJson +"---bitti")
                                # sw=json.loads(writeJson)
                                # print( "yazdırılan veri : ",str(sw["turnLeftSpeed"]))
                                try:
                                    # self.readJson=json.loads(self.readJson)
                                    # print("sola : "+ str(self.readJson["goLeftSpeed"])+ " sağa : "+str(self.readJson["goRightSpeed"]))
                                    # print(self.readJson)
                                    # print(self.readJson)
                                    # await websockets.send(readJson)
                                    pass
                                except Exception as exp:
                                    "hata aldığımız için pass ediyoruz.."
                                    # print(exp)
                                    pass
                            else:
                                # print("veri okunmuyor")
                                pass
                        except Exception as e:
                            print(e)
                            pass

                    self.robot_working = True

                self.direction = "0"
                self.frontSpeed = 1500
                self.backSpeed = 1500
                self.goRightSpeed = 1500
                self.goLeftSpeed = 1500
                self.turnRightSpeed = 1500
                self.turnLeftSpeed = 1500
                # self.gripper_arm=1500

            await websockets.send(self.readJson)
        except Exception as exp:
            pass
            print("roboServer bölümünde veriler gelirken bir hata oluştu hata kodu : ", exp)
        finally:
            # print(value)
            pass

    async def startRoboServerConnect(self, clientHost=None, clientPort=None, sendMessage=None):
        "Server a diğer araçta ki server a bağlanma durumunu buradan ele alarak yapacağız"

        if self.clientHost == None or self.clientPort == None:
            self.clientHost = clientHost
            self.clientPort = clientPort

        """
        websocket bağlantısı açılmaktadır ve bu açılma işlemi ile verileri transfer işlemi yapmaktayız...

        """
        async with websockets.connect(
                "ws://" + str(self.clientHost) + ":" + str(self.clientPort)) as roboClientWebSocket:

            "hata alınmaz ise verileri aktarma bölümü..."
            try:
                self.roboClientWebSocket = roboClientWebSocket
                """
                farklı bir foknsiyon içerisinde verilerimizi transfer işlemi yapmaya çalışmaktayız...
                ancak verileri transfer ederken bir sorun almaktayız ----düzeltimesi gerekiyor----
                ------ Hatalı bölüm-----------
                #asyncio.get_event_loop().run_until_complete(self.roboSendMessage(roboClientWebSocket=self.roboClientWebSocket,sendMessage=sendMessage))
                """

                " foksiyon sayesinde alınan veriyi socket üzerinden server a transfer etme işlemi"
                await self.roboClientWebSocket.send(sendMessage)

                "server dan gelen veriyi dinleme işlemi"
                print(await self.roboClientWebSocket.recv())
                return self.roboClientWebSocket
            except Exception as hata:
                print("startRoboServerConnect bölümünde veriler iletilirken bir hata ile karışılaşıldı hata kodu : ",
                      hata)

    async def roboSendMessage(self, roboClientWebSocket=None, sendMessage=None):
        "buradan bir mesaj gönderme işlemi yapılmaktadır..."
        # self.roboClientWebSocket=await self.startRoboServerConnect()

        if sendMessage == None:
            pass
        else:
            try:
                await self.roboClientWebSocket.send(sendMessage)
                print(await self.roboClientWebSocket.recv())

            except Exception as exp:
                print("roboSendMessage bölümünde veriler iletilirken bir hata ile karşılaşıldı hata kodu : ", exp)
        # self.roboClientWebSocket.close()


if __name__ == '__main__':
    robosocket = RoboSocketCom(serverHost="127.0.0.1", serverPort=5000)
    # robosocketclient=RoboSocketCom(clientHost="127.0.0.1",clientPort=5000)
    # robosocketclient.startRoboServerConnect()
    # robosocketclient.socketRun()


