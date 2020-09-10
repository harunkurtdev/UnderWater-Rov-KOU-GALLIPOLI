import imutils
import numpy as np
import cv2
import operator

cam=cv2.VideoCapture(0)
while True:
    _,image = cam.read()
    image = imutils.resize(image, width=600)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(image)
    h.fill(255)
    v.fill(255)

    h = cv2.equalizeHist(h)

    hsv_image = cv2.merge([h, s, v])

    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


    #Convert to Gray
    #Hough works on single channel
    #convert to Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Blur  (13x13) SigmaX= 7 to smoothen image
    #Helps Avoid detecting same circular object Multiple times
    blur = cv2.GaussianBlur(gray,(3,3), 3)
    canny = cv2.Canny(blur,50,100)
    erode = cv2.erode(canny,(1,1),iterations=3)
    dilate = cv2.dilate(canny,None,iterations=1)


    #Detect Circle on Blured Grayscale Image (Minimum distance between centers=10 minimum Radius =5 )
    circles =  cv2.HoughCircles(dilate,cv2.HOUGH_GRADIENT,1,10,param2=40)
    cv2.imshow("GrayBlurerdImg",dilate)
    # d= []

    def findCircularObjects(circles):
        try:
            circlestodelete = circles

            xm, ym, rm = (max(circlestodelete, key=operator.itemgetter(2)))
            print(rm)
            cv2.circle(image, (xm, ym), rm, (0, 225, 0), 4)
            maxx = np.array([xm, ym, rm])
            circlestodelete = np.array([x for x in circlestodelete if not np.all(x == maxx)])
            print(len(circlestodelete))
            # Delete all circles in side current max circle found
            for (x, y, r) in circlestodelete:
                d = (np.sqrt((x - xm) ** 2 + (y - ym) ** 2))
                if (rm >= d):
                    print(rm, d + r)
                    maxx = np.array([x, y, r])
                    # These circles's center is inside others and we wont plot them
                    #cv2.circle(image, (x, y), r, (0, 225, 225), 4)
                    circlestodelete = np.array([x for x in circlestodelete if not np.all(x == maxx)])
                    print(len(circlestodelete))
            if len(circlestodelete > 0):
                findCircularObjects(circlestodelete)
        except TypeError:
            print("Not Found Circle")

    # Covert to iterate-able integers for x,y and radius
    try :
        circles = np.round( circles[0, :]).astype("int")
        findCircularObjects(circles)
    except TypeError:
        print("Not Found Circle")

    #add multiple images to output using np.hstack if needed Only with same Dimentions
    cv2.imshow("DetectedImage", np.hstack([image]))
    # cv2.imwrite(r'C:\Users\admin\Desktop\circlesdetected.jpg', image)

    cv2.waitKey(1)