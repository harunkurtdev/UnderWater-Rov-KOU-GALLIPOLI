# gerekli paketleri içe aktarın
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # şekil adını başlat ve konturu yaklaştır
        shape = "unidentified"
        print(str(c))
        peri = cv2.arcLength(c, True)
        print(peri)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        #approx = cv2.approxPolyDP(c, peri, True)

        #şekil düz bir çizgi ise
        if len(approx) == 2:
            shape = "Line"

        # şekil bir üçgense, 3 köşesi olacaktır
        if len(approx) == 3:
            shape = "triangle"

        # şeklin 4 köşesi varsa, kare veya
        # dikdörtgen şeklindedir
        elif len(approx) == 4:
            # konturun sınırlayıcı kutusunu hesaplayın ve en boy oranını hesaplamak için
            # sınırlayıcı kutuyu kullanın
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # bir kare, yaklaşık olarak bire eşit bir en boy oranına sahip olacaktır, aksi takdirde şekil bir dikdörtgendir
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # şekil bir beşgen ise, 5 köşesi olacaktır
        elif len(approx) == 5:
            shape = "pentagon"

        # Aksi takdirde, şeklin bir daire olduğunu varsayarız
        else:
            shape = "circle"

        # şeklin adını döndür
        return shape

if __name__ == '__main__':
    s=ShapeDetector()
    img = cv2.imread('circles.png', 0)
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    c = contours[0]
    M = cv2.moments(c)
    print(M)
    s=s.detect(c)
    print(s)
    cX = int((M["m10"] / M["m00"]) )
    cY = int((M["m01"] / M["m00"]) )
    c = c.astype("int")
    cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
    cv2.putText(img, s, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()