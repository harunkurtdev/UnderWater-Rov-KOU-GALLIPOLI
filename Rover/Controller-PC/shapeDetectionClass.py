import cv2
import numpy as np

class ShapeDetection:

    def __init__(self):
        self.b=255
        self.g=0
        self.r=0

    def imgRead(self,img,imgContour,b=None,g=None,r=None):

        "resim üzerine çizdireceğimiz kare daire vb. şekillerin çizgi renklerini ayarlayabiliriz."
        if b!=None or g!=None or r!=None:
            pass
        self.img=img
        self.imgContour=imgContour

        imgGray=self.imgGrayF(img)
        imgBlur=self.imgGaussianBlurF(imgGray)
        imgCanny=self.imgCanny(imgBlur)

        shape= self.getContours(imgCanny)

        # circles=self.CircleDetection(imgGray)
        circles=0,0

        return shape,circles

    def imgGrayF(self,img):
        """
        Resmimizi Gri tonuna getirmemizi sağlar
        """
        self.imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return self.imgGray

    def imgGaussianBlurF(self,imgGray):
        """
        Gelen resmi Blur haline getirerek görünmez bir hale sokabilir
        GaussianBlur fonksiyonunu google dan araştırarak resimlere bakınız.
        """
        imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
        return imgBlur

    def imgMedianBlurF(self,imgGray):
        """
        Gelen Blur resmini daha görülebilir hale getirerek resimde seçme yapmamızı
        sağlar
        """
        imgBlur=cv2.medianBlur(imgGray,15)
        return imgBlur

    def imgCanny(self,imgBlur):
        """
        Resmimiz de kenar veyahut keskin hatlarını bularak göstermemize yarar bir resim
        elde etmemizi sağlar...
        """
        imgCanny=cv2.Canny(imgBlur,50,50)
        return imgCanny

    def CircleDetection(self,imgGray):
        blured = cv2.blur(imgGray,(3,3))
        circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=30, minRadius=20,
                                   maxRadius=50)

        if circles is not None:
            # dairelerin indexlerine göre sayı adetini alırız
            circles = np.round(circles[0, :]).astype("int")

            for (dX, dY, r) in circles:

                cv2.circle(self.imgContour, (dX, dY), r, (0, 0, 255), 4)
                cv2.line(self.imgContour, (dX, dY),
                         (int(self.imgContour.shape[1] / 2), int(self.imgContour.shape[0] / 2)), (0, 255, 0), 1)

                # cv2.rectangle(self.imgContour,(dX-r,dY+r),(dX+r,dY-r),(255,0,0),3)

                yield dX,dY
    def getContours(self,imgCanny):
        """
        getContours fonksiyonu bizden Canny alarak kenarları tespit edilen resim üzerinden
        findContours fonksiyonu cisimin kenarlarını bularak bize geri dönzerir
        """
        cv2.circle(self.imgContour, (int(self.imgContour.shape[1] / 2), int(self.imgContour.shape[0] / 2)), 1, (255, 0, 0), 5)
        cv2.line(self.imgContour, (int(self.imgContour.shape[1] / 2)-50, int(self.imgContour.shape[0] / 2)), (int(self.imgContour.shape[1] / 2)+50, int(self.imgContour.shape[0] / 2)), (0, 255, 0), 1)
        cv2.line(self.imgContour, (int(self.imgContour.shape[1] / 2), int(self.imgContour.shape[0] / 2)-25), (int(self.imgContour.shape[1] / 2), int(self.imgContour.shape[0] / 2)+25), (0, 255, 0), 1)

        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:

            "contours bize list olarak döndükten sonra contourArea sayesinde pixellerinin yerlerini alıyoruz"
            area = cv2.contourArea(cnt)
            M = cv2.moments(cnt)
            objbool=False

            if area > 500:  # 500 pixellerin altındakiler dikkate alınmaz
                "contourArea sayesinde oluşan pixelleri drawContours sayesinde cismin etrafını ciziyoruz" \
                "imgContour imgRead fonksiyonu içerisinde img karesi üzerinden kopyalanıyor" \
                "-1, tüm konturları çizmemiz gerektiğini gösterir"
                cv2.drawContours(self.imgContour, cnt, -1, (255, 0, 0), 3)

                "konturumuzun kapalı olduğunu teyit ediyoruz"
                perimeter = cv2.arcLength(cnt, True)

                "Bu yöntem, yaklaşık kontür sayısını bulmak için kullanılır." \
                "approx nesnelerimizin kenar sayısını vermektedir."
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                "cisimlerimizin kenar sayını objCorner içerisine atadık"
                objCorner = len(approx)
                # print("objCorner")
                "Burada nesnenin etrafına çizeceğimiz sınırlayıcı kutumuzun değerlerini elde ederiz."
                x, y, w, h = cv2.boundingRect(approx)
                # if objCorner == 3:
                #     objectType = 'Triangle'
                # elif objCorner == 4:
                #     aspectRatio = float(w) / float(h)
                #     if aspectRatio > 0.95 and aspectRatio < 1.05:
                #         objectType = 'Square'
                #     else:
                #         objectType = "Rectangle"
                if objCorner > 6:

                    objectType = 'Circle'

                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(self.imgContour, (cX, cY), 5, (255, 255, 255), -1)

                    yield cX,cY

                else:
                    objectType = "None"

                cv2.rectangle(self.imgContour, (x, y), (x + w, y + h), (0, 255, 0),
                              2)  # Draw a rectange around the shapes
                cv2.putText(self.imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 0), 2)
    def objectDetection(self,imgRed,frame):
        (contours, hierarchy) = cv2.findContours(imgRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img=cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                yield img, x,y

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        print("çıktı")

if __name__ == '__main__':
    print(cv2.__version__)
    cam = cv2.VideoCapture(0)
    shape = ShapeDetection()
    while True:
        ret,img=cam.read()
        frame=img.copy()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        # lower_blue = np.array([110,50,50])
        # lower_blue = np.array([0,191,0])#Sualtın da ki nesne
        lower_blue = np.array([91, 159, 255])  # Sualtında ki Çember
        # upper_blue = np.array([130,255,255])
        # upper_blue = np.array([15,255,255])#Sualtında ki nesne
        upper_blue = np.array([112, 255, 255])  # Sualtında ki Çember
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        # resimGray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        # cv.imshow('frame', frame)
        cv2.imshow('mask', mask)
        # cv2.imshow('mask', resimGray)

        h,w,_=img.shape
        h=int(h/2)
        w=int(w/2)
        _,imgContour=cam.read()
        _,img0=cam.read()
        data=None
        shapeCircle,Circles=shape.imgRead(img=res,imgContour=imgContour)
        object=False
        x,y=None,None
        for cX,cY in shapeCircle:
            # print(f"sekil dairenin X ekseni {cX} y ekseni {cY}")
            for dX,dY in Circles :
                # print(f"Dairenin X ekseni {dX} y ekseni {dY}")
                if (abs(cX-dX)<50) and (abs(dY-cY)<50):
                    # print("daire bulundu")
                    x=int((cX+dX)/2)
                    y=int((dX+cY)/2)
                    data={
                        "sekilX":cX,
                        "sekilY":cY,
                        "daireX":dX,
                        "daireY":dY
                    }
                    object=True
                    # print(data)

        if object==True:
            # print(data)
            if w>x and h>y:
                print("x ekseninde sola doğru - y ekseninde yukarı doğru çıkıyor")
            if x>w and h>y:
                print("x ekseninde sağa doğru dönüyor - y ekseninde yukarı doğru çıkıyor")
            if w>x and y>h:
                print("x ekseninde sola doğru dönüyor - y ekseninde aşağı doğru iniyor")
            if x>w and y>h:
                print("x ekseninde sağa doğru dönüyor - y ekseninde aşağı doğru iniyor")
        else:
            print("tarama ya geçiliyor")

        cv2.imshow("Resim", imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break
