import cv2
import numpy

scalingFactor = 2
objectHSVLowerLimit = numpy.array([0,60,32]) #human skin lower limit hsv
objectHSVUpperLimit = numpy.array([180,255,255]) #human skin upper limit hsv

class ObjectTracking(object):
    def __init__(self, scalingFactor):
        self.capture = cv2.VideoCapture(0)
        #self.subtractor = cv2.createBackgroundSubtractorMOG2()
        ignore, self.frame = self.capture.read()
        #scaling for the frame that was captured
        self.scalingFactor = scalingFactor
        self.frame = cv2.resize(self.frame, None, fx=self.scalingFactor, fy=scalingFactor, interpolation=cv2.INTER_AREA)
        cv2.namedWindow('tracking')
        cv2.setMouseCallback('tracking', self.mouse_tracking)
        self.selection = None
        self.dragStart = None
        self.trackingState = 0

    def mouse_tracking(self, event, x, y, flags, param):
        x,y = numpy.int16([x,y]) #!!

        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragStart = (x,y)
            self.trackingState = 0

        #check for user defined region has init
        if self.dragStart:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.frame.shape[:2]
                xstart, ystart = self.dragStart
                xmax, ymax = numpy.maximum(0, numpy.minimum([xstart, ystart], [x,y])) #!!
                xmin, ymin = numpy.minimum([w,h], numpy.maximum([xstart, ystart], [x,y]))#!!
                #reset
                self.selection = None
                #finzalize selection
                if xmin-xmax > 0 and ymin-ymax >0:
                    self.selection = (xmax, ymax, xmin, ymin)
            else:
                 self.dragStart = None
                 if self.selection is not None:
                     self.trackingState = 1

    def start_tracking(self, lowerLimit, upperLimit):
        while(True):
            _, self.frame = self.capture.read()
            self.frame = cv2.resize(self.frame, None, fx=self.scalingFactor,
                                    fy = self.scalingFactor, interpolation=cv2.INTER_AREA)
            vis = self.frame.copy()
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lowerLimit, upperLimit)
            if self.selection:
                xmax, ymax, xmin, ymin = self.selection
                self.trackWindow = (xmax, ymax, xmin-xmax, ymin-ymax)
                #region of interest
                hsvROI = hsv[ymax:ymin, xmax:xmin]
                maskROI = mask[ymax:ymin, xmax:xmin]
                #histogram using roi in hsv using mask
                histogram = cv2.calcHist([hsvROI], [0], maskROI, [16], [0,180])#!!
                cv2.normalize(histogram, histogram, 0, 255, cv2.NORM_MINMAX);
                self.histogram = histogram.reshape(-1)
                visROI = vis[ymax:ymin, xmax:xmin]
                cv2.bitwise_not(visROI, visROI)
                vis[mask == 0] = 0 #!!

            if self.trackingState == 1:
                self.selection = None
                hsvBackProjection = cv2.calcBackProject([hsv], [0], self.histogram, [0,180],1)
                hsvBackProjection &= mask
                #termination
                termCriteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
                trackBox, self.trackWindow = cv2.CamShift(hsvBackProjection, self.trackWindow, termCriteria)
                cv2.ellipse(vis, trackBox, (0,255,0),2)

            cv2.imshow('tracking', vis)
            keyPressed = cv2.waitKey(5)
            if keyPressed == 27: #ASCII 27 == 'ESC'
                break

        #terminate
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    ObjectTracking(scalingFactor).start_tracking(objectHSVLowerLimit, objectHSVUpperLimit)