import cv2
from urllib.request import urlopen
import numpy as np

while True:

    stream = urlopen('http://192.168.1.52:9875/video_feed')
    bytes = ''
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Video', img)
        if cv2.waitKey(1) == 27:
            exit(0)