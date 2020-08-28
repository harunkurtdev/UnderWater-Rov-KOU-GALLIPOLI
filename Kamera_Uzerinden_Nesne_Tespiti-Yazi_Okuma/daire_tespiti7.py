import cv2
import numpy as np
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    frame2=cv2.bilateralFilter(frame,5,250,250)
    frame3=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    ret,thresh=cv2.threshold(frame3,5,255,cv2.THRESH_BINARY_INV)
    edges=cv2.Canny(frame2,75,200)
    contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_list=[]
    for contour in contours:
        approx=cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area=cv2.contourArea(contour)
        if ((len(approx)>10) & (area>500)):
            contours_list.append(contour)
    cv2.drawContours(thresh,contours_list,-1,(255,255,255),2)
    cv2.imshow("detected",thresh)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()