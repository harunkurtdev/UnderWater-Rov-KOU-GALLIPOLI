import cv2
import urllib.request as ur
import numpy as np

# Replace the URL with your own IPwebcam shot.jpg IP:port
url = 'http://172.19.96.227:9875/video_feed'

while True:
    # Use urllib to get the image from the IP camera
    print("deneme")
    imgResp = ur.urlopen(url)
    print(imgResp.read())
    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    print(imgNp)
    # Finally decode the array to OpenCV usable format ;)
    img = cv2.imdecode(imgNp, -1)

    # put the image on screen
    cv2.imshow('IPWebcam', img)

    # To give the processor some less stress
    # time.sleep(0.1)

    # Quit if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
