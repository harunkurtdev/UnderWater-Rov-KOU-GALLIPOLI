from flask import Flask,render_template, Response
import json,base64,io,websockets,cv2,asyncio,socket
import numpy as np
from shapeDetectionClass import ShapeDetection
from webSocketsOpencvClient import WebSocketsOpencvClient
from roboSocketCom import RoboSocketCom
from websocket import create_connection

app=Flask(__name__)

@app.route("/")
def mainIndex():
    return "Naber lan Trekkk"

def streamCam():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
    while True:
        ws = create_connection("ws://127.0.0.1:5001")
        ws.send("Hello, World")
        result = ws.recv()
        ws.close()
        im_bytes = base64.b64decode(result.decode("utf-8"))
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        # cv2.imshow("Resim", img)
        img =img
        frame=img.copy()
        # shape.imgRead(img=img,imgContour=frame)
        # cv2.imshow("resim",frame)
        cv2.waitKey(1)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        """yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                """
        if not flag:
            continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(streamCam(),mimetype='multipart/x-mixed-replace; boundary=frame')

def streamCircles():
    """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""

    while True:
        ws = create_connection("ws://127.0.0.1:5001")
        ws.send("Hello, World")
        result = ws.recv()
        ws.close()
        im_bytes = base64.b64decode(result.decode("utf-8"))
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        # cv2.imshow("Resim", img)
        img = img
        frame = img.copy()
        shape.imgRead(img=img,imgContour=frame)
        # cv2.imshow("resim",frame)
        cv2.waitKey(1)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        """yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                """
        if not flag:
            continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')
    cv2.destroyAllWindows()

@app.route('/mission_circles')
def mission_circles():
    """burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
    Response ise burada cevap almamıızı sağlıyor
    -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
    sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
    """
    return Response(streamCircles(),mimetype='multipart/x-mixed-replace; boundary=frame')


async def MainLoop(host="0.0.0.0",port=5002,clientHost="127.0.0.1",clientPort=5001,loop=None):
    t1=loop.create_task(app.run(host=host,port=port,debug=True,use_reloader=True,threaded=True))
    await t1

if __name__ == '__main__':
    loop=asyncio.get_event_loop()
    shape = ShapeDetection()
    loop.run_until_complete(MainLoop(host="0.0.0.0",port=5002,loop=loop))
