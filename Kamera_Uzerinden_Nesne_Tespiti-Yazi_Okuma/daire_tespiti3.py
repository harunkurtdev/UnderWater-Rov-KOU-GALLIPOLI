import imutils
import cv2
import numpy as np
cap = cv2.VideoCapture(0)##change this later to the name of the video


while True:
    try:
        ret, image = cap.read()
        ####first detect the cirle and decide ROI
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        low = np.array([0,90,100], dtype=np.uint8)
        high = np.array([9, 200, 190], dtype=np.uint8)

        mask = cv2.inRange(hsv, low, high)
        res = cv2.bitwise_and(image,image, mask= mask)
        cv2.imshow("res", res)


        ##then find the extreme
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.threshold(gray, 0, 120, cv2.THRESH_BINARY)[1]# why do we have here a one
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        # find contours in thresholded image, then grab the largest

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) == 0:
            raise ValueError
        c = max(cnts, key=cv2.contourArea)

        cv2.imshow("th", thresh)
        # determine the most extreme points along the contour
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        ##ma = cv2.minAreaRect(arr);
        ##bp = cv2.boxPoints(ma)

        cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
        cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
        cv2.circle(image, extRight, 8, (0, 255, 0), -1)
        cv2.circle(image, extTop, 8, (255, 0, 0), -1)
        cv2.circle(image, extBot, 8, (255, 255, 0), -1)
        # show the output image

        centrex = (extLeft[0] + extRight[0] + extTop[0]+ extBot[0])//4
        centrey = (extLeft[1] + extRight[1] + extTop[1]+ extBot[1])//4
        centre = (centrex, centrey)

        cv2.circle(image, centre, 8, (0, 0, 255), -1)
        print(centre)

        cv2.imshow("Image", image)
        if cv2.waitKey(1) &0xff == 27:
            break
    except ValueError:
        print("max is empty")
cap.release()
cv2.destroyAllWindows()