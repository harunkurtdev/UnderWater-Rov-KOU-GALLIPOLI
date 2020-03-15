#Bu nesnelerin boyutunu algılayan programdır

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
# Verilen iki noktanın orta noktasını bulmak için bir işlev
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# Değişkenleri tanımlayın
image = cv2.imread("resim.jpg", flags=cv2.IMREAD_COLOR)
scale_percent = 15
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# Konturları soldan sağa doğru sıralayın ve
#(cnts,boundingBoxes) = contours.sort_contours(cnts)
pixelsPerMetric = 1.0
orig = image.copy()
# konturlar üzerinde ayrı ayrı döngü
for c in cnts:
	# Kontur yeterince büyük değilse, yoksay
	if cv2.contourArea(c) < 10:
		continue
	# Konturun döndürülmüş sınırlayıcı kutusunu hesaplayın
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	# Konturdaki noktaları görünecek şekilde sıralayın
	# Sol üstte, sağ üstte, sağ altta ve sol altta
	# ardından döndürülmüş sınırlamanın ana hatlarını çizin
	# kutu
	box = perspective.order_points(box)
	cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

	# orijinal noktaların üzerine gelin ve çizin
	for (x, y) in box:
		cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

	# Sipariş edilen sınırlama kutusunu açın, sonra orta noktayı hesaplayın
	# sol üst ve sağ üst koordinatlar arasında, ardından
	# sol alt ve sağ alt koordinatlar arasındaki orta nokta
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)

	# Sol üst ve sağ üst noktalar arasındaki orta noktayı hesaplayın,
	# ardından sağ üst ve sağ alt arasındaki orta nokta
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)

	# görüntüdeki orta noktaları çizin
	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	# Orta noktalar arasında çizgi çizme
	cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(255, 0, 255), 2)
	cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(255, 0, 255), 2)

	# Orta noktalar arasındaki Öklid mesafesini hesaplayın
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

	# Nesnenin boyutunu hesaplama
	dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric
	# Yanındaki nesnenin boyutunu görüntüleme
	cv2.putText(orig, "{:.1f}px".format(dimA),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}px".format(dimB),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
#Görüntüdeki tüm nesnelerin boyutunu ve orta noktalarını görüntüleme
cv2.imshow("Image", orig)
cv2.waitKey(0)
