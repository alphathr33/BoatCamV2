import cv2
import numpy as np
import pyrealsense2 as rs

class BoatImageProcessing:
    def __init__(self, finishedProduct):
        super().__init__()

        self.isColor = None
        self.finalImage = None
        self.finishedProduct = finishedProduct

        self.functionList = {
            'noChange' : self.noChange,
            'blur' : self.toBlurImage,
            'grey' : self.toGreyImage,
            'cannyEdge' : self.toCannyEdge
        }

        self.defaultDepthClose = 0
        self.defaultDepthFar = 10
        self.depthClose = self.defaultDepthClose
        self.depthFar = self.defaultDepthFar

        self.defaultKSize = (5,5)
        self.ksize = self.defaultKSize

        self.defaultThreshold1 = 0
        self.defaultThreshold2 = 0
        self.threshold1 = self.defaultThreshold1
        self.threshold2 = self.defaultThreshold2

    def setIsColor(self, value):
        self.isColor = value

    def setImage(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.processImage()

    def setDepthClose(self, value):
        if(self.depthFar >= value):
            self.depthClose = value
        else:
            self.depthClose = self.depthFar

    def setDepthFar(self, value):
        if(self.depthClose <= value):
            self.depthFar = value
        else:
            self.depthFar = self.depthClose

    def setKSize(self, value):
        if(type(value) == type(self.ksize)):
            self.ksize = value
        elif(type(value) == int):
            self.ksize = (value, value)
        elif(type(value) == float):
            self.ksize = (int(value), int(value))
        else:
            raise Exception('Wrong type for KSize')

    def setThreshold1(self, value):
        if(self.threshold2 >= value):
            self.threshold1 = value
        else:
            self.threshold1 = self.threshold2

    def setThreshold2(self, value):
        if(self.threshold1 <= value):
            self.threshold2 = value
        else:
            self.threshold2 = self.threshold1

    def getImage(self):
        try:
            return(self.finalImage)
        except:
            return(self.image)


    def processImage(self):
        try:
            self.finalImage = self.functionList[self.finishedProduct](self.image)

        except KeyError:
            print('Cant process image like that')

    def noChange(self, image):
        return(image)
            
    def toBlurImage(self, image, ksize = (-1,-1)):
        if(ksize == (-1,-1)):
            self.ksize = self.defaultKSize
        else:
            self.ksize = ksize

        blurred = cv2.blur(image, self.ksize)

        return(blurred)

    def toGreyImage(self, image):
        grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        return(grey)

    def toCannyEdge(self, image, threshold1=0, threshold2=0):
        grey = self.toGreyImage(image)
        if(threshold1 == 0 and threshold2 == 0):
            med = np.median(grey)
            sigma = 0.33

            threshold1 = int(max(0, (1 - sigma) * med))
            threshold2 = int(min(255, (1 + sigma) * med))

        blur = self.toBlurImage(grey, self.ksize)
        if(threshold2 >= threshold1):
            cannyEdge = cv2.Canny(blur, threshold1, threshold2)
        else:
            cannyEdge = cv2.Canny(blur, threshold2, threshold1)

        return(cannyEdge)
