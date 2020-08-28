import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print ("Starting " + self.previewName)
        self.camPreview(self.previewName, self.camID)

    def camPreview(self,previewName, camID):
        cv2.namedWindow(previewName)
        cam = cv2.VideoCapture(camID)
        # cam.set(3,1920)
        cam.set(3,640)
        cam.set(4,480)
        # cam.set(4,1080)
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            cv2.imshow(previewName, frame)
            rval, frame = cam.read()
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break
        cv2.destroyWindow(previewName)



thread1 = camThread("Camera 1", 0)
#thread2 = camThread("Camera 2", 0)
thread1.start()
#thread2.start()
