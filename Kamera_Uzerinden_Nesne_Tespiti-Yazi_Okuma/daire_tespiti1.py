import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.get(cv2.CAP_PROP_FPS)

t = 50
w = 640.0

last = 0
while True:
    ret, image = capture.read()

    img_height, img_width, depth = image.shape
    scale = w // img_width
    h = img_height * scale
    image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

    # Apply filters
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blured = cv2.medianBlur(grey, 15)

    # Compose 2x2 grid with all previews
    grid = np.zeros([2 * int(h), 2 * int(w), 3], np.uint8)
    grid[0:int(h), 0:int(w)] = image

    # We need to convert each of them to RGB from grescaled 8 bit format
    grid[int(h):2 *int(h), 0:int(w)] = np.dstack([cv2.Canny(grey, int(t) / 2, int(t))] * 3)
    grid[0:int(h), int(w):2 * int(w)] = np.dstack([blured] * 3)
    grid[int(h):2 * int(h), int(w):2 * int(w)] = np.dstack([cv2.Canny(blured, int(t) / 2, int(t))] * 3)

    #cv2.imshow('Resim 1', grid)

    sc = 1
    md = 30
    at = 40

    circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1, 20,param1=50, param2=30, minRadius=1, maxRadius=40)

    cv2.circle(image, (int(img_width / 2), int(img_height / 2)), 1, (255, 0, 0), 5)

    if circles is not None:

        # dairelerin indexlerine göre sayı adetini alırız
        circles = np.round(circles[0, :]).astype("int")

        # We care only about the first circle found.

        # circle = circles[0][0]
        # # #print(circle)
        # x, y = int(circle[0]), int(circle[1])
        #
        # # Draw dot in the center
        # "hedef dairenin x ve y kordinatları"
        # cv2.circle(image, (x, y), 1, (0, 0, 255), 5)
        # "bizim merkez kkonumu"
        # cv2.circle(image, (int(img_width/2),int(img_height/2)), 1, (255, 0, 0), 5)
        # ix=0
        # jy=0
        # for i in range(x):
        #     for j in range(y):
        #         if jy==y:
        #             print("dikey de kayma tamamlandı")
        #             print(jy)
        #     jy+=j
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 0, 255), 4)
            cv2.line(image,(x,y),(int(img_width/2),int(img_height/2)),(0,255,0),1)
        #     ix=0
        #     jy=0
        #     for i in range(x):
        #         for j in range(y):
        #             print("dikey de kayma")
        #             if jy==y:
        #                 print("dikey de kayma tamamlandı")
        #                 print(jy)
        #             jy+=j
        #         jy=0

    cv2.imshow('Resim', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        capture.release()
        break