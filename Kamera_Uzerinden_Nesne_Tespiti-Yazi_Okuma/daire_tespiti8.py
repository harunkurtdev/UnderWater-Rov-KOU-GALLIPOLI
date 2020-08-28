import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while (True):
    ret, frame=cap.read()
    bilateral_filtered_image = cv2.bilateralFilter(frame, 5, 175, 175)
    cv2.imshow('Bilateral', bilateral_filtered_image)

    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    cv2.imshow('Edge', edge_detected_image)

    contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.moments(contour)
        # if ((len(approx) > 8) and (len(approx) < 25) and (area >100 ) ):
        #     contour_list.append(contour)
        cv2.drawContours(frame, contour_list,  -1, (255,0,0), 2)
        cv2.imshow('Objects Detected',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()