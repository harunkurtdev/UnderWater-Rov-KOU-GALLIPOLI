#!/usr/bin/env python
from flask import Flask, render_template, Response #burada flask kütüphanesinden parçalarımızı cıkardık
import cv2  # opencv kütüpahensini ekledik
#import numpy as np
import threading
import datetime
import imutils
import time
from singlemotiondetector import SingleMotionDetector

"""Bu sayfa bize web üzerinden ve aynı zamanda desktop görüntü almamıza yarıyor"""
app = Flask(__name__) #flask ı bu saftada entegre ettik
video = cv2.VideoCapture(0) # opencv kütüpahensi ile
''' bu kameradan bilgi almasını istedik'''

'burada sayfaya ilk girildiğinde bize html bilgisini göstermesini istedik'
@app.route('/')
def index():
    """Video streaming home page."""

    return render_template('trova_hareket.html')
    'burada template ile index.html bilgisini göstermesini istedik'

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock
    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        _,frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
    	"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
    	cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	    # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)
            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion

                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                (0, 0, 255), 2)
		
        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()



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


if __name__ == '__main__':
    app.run(debug=True, threaded=True,host="0.0.0.0",port=9875,use_reloader=True)
