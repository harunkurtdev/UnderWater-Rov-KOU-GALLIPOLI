import asyncio
import websockets
import json
import numpy as np
import serial
import time
import cv2
import base64

class RovCamSocketsTransfer:
    "Burada ki amaç şudur raspberry pi den geliştirğidiğimiz bu kütüphane sayesinde websockets üzerinden" \
    "verillerimizi aktararak kablosuz bağlantı sayesinde mobil ve bilgisayar üzerinden rahatlıkla kamera bilgileirine " \
    "erişebilmeyi sağlanmaktayız..."

    def __init__(self, roboSocketCom=None):
        self.roboSocketCom = roboSocketCom

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.cam.release()
        cv2.destroyAllWindows()

    async def startRoboServerConnectCamRead(self, clientHost=None, clientPort=None, sendMessage=None):
        "Server a diğer araçta ki server a bağlanma durumunu buradan ele alarak yapacağız"

        # if self.clientHost == None or self.clientPort == None:
        self.clientHost = clientHost
        self.clientPort = clientPort

        """
        websocket bağlantısı açılmaktadır ve bu açılma işlemi ile verileri transfer işlemi yapmaktayız...

        """
        async with websockets.connect("ws://" + str(self.clientHost) + ":" + str(self.clientPort)) as roboClientWebSocket:

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
                # print(await self.roboClientWebSocket.recv())

                "base64 formatında resimlerimizi okuyarak bu okunan resimler üzerinden resimlerimizi tanıma yazma ve okuma gibi işlemlerini yapacağız"
                im_bytes = base64.b64decode(await self.roboClientWebSocket.recv())
                im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
                cv2.imshow("Resim", img)
                cv2.waitKey(1)
            except Exception as hata:
                print("startRoboServerConnect bölümünde veriler iletilirken bir hata ile karışılaşıldı hata kodu : ",
                      hata)

if __name__ == '__main__':
    "Clienthost bilgisine raspberry pi ip bilgisini giriyoruz... "
    try:
        # roboSocketCom = RoboSocketCom(clientHost="127.0.0.1", clientPort=5001)
        pass
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)
    try:
        rovCamSocketsTransfer = RovCamSocketsTransfer()#roboSocketCom=roboSocketCom
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

    while True:
        try:
            asyncio.get_event_loop().run_until_complete(rovCamSocketsTransfer.startRoboServerConnectCamRead(clientHost="127.0.0.1", clientPort=5001,sendMessage="deneme"))
            # cv2.imshow("Resim 2", rovCamSocketsTransfer.camRead())

        except Exception as exp:
            print("rovCamClient bir hata yakalandı : ", exp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

