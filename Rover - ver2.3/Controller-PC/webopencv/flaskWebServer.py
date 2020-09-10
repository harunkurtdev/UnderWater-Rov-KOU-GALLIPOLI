from flask import Flask, render_template, Response #burada flask kütüphanesinden parçalarımızı cıkardık
import cv2  # opencv kütüpahensini ekledik
import imutils

#from singlemotiondetector import SingleMotionDetector

class flaskWebServer:

    def __init__(self, app,port,debug,threaded,use_reloader):
        self.app = app
        self.port=port
        self.debug=debug
        self.threaded=threaded
        self.use_reloader=use_reloader

    
    def appRun(self):
        self.appRoutue()
        self.app.run(host="0.0.0.0",port=9875,debug=True,threaded=True,use_reloader=True)

        
    def appRoutue(self):

        @self.app.route('/')
        def index():
            return render_template("trova_hareket.html")

        @self.app.route('/video_feed')
        def video_feed():
            '''burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
            Response ise burada cevap almamıızı sağlıyor
            -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
            sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
            '''
            return Response(self.rootImage(),mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/video_feed_arm')
        def video_feed():
            '''burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
            Response ise burada cevap almamıızı sağlıyor
            -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
            sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
            '''
            return Response(self.rootArmImage(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/mpu_display')
        def video_feed(self):
            '''burada amaç ise index.html sayfasına ihtiyaç duymadan anlık olarak verilerimizi kaydetip çekebiliyoruz
            Response ise burada cevap almamıızı sağlıyor
            -Sayfaya istek atıyoruz atılan isteğe göre bir Response dönüyor ancak verimiz
            sürekli olması gerektiği için Response ile sarmalayıp mimetype ile gerş dönüşü belli ediyoruz...
            '''
            return Response(self.rootMpuStabilizatorImage(),mimetype='multipart/x-mixed-replace; boundary=frame')


    """
    RootImage ve rootArmImage 2 kameradan gelen görüntüleri direkt olarak
    web üzerine aktarmak için while döngüsünden kaldırıldı
    ayhnı zamanda 
    """

    "rootimage kameradan okunan bilgiler girilecektir. "
    def rootImage(self,image=None):
        """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
        #while True:
        # NOT : While kaldırıldı
        rval, frame = image.read()
        #resim = display_stabilazatora.DisplayStabilzator(frame)
        if rval==True:

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """

            #if not flag:
            #    continue
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

    "rootArmImage kameradan okunan bilgiler girilecektir. "
    def rootArmImage(self,image=None):
        """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
        #while True:
            # NOT : While kaldırıldı
        rval, frame = image.read()
        #resim = display_stabilazatora.DisplayStabilzator(frame)
        if rval==True:

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """

            # if not flag:
            #     continue
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')
    
    """rootMpuStabilizatorImage mpu üzerinden Uart ile okunan bilgiler 
    işlenerek bu bölüme girecektir
    """
    def rootMpuStabilizatorImage(self,image=None):
        """Burada sonsuz bir döngü oluşturarak Streaming bir şekilde resmimizi kaydetip okuma işlemleri ypaıyoruz"""
        #while True:
            # NOT : While kaldırıldı
        rval, frame = image.read()
        #resim = display_stabilazatora.DisplayStabilzator(frame)
        if rval==True:

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            
            """yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
                    """

            # if not flag:
            #     continue
            # yield the output frame in the byte format
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

if __name__ == '__main__':
    app=Flask(__name__)
    flaskWebServer(app=app,port=9875,debug=True,threaded=True,use_reloader=True).appRun()