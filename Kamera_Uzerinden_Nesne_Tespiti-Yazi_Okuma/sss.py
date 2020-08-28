import numpy as np
import cv2

class Shp:
    def getContours(self,img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in contours:
            area = cv2.contourArea(cnt)  # This is used to find the area of the contour.
            print("Area: ", area)
            if area > 500:  # The areas below 500 pixels will not be considered
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0),
                                 3)  # -1 denotes that we need to draw all the contours
                perimeter = cv2.arcLength(cnt, True)  # The true indicates that the contour is closed
                print("Perimeter: ", perimeter)
                approx = cv2.approxPolyDP(cnt, 0.02 * perimeter,
                                          True)  # This method is used to find the approximate number of contours
                print("Corner Points: ", len(approx))
                objCorner = len(approx)
                x, y, w, h = cv2.boundingRect(
                    approx)  # In this we get the values of our bounding box that we will draw around the object

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
                else:
                    objectType = "None"

                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a rectange around the shapes
                cv2.putText(imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 0), 2)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while True:
        ret, img = cam.read()
        imgContour = img.copy()

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
        imgCanny = cv2.Canny(imgBlur, 50, 50)
        Shp.getContours(imgCanny)

        cv2.imshow("Resim", imgContour)
        # cv2.imwrite("Resim.png", imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break