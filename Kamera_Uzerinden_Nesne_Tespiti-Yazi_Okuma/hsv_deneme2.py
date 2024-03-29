import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    # lower_blue = np.array([110,50,50])
    lower_blue = np.array([0,191,0])#Sualtın da ki nesne
    # lower_blue = np.array([91,159,255])#Sualtında ki Çember
    # upper_blue = np.array([130,255,255])
    upper_blue = np.array([15,255,255])#Sualtında ki nesne
    # upper_blue = np.array([112,255,255])#Sualtında ki Çember
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()