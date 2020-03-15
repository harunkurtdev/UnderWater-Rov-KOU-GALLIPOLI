import cv2
import numpy as np
num = 0
"""
while True:
    filename = "frame" + str(13) + ".jpg"
    img = cv2.imread(filename)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)

    img=cv2.drawKeypoints(gray,keypoints=kp,outImage=img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imwrite("sift_keypoints" + str(13) + ".jpg",img)
    #num += 1

"""    
while True:
    filename = str("resim") + ".jpg"
    #filename="resim.jpg"
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)

    # centroids bulun
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # köşeleri durdurmak ve hassaslaştırmak için kriterleri tanımlamak
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

    # Şimdi onları çiz
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    img[res[:,1],res[:,0]]=[0,0,255]
    img[res[:,3],res[:,2]] = [0,255,0]

    cv2.imwrite("subpixel" + str(15) + ".jpg",img)
    num += 1

