#!/usr/bin/env python
from flask import Flask, render_template, Response #burada flask kütüphanesinden parçalarımızı cıkardık
import cv2  # opencv kütüpahensini ekledik
#import numpy as np
import threading
import argparse
import datetime
import imutils
import time
import cv2,asyncio
from webSocketsOpencvServer import WebSocketsOpencvServer

"""Bu sayfa bize web üzerinden ve aynı zamanda desktop görüntü almamıza yarıyor"""
app = Flask(__name__) #flask ı bu saftada entegre ettik
''' bu kameradan bilgi almasını istedik'''

'burada sayfaya ilk girildiğinde bize html bilgisini göstermesini istedik'
@app.route('/')
def index():
    """Video streaming home page."""

    return render_template('trova_hareket.html')
    'burada template ile index.html bilgisini göstermesini istedik'


def gen():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
    while True:
        rval, frame = video.read()
        #resim = display_stabilazatora.DisplayStabilzator(frame)
        if rval==True:

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """

            if not flag:
                continue
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')            
           

@app.route('/video_feed')
def video_feed():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

async def MainLoop(host="0.0.0.0",port=5002,loop=None):
    roboOpencv = WebSocketsOpencvServer(serverHost="127.0.0.1", serverPort=5003, video=video)
    print("girdi")
    t2 = loop.create_task(roboOpencv.socketRun())
    print("girdi")
    await t2
    t1=loop.create_task(app.run(host=host,port=port,debug=True,use_reloader=True,threaded=True))
    print("deneme")
    # await t1, t2

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    loop=asyncio.get_event_loop()
    loop.run_until_complete(MainLoop(host="0.0.0.0",port=5002,loop=loop))