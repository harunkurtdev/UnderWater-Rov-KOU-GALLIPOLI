import numpy as np
import cv2

# En yeni çalışan kamerayı alın
def getNumCam():
    num = 0
    while True:
        cp = cv2.VideoCapture(num)
        if cp.isOpened():
            num += 1
        else:
            break
    return num

currCam = 0
cap = cv2.VideoCapture(currCam)
cap.set(3,1920)
cap.set(4,1080)
capNum = 0

while(True):
    
    # Kare kare yakalama
    ret, frame = cap.read()
    # Ortaya çıkan kareyi görüntüleyin ve kullanıcı girişine göre çeşitli işlemler gerçekleştirin (resim çekmek veya kamera değiştirmek gibi)
    cv2.imshow('frame', frame)
    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break
    if k & 0xFF == ord('c'):
        cv2.imwrite("frame%d.jpg" % capNum, frame)
        capNum += 1;
    if k & 0xFF == ord('n'):
        cap.release()
        currCam += 1
        if currCam >= getNumCam():
            currCam = 0
        cap = cv2.VideoCapture(currCam)
        cap.set(3,1920)
        cap.set(4,1080)


# Her şey bittiğinde, yakalamayı serbest bırakın
cv2.destroyAllWindows()
