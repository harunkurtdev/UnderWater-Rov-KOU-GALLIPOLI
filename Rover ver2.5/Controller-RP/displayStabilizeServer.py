import json
import base64
import io
import asyncio
import websockets
import cv2
import numpy as np
from Display_Stabilize import Display

class DisplayStabilizeServer:

    "Burada ki amaç şudur raspberry pi den geliştirğidiğimiz bu kütüphane sayesinde websockets üzerinden" \
    "verillerimizi aktararak kablosuz bağlantı sayesinde mobil ve bilgisayar üzerinden rahatlıkla kamera bilgileirine " \
    "erişebilmeyi sağlanmaktayız..."

    def __init__(self, serverHost=None, serverPort=None, clientHost=None, clientPort=None,display=None):
        "gelen bilgiler atanmakta..."
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientHost = clientHost
        self.clientPort = clientPort
        # if display!=None:
        self.display=Display()

        "socket bağlantılarını başlat"
        # self.socketRun()

    def __exit__(self, exc_type, exc_val, exc_tb):
        cv2.destroyAllWindows()

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
   |----------------------------------------GALLIPOLI ROV RASPBERRY PI WebSocketsOpencvServer -------------------------------|
   |  RoboSocketCom Sunucusu Başlatılıyor -- MikroDenetleyici ile Haberleşmeye Hazırlanıyor...                               |
   |-------------------------------------------------------------------------------------------------------------------------|
   |  RoboSocketcom Sunucusunun Portu : {self.serverPort}                                                                                 |
   |-------------------------------------------------------------------------------------------------------------------------|
                  """)
        return self.startserver

    # def camRead(self,img=None):
    #     "camRead fonksiyonun amacı camera kare bilgimize bu fonksiyon sayesinde erişebilmek"
    #
    #     "camera idsi var ise ve camera açılmış ise if bölümüne gir"
    #     if self.cam.isOpened():
    #         """Bu bölüm bizim cameramızdan gelen verileri alığ ilettiğimiz kısımdır
    #            """
    #         ret, frame = self.cam.read()
    #         if ret == True:
    #             return frame

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
            # print("client ten gelen : ", self.message)
            if self.message != None:
                "base64 formatında resimlerimizi okuyarak bu okunan resimler üzerinden resimlerimizi tanıma yazma ve okuma gibi işlemlerini yapacağız"
                # im_bytes = base64.b64decode(self.message)
                # im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
                # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                # cv2.imshow("Resim",img)
                # cv2.waitKey(1)



                frame = self.display.make_image(0, 0, 0)
                _, im_arr = cv2.imencode(".jpg", frame)
                im_bytes = im_arr.tobytes()
                im_b64 = base64.b64encode(im_bytes)
                # print(im_b64)
                await websockets.send(im_b64)
                # self.loop.run_until_complete(self.startRoboServerConnect(clientHost="172.19.96.227",clientPort=5000,sendMessage=json.dumps(self.data)))
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
    import socket

    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    print(f" Cihazın ismi : {hostname} \n Cihazın ip adresi : {ip_address}")
    robosocket = DisplayStabilizeServer(serverHost="0.0.0.0", serverPort=5001,)

    # robosocketclient=RoboSocketCom(clientHost="127.0.0.1",clientPort=5000)
    # robosocketclient.startRoboServerConnect()
    # robosocketclient.socketRun()


