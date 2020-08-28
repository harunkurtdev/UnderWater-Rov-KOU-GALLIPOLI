import asyncio
import websockets
import json
import numpy as np
import serial
import time
import cv2
import base64
class RoboSocketCom:

    def __init__(self, serverHost=None, serverPort=None, clientHost=None, clientPort=None):
        "gelen bilgiler atanmakta..."
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientHost = clientHost
        self.clientPort = clientPort
        self.loop=asyncio.get_event_loop()
        "Raspberry pi de roboSocketCom classını çalıştırmaya başladığımız da biz oraya joystick bilgilierini bastırmayı " \
        "hedeflediğimiz için başka bir json verisi yazdırmayı düşüğündüğümüzde hata almaktayız..." \
        "algoritymamızın sağa sol vs vs gibi özellikleri bunun üzerine inşa ederek daha düzgün" \
        "çalışabilir bir şekilde hedeflemekteyiz..."
        self.data = {
            "motor_x_axis": 0.0,
            "motor_y_axis": 0.0,
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
            "robot_run": 0,
            "gripper_negative": 0,
            "gripper_positive": 0,
        }



        "socket bağlantılarını başlat"
        self.socketRun()

    def socketRun(self):

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
            asyncio.get_event_loop().run_until_complete(self.startRoboServer())
            "clientHost ve clientPort dolu ise bağlanma işlemi başlasın"
            asyncio.get_event_loop().run_forever()

        if self.clientHost == None and self.clientPort == None:
            pass
        else:
            "client bilgilerini burada doldurabilir connect işlemini başlatılabilir ancak hata alınmakta"
            pass
            # asyncio.get_event_loop().run_until_complete(self.startRoboServerConnect())

    def startRoboServer(self, serverHost=None, serverPort=None):
        "server ın başlatılması gerektiğini dile getiyoruz gelen verileri roboResponse da yakalamamız gerektiğini istoyruz"
        if self.serverHost == None or self.serverPort == None:
            self.serverHost = serverHost
            self.serverPort = serverPort

        self.startserver = websockets.serve(self.roboServer, self.serverHost, self.serverPort)
        print("Rov Cam Server Çağrısı başladı")
        return self.startserver

    async def roboServer(self, websockets, path):
        """
        Burada bir algoritma üreterek ancak send veri gönderebiliriz... gelen verileri buradan
        recv ile yakalarız...
        """
        self.roboServerWebSocket = websockets

        """
        send() fonksiyonu ile gelen mesajlara karşılık verebiliriz...
        """
        """gelen mesajları bu fonksiyon içerisinde recv() ile yakalayıp 
        ekrana basabiliriz...
        """
        try:
            self.message = await websockets.recv()
            # print("client ten gelen : ",self.message)

            if self.message!=None:
                "base64 formatında resimlerimizi okuyarak bu okunan resimler üzerinden resimlerimizi tanıma yazma ve okuma gibi işlemlerini yapacağız"
                im_bytes = base64.b64decode(self.message)
                im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                cv2.imshow("Resim",img)
                cv2.waitKey(1)
                #await websockets.send("server dan giden mesaj- roboServerWebSocket")
                self.loop.run_until_complete(self.startRoboServerConnect(clientHost="172.19.96.227",clientPort=5000,sendMessage=json.dumps(self.data)))
            else:
                cv2.destroyAllWindows()
        except Exception as exp:
            print("roboServer bölümünde veriler gelirken bir hata oluştu hata kodu : ", exp)

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


if __name__ == '__main__':
    robosocket = RoboSocketCom(serverHost="0.0.0.0", serverPort=5001)
    # robosocketclient=RoboSocketCom(clientHost="127.0.0.1",clientPort=5000)
    # robosocketclient.startRoboServerConnect()
    # robosocketclient.socketRun()


