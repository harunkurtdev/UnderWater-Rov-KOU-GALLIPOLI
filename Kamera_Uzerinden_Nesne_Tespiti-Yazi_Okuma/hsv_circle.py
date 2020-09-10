import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if cap.isOpened():
    while(True):
        ret,frame= cap.read()
        # blurring the frame that's captured
        frame_gau_blur = cv2.GaussianBlur(frame, (3, 3), 0)
        # converting BGR to HSV
        hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV)
        # the range of blue color in HSV
        lower_blue = np.array([110, 50, 50])
        higher_blue = np.array([130, 255, 255])
        # getting the range of blue color in frame
        blue_range = cv2.inRange(hsv, lower_blue, higher_blue)
        # getting the V channel which is the gray channel
        blue_s_gray = blue_range[::2]
        # applying HoughCircles
        circles = cv2.HoughCircles(blue_s_gray, cv2.HOUGH_GRADIENT, 1, 80, 1, 25, 5, 50)
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # drawing on detected circle and its center
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        cv2.imshow('circles', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()