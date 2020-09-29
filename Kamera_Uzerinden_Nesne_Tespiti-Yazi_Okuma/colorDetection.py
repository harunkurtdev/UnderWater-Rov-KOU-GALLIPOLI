import cv2
import numpy as np

import websockets,asyncio,time,json,cv2,base64
import numpy as np
# from shapeDetectionClass import ShapeDetection
from websocket import create_connection


# capturing video through webcam

# cap = cv2.VideoCapture(0)
def connect(url,port):
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img
while (1):
    ip = "192.168.1.42"
    # _, img = cap.read()
    img = connect(ip, 5002)
    # converting frame(img == BGR) to HSV(hue-saturation-value)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # red color

    red_lower = np.array([0,191,0], np.uint8)
    # red_lower = np.array([136, 87, 111], np.uint8)
    # red_upper = np.array([180, 255, 255], np.uint8)
    red_upper = np.array([15,255,255], np.uint8)

    # blue color

    blue_lower = np.array([99, 115, 150], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # yellow color

    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # white color

    white_lower = np.array([0, 0, 200], np.uint8)
    white_upper = np.array([180, 20, 255], np.uint8)

    # black color

    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([180, 255, 30], np.uint8)

    # all color together

    red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    white = cv2.inRange(hsv, white_lower, white_upper)
    black = cv2.inRange(hsv, black_lower, black_upper)

    # Morphological Transform, Dilation

    kernal = np.ones((1, 1), "uint8")

    red = cv2.dilate(red, kernal)
    res_red = cv2.bitwise_and(img, img, mask=red)

    blue = cv2.dilate(blue, kernal)
    res_blue = cv2.bitwise_and(img, img, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    res_yellow = cv2.bitwise_and(img, img, mask=yellow)

    white = cv2.dilate(white, kernal)
    res_white = cv2.bitwise_and(img, img, mask=white)

    black = cv2.dilate(black, kernal)
    res_black = cv2.bitwise_and(img, img, mask=black)
    cv2.imshow("asd",red)
    # Tracking red
    ( contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

            # Tracking blue
    # (contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #         cv2.putText(img, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

    # Tracking yellow
    # (contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         cv2.putText(img, "Yellow Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

    # Tracking white
    # (contours, hierarchy) = cv2.findContours(white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #         cv2.putText(img, "White Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))

    # Tracking black
    # ( contours, hierarchy) = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
    #         cv2.putText(img, "Black Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0))

    cv2.imshow("Color Tracking", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break