import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#ret, frame = cap.read()
circles_saved = None
circles = None
# red Snooker
# lowerColorBGR = np.array([0,0,100])
# upperColorBGR = np.array([100,100,180])

lowerColorBGR = np.array([0, 0, 100])
upperColorBGR = np.array([100, 100, 180])

ret = True
while ret:

    while circles is None:
        ret, frame = cap.read()
        # masked background
        frame_masked = cv2.inRange(frame, lowerColorBGR, upperColorBGR)
        frame_masked = cv2.medianBlur(frame_masked,9) # in case no circle catched
        # find circle
        circles = cv2.HoughCircles(frame_masked,cv2.HOUGH_GRADIENT,1,1,param1=10,param2=10,minRadius=0,maxRadius=20)

    for i in circles[0,:]:
        cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        txt = ('[' + str(i[0]) + ',' + str(i[1]) + ' r= ' + str(i[2]) + ']')
        cv2.putText(frame, txt, (10,40), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
    cv2.imshow('original', frame)
    cv2.imshow('remove background', frame_masked)

    circles = None

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllwindows()