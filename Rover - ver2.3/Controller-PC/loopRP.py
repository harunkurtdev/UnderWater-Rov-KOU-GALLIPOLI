from flask import Flask,render_template, Response
import json,base64,io,websockets,cv2
import numpy as np
from shapeDetectionClass import ShapeDetection
from webSocketsOpencvClient import RovCamSocketsTransfer
# from roboSocketCom import RoboSocketCom
"""
loop dosyası içerisinde programımızın akışı sağlanacaktır..
resimler flask üzerinden webBrowser da gösterebileceğimiz şekilde olabilmesini sağlamaktır.
aynı zamanda kurulan server da request atarak görevlerimizin tanımlamalarını yapabilir hale getirmek amacımız.
"""
app=Flask(__name__)
cam = cv2.VideoCapture(0) # opencv kütüpahensi ile
''' bu kameradan bilgi almasını istedik'''

@app.route("/")
def main():
    return "Naber lan Trekkk"

def gen():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
    while True:
        rval, frame = cam.read()
        ret,img=cam.read()

        shape.imgRead(img=img,imgContour=frame)
        # cv2.imshow("resim",frame)
        # cv2.waitKey(1)
        if ret == True:
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """
            if not flag:
                continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')



def ten():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""


    while True:
        rval, frame = cam.read()
        ret,img=cam.read()

        rovCamSocketsTransfer.camWrite(img=frame)

        shape.imgRead(img=img,imgContour=frame)
        # cv2.imshow("resim",frame)
        # cv2.waitKey(1)
        if ret == True:
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """
            if not flag:
                continue
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')


@app.route('/mission_circles')
def mission_circles():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(ten(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    shape = ShapeDetection()

    "Clienthost bilgisine raspberry pi ip bilgisini giriyoruz... "
    try:
        roboSocketCom = RoboSocketCom(clientHost="10.0.0.52", clientPort=5001)
    except Exception as exp:
        print("sockete bağlanma işlemi başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)
    try:
        rovCamSocketsTransfer = RovCamSocketsTransfer(roboSocketCom=roboSocketCom)
    except Exception as exp:
        print("jsonController başlatılırken bir sorun çıktı sorun... hata kodu : ", exp)

    app.run(host="0.0.0.0",port=5002,debug=True,use_reloader=True,threaded=True)