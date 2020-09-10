import cv2
import numpy as np

cap=cv2.VideoCapture(0)

while (True):
    # goruntu yakalama
    ret, frame = cap.read()

    # goruntuyu grilestir

    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # goruntuyu blurlastir
    gray = cv2.GaussianBlur(gray, (5, 5), 0);
    gray = cv2.medianBlur(gray, 5)

    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 3.5)

    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.erode(gray, kernel, iterations=1)

    gray = cv2.dilate(gray, kernel, iterations=1)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 400, param1=40, param2=45, minRadius=0,
                               maxRadius=0)  # python3 icin
    # circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 400, param1=40, param2=45, minRadius=0, maxRadius=0) #python2 icin
    # kalibre
    # daireyi isle

    if circles is not None:
        # x y kordinatlarini integer cevir
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:

            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            print("X kordinat: ")
            print(x)
            print("Y Kordinat: ")
            print(y)
            print("Radius: ")
            print(r)
            cv2.imshow('frame', output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

