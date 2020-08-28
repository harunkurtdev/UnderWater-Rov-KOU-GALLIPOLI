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

        self.getContours(imgCanny)
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

    def getContours(self,imgCanny):
        """
        getContours fonksiyonu bizden Canny alarak kenarları tespit edilen resim üzerinden
        findContours fonksiyonu cisimin kenarlarını bularak bize geri dönzerir
        """
        cv2.circle(imgContour, (int(imgContour.shape[1] / 2), int(imgContour.shape[0] / 2)), 1, (255, 0, 0), 5)
        cv2.line(imgContour, (int(imgContour.shape[1] / 2)-50, int(imgContour.shape[0] / 2)), (int(imgContour.shape[1] / 2)+50, int(imgContour.shape[0] / 2)), (0, 255, 0), 1)
        cv2.line(imgContour, (int(imgContour.shape[1] / 2), int(imgContour.shape[0] / 2)-25), (int(imgContour.shape[1] / 2), int(imgContour.shape[0] / 2)+25), (0, 255, 0), 1)

        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:

            "contours bize list olarak döndükten sonra contourArea sayesinde pixellerinin yerlerini alıyoruz"
            area = cv2.contourArea(cnt)
            M = cv2.moments(cnt)

            if area > 500:  # 500 pixellerin altındakiler dikkate alınmaz
                "contourArea sayesinde oluşan pixelleri drawContours sayesinde cismin etrafını ciziyoruz" \
                "imgContour imgRead fonksiyonu içerisinde img karesi üzerinden kopyalanıyor" \
                "-1, tüm konturları çizmemiz gerektiğini gösterir"
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

                "konturumuzun kapalı olduğunu teyit ediyoruz"
                perimeter = cv2.arcLength(cnt, True)

                "Bu yöntem, yaklaşık kontür sayısını bulmak için kullanılır." \
                "approx nesnelerimizin kenar sayısını vermektedir."
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                "cisimlerimizin kenar sayını objCorner içerisine atadık"
                objCorner = len(approx)
                print("objCorner")
                "Burada nesnenin etrafına çizeceğimiz sınırlayıcı kutumuzun değerlerini elde ederiz."
                x, y, w, h = cv2.boundingRect(approx)
                if objCorner == 3:
                    objectType = 'Triangle'
                elif objCorner == 4:
                    aspectRatio = float(w) / float(h)
                    if aspectRatio > 0.95 and aspectRatio < 1.05:
                        objectType = 'Square'
                    else:
                        objectType = "Rectangle"
                elif objCorner > 4:
                    objectType = 'Circle'

                    blured = self.imgMedianBlurF(self.imgGray)
                    circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=30, minRadius=1,
                                           maxRadius=50)

                    if circles is not None:

                        # dairelerin indexlerine göre sayı adetini alırız
                        circles = np.round(circles[0, :]).astype("int")

                        for (x, y, r) in circles:
                            cv2.circle(imgContour, (x, y), r, (0, 0, 255), 4)
                            cv2.line(imgContour, (x, y), (int(imgContour.shape[1] / 2), int(imgContour.shape[0] / 2)), (0, 255, 0), 1)

                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                            cv2.circle(self.imgContour, (cX, cY), 5, (255, 255, 255), -1)

                else:
                    objectType = "None"

                cv2.rectangle(self.imgContour, (x, y), (x + w, y + h), (0, 255, 0),
                              2)  # Draw a rectange around the shapes
                cv2.putText(self.imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 0), 2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("çıktı")

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    shape = ShapeDetection()
    while True:
        ret,img=cam.read()
        _,imgContour=cam.read()

        shape.imgRead(img=img,imgContour=imgContour)
        cv2.imshow("Resim", imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break

