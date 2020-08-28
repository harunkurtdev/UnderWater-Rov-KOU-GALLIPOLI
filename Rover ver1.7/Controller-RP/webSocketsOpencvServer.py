from roboSocketCom import RoboSocketCom
import json
import base64
import io
import asyncio
import websockets
import cv2
import numpy as np

class RovCamSocketsTransfer:

    "Burada ki amaç şudur raspberry pi den geliştirğidiğimiz bu kütüphane sayesinde websockets üzerinden" \
    "verillerimizi aktararak kablosuz bağlantı sayesinde mobil ve bilgisayar üzerinden rahatlıkla kamera bilgileirine " \
    "erişebilmeyi sağlanmaktayız..."

    def __init__(self,roboSocketCom=None,camId=None):
        self.roboSocketCom=roboSocketCom
        self.cam=cv2.VideoCapture(camId)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cam.release()
        cv2.destroyAllWindows()

    def camRead(self):
        "camRead fonksiyonun amacı camera kare bilgimize bu fonksiyon sayesinde erişebilmek"

        "camera idsi var ise ve camera açılmış ise if bölümüne gir"
        if self.cam.isOpened():
            """Bu bölüm bizim cameramızdan gelen verileri alığ ilettiğimiz kısımdır
               """
            ret, frame = self.cam.read()
            if ret == True:
                return frame

    def camWrite(self,roboSocketCom=None):
        
        """WebSockets bağlantılarını başlatarak ilgili aracımızın camera işlemlerini
            yapmayı başlatıyoruz ve böylelikle aracımız ile online bağlantı yaparak başlıyor kamera bilgilerini aktarmaya
            başlıyoruz....
        """

        "roboSocket boş ise veya dolu ise istenilen socketi atayalım"
        if self.roboSocketCom==None or roboSocketCom:
            self.roboSocketCom=roboSocketCom

        frame=self.camRead()
        _,im_arr=cv2.imencode(".jpg",frame)
        im_bytes=im_arr.tobytes()
        im_b64=base64.b64encode(im_bytes)

        #cv2.imshow("frame",frame)

        try :
            "hata oluşmaz  ise bu bölümde server a verilerimizi transfer edeceğiz"
            asyncio.get_event_loop().run_until_complete(self.roboSocketCom.startRoboServerConnect(sendMessage=im_b64))
        except Exception as exp:
            print(" içinde startRoboServerConnect ile veri aktalırken bir hata oluştu hata kodu : ",exp)


if __name__ == '__main__':
    "Clienthost bilgisine raspberry pi ip bilgisini giriyoruz... "
    try:
        roboSocketCom=RoboSocketCom(clientHost="172.19.96.227",clientPort=5001)
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ",exp)
    try:
        rovCamSocketsTransfer=RovCamSocketsTransfer(roboSocketCom=roboSocketCom,camId=0)
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ",exp)
        
    while True :
        try :
            rovCamSocketsTransfer.camWrite()
            cv2.imshow("Resim 2",rovCamSocketsTransfer.camRead())

        except Exception as exp:
            print("rovCamClient bir hata yakalandı : ",exp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
