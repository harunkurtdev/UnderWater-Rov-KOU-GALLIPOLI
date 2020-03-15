import pytesseract
import cv2
from PIL import Image
import pyttsx3
import numpy as np
 
pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
 
 
kaynak_yolu=""
def getText(img_yolu):
    img=cv2.imread(img_yolu)
    #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1,1),np.uint8)
    img = cv2.erode(img,kernel,iterations=1)
    img = cv2.dilate(img , kernel , iterations=1)
    img=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,2)
    cv2.imwrite('e.jpg',img)
    result = pytesseract.image_to_string(Image.open(img_yolu),lang="eng")
    print(result)
    return result
 
engine = pyttsx3.init()
engine.setProperty('rate', 120)
 
engine.say('{}'.format(getText("e.png")))
    
engine.runAndWait()