import numpy as np
import cv2

cam=cv2.VideoCapture(0)

while True:
    ret,frame=cam.read()

    cikti = frame.copy()
    # resimin renigini belirleriz
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # resim de blur blur getirmeisini sağlarız
    gray_blur = cv2.blur(gray, (3, 3))

    # tüm daireleri yakalamaya çalışırız
    daireler = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=40, minRadius=1, maxRadius=40)

    # daireler var ise
    if daireler is not None:
        # dairelerin indexlerine göre sayı adetini alırız
        daireler = np.round(daireler[0, :]).astype("int")

        # kare vedaire çizeirz
        for (x, y, r) in daireler:
            cv2.circle(cikti, (x, y), r, (0, 0, 255), 4)
            #cv2.rectangle(cikti, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), 4)


    cv2.imshow("Color", cikti)  # ekran rengi bundan kaynaklı

    cv2.waitKey(10)