import cv2
import pyrealsense2 as rs

class BoatImageProcessing:
    def __init__(self, isColor, finishedProduct):
        super().__init__()

        self.isColor = isColor
        self.finalImage = None
        self.finishedProduct = finishedProduct

        self.functionList = {
            'noChange' : self.noChange,
            'blur' : self.toBlurImage,
            'grey' : self.toGreyImage,
            'cannyEdge' : self.toCannyEdge
        }


    def setImage(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.processImage()

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
            
    def toBlurImage(self, image, ksize = (5,5)):
        blurred = cv2.blur(image, ksize)

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
        blur = self.toBlurImage(grey)
        if(threshold2 >= threshold1):
            cannyEdge = cv2.Canny(blur, threshold1, threshold2)
        else:
            cannyEdge = cv2.Canny(blur, threshold2, threshold1)

        return(cannyEdge)
