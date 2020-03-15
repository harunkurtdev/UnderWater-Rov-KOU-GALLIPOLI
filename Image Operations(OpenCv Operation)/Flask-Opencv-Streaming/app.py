#!/usr/bin/env python
from flask import Flask, render_template, Response #burada flask kütüphanesinden parçalarımızı cıkardık
import cv2  # opencv kütüpahensini ekledik
#import numpy as np

"""Bu sayfa bize web üzerinden ve aynı zamanda desktop görüntü almamıza yarıyor"""


app = Flask(__name__) #flask ı bu saftada entegre ettik
video = cv2.VideoCapture(0) # opencv kütüpahensi ile
''' bu kameradan bilgi almasını istedik'''

'burada sayfaya ilk girildiğinde bize html bilgisini göstermesini istedik'
i=0
@app.route('/')
def index():
    """Video streaming home page."""

    def sayac(i=0):
        while True:
        #return render_template('index.html')

            yield str(i)+"sayac \n"
            i+=1
    return Response(sayac(), mimetype="text")

    'burada template ile index.html bilgisini göstermesini istedik'


def gen():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
    while True:
        rval, frame = video.read()
        ret, kare = video.read()
        #resim = display_stabilazatora.DisplayStabilzator(frame)

        cv2.imwrite('t.jpg', frame)
        #cv2.imshow("Islenmis Video", frame)
        #cv2.imshow("Normal Video", kare)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

        '''yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')'''
        if cv2.waitKey(25)&0xFF==ord("q"):
            video.release()
            cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, threaded=True,host="0.0.0.0",port=9875)

