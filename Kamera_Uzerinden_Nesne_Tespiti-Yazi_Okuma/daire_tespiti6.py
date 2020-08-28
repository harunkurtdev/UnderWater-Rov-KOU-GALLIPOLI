import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(1):
    ret,frame=cap.read()
    frame = cv2.bilateralFilter(frame, 5, 175, 175)
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white=np.array([0,0,225])
    upper_white=np.array([179,255,255])
    mask=cv2.inRange(hsv,lower_white,upper_white)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('frame',frame)
    cv2.imshow('result',res)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()