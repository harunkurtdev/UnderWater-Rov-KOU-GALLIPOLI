
import cv2
import numpy as np


def motorSpeedMap( x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def opencvDistanceShow(img,distanceFront,distanceRight,distanceLeft,distanceDown):
    # cv2.rectangle(img, (110, 100), (90, 200), (255, 255, 255), 3)

    distanceFrontWall=motorSpeedMap(distanceFront,0,450,255,0)
    distanceRightWall=motorSpeedMap(distanceRight,0,450,255,0)
    distanceLeftWall=motorSpeedMap(distanceLeft,0,450,255,0)
    distanceDownWall=motorSpeedMap(distanceDown,0,450,255,0)

    if(50>distanceFront):
        cv2.line(img, (90, 90), (210, 90), (0, 0, distanceFrontWall), 3)
        # cv2.line(img, (80, 80), (220, 80), (255, 0, 0), 3)
        # cv2.line(img, (70, 60), (230, 60), (255, 0, 0), 3)
        # cv2.line(img, (60, 40), (240, 40), (255, 0, 0), 3)
    elif(100>distanceFront>=50):
        cv2.line(img, (90, 90), (210, 90), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (80, 80), (220, 80), (0, 0, distanceFrontWall), 3)
        # cv2.line(img, (70, 60), (230, 60), (255, 0, 0), 3)
        # cv2.line(img, (60, 40), (240, 40), (255, 0, 0), 3)
    elif(200>distanceFront>=100):
        cv2.line(img, (90, 90), (210, 90), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (80, 80), (220, 80), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (70, 60), (230, 60), (0, 0, distanceFrontWall), 3)
        # cv2.line(img, (60, 40), (240, 40), (255, 0, 0), 3)
    elif(300>distanceFront>=200):
        cv2.line(img, (90, 90), (210, 90), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (80, 80), (220, 80), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (70, 60), (230, 60), (0, 0, distanceFrontWall), 3)
        cv2.line(img, (60, 40), (240, 40), (0, 0, distanceFrontWall), 3)

    if (50 > distanceRight):
        cv2.line(img, (90, 90), (90, 210), (distanceRightWall, 0, 0), 3)
        "----- Eski Sağ düzeni-------"
        # cv2.line(img, (90, 90), (90, 210), (255, 0, 0), 3)
        # cv2.line(img, (80, 80), (80, 220), (255, 0, 0), 3)
        # cv2.line(img, (60, 70), (60, 230), (255, 0, 0), 3)
        # cv2.line(img, (40, 60), (40, 240), (255, 0, 0), 3)
    elif (100 > distanceRight >= 50):
        cv2.line(img, (90, 90), (90, 210), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (80, 80), (80, 220), (distanceRightWall, 0, 0), 3)
    elif (200 > distanceRight >= 100):
        cv2.line(img, (90, 90), (90, 210), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (80, 80), (80, 220), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (60, 70), (60, 230), (distanceRightWall, 0, 0), 3)
    elif (300 > distanceRight >= 200):
        cv2.line(img, (90, 90), (90, 210), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (80, 80), (80, 220), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (60, 70), (60, 230), (distanceRightWall, 0, 0), 3)
        cv2.line(img, (40, 60), (40, 240), (distanceRightWall, 0, 0), 3)

    if (50 > distanceLeft):
        cv2.line(img, (210, 90), (210, 210), (0, distanceLeftWall, 0), 3)
        "----- Eski Sağ düzeni-------"
        # cv2.line(img, (210, 90), (210, 210), (255, 0, 0), 3)
        # cv2.line(img, (220, 80), (220, 220), (255, 0, 0), 3)
        # cv2.line(img, (240, 70), (240, 230), (255, 0, 0), 3)
        # cv2.line(img, (260, 60), (260, 240), (255, 0, 0), 3)
    elif (100 > distanceLeft >= 50):
        cv2.line(img, (210, 90), (210, 210), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (220, 80), (220, 220), (0, distanceLeftWall, 0), 3)
    elif (200 > distanceLeft >= 100):
        cv2.line(img, (210, 90), (210, 210), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (220, 80), (220, 220), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (240, 70), (240, 230), (0, distanceLeftWall, 0), 3)
    elif (300 > distanceLeft >= 200):
        cv2.line(img, (210, 90), (210, 210), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (220, 80), (220, 220), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (240, 70), (240, 230), (0, distanceLeftWall, 0), 3)
        cv2.line(img, (260, 60), (260, 240), (0, distanceLeftWall, 0), 3)


    if (50 > distanceDown):
        cv2.line(img, (90, 210), (210, 210), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        "----- Eski Sağ düzeni-------"
        # cv2.line(img, (90, 210), (210, 210), (255, 255, 255), 1)
        # cv2.line(img, (80, 220), (220, 220), (255, 255, 255), 1)
        # cv2.line(img, (60, 240), (240, 240), (255, 255, 255), 1)
        # cv2.line(img, (40, 260), (260, 260), (255, 255, 255), 1)
    elif (100 > distanceDown >= 50):
        cv2.line(img, (90, 210), (210, 210), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (80, 220), (220, 220), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
    elif (200 > distanceDown >= 100):
        cv2.line(img, (90, 210), (210, 210), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (80, 220), (220, 220), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (60, 240), (240, 240), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
    elif (300 > distanceDown >= 200):
        cv2.line(img, (90, 210), (210, 210), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (80, 220), (220, 220), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (60, 240), (240, 240), (distanceDownWall, distanceDownWall, distanceDownWall), 3)
        cv2.line(img, (40, 260), (260, 260), (distanceDownWall, distanceDownWall, distanceDownWall), 3)

    return  img

def mainDistance(front,down,right,left):

    rov = cv2.imread("rov.PNG")
    image = np.zeros(shape=[300, 300, 3], dtype="uint8")
    img1 = image
    img2 = rov
    # I want to put logo on top-left corner, So I create a ROI
    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    img1[110:rows+110, 100:cols+100] = dst

    img=opencvDistanceShow(image,i,i,i,i)

    return img

#
# rov=cv2.imread("rov.PNG")
# image=np.zeros(shape=[300,300,3],dtype="uint8")
# print(rov.shape)
if __name__ == '__main__':

    rov = cv2.imread("rov.PNG")
    image = np.zeros(shape=[300, 300, 3], dtype="uint8")
    img1 = image
    img2 = rov
    # I want to put logo on top-left corner, So I create a ROI
    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    img1[110:rows+110, 100:cols+100] = dst
    # cv2.imshow('res', img1)
    for i in range(0,450):
        img=opencvDistanceShow(image,i,i,i,i)
    # newimg=cv2.add(rov,img)
        cv2.imshow("image",img)

    # cv2.imshow("rov",rov)
    # cv2.imshow("aşsd",newimg)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
