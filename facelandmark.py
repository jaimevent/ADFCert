"""

Sources:
https://medium.com/analytics-vidhya/facial-landmarks-and-face-detection-in-python-with-opencv-73979391f30e
https://www.datacamp.com/community/tutorials/face-detection-python-opencv

"""

#import all necessary libraries

#import numpy as np
import cv2
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#used for accessing url to download files
import urllib.request as urlreq
# used to access local directory
import os
import hashlib

class FaceLandMark:

    LBFmodel_url = "https://github.com/kurnianggoro/GSOC2017/raw/master/data/lbfmodel.yaml"
    #save facial landmark detection model's name as LBFmodel
    LBFmodel = "lbfmodel.yaml"

    image = None
    image_rgb = None
    image_grey = None
    faces_rects = 0
    landMarksArr = ""

    #Init method
    def __init__(self, image):
        if image is not None:
            # check if file is in working directory, otherwise download it
            if not (self.LBFmodel in os.listdir(os.curdir)):
                # download picture from url and save locally as lbfmodel.yaml, < 54MB
                urlreq.urlretrieve(self.LBFmodel_url, self.LBFmodel)

            #read the image
            self.image = cv2.imread(image)
            #plot image with matplotlib package
            plt.imshow(self.image)
        else:
            print("Error")

    #Method to create the hash of the landmarks, if found
    def createHashImage(self):
        if self.findFaces() > 0:
            self.landMarksArr = self.findLandmarks()
            if len(self.landMarksArr) > 0:
                return hashlib.sha256(str(self.landMarksArr).encode()).hexdigest()
            else:
                return False
        else:
            return False

    #Searches for faces in the image given
    def findFaces(self):
        # convert image to RGB colour
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # plot image with matplotlib package
        plt.imshow(self.image_rgb)

        # convert image to Grayscale
        self.image_gray = cv2.cvtColor(self.image_rgb, cv2.COLOR_BGR2GRAY)

        plt.imshow(self.image_gray, cmap = "gray")

        haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

        self.faces_rects = haar_cascade_face.detectMultiScale(self.image_gray);

        #Draw rectangle around faces
        for face in self.faces_rects:
            #save the coordinates in x, y, w, d variables
            (x,y,w,d) = face
            # Draw a white coloured rectangle around each face using the face's coordinates
            # on the "image_template" with the thickness of 2
            cv2.rectangle(self.image_rgb,(x,y),(x+w, y+d),(0, 255, 0), 2)

        #plt.axis("off")
        plt.imshow(self.image_rgb)

        return len(self.faces_rects)

    def findLandmarks(self):
        # create an instance of the Facial landmark Detector with the model
        landmark_detector  = cv2.face.createFacemarkLBF()
        landmark_detector.loadModel(self.LBFmodel)

        #Detect landmarks on "image_gray"
        _, landmarks = landmark_detector.fit(self.image_gray, self.faces_rects)

        arr = []
        for landmark in landmarks:
            for x,y in landmark[0]:
                #push into array
                arr.append([float(x), float(y)])
                #Draw landmarks dots
                cv2.circle(self.image_rgb, (int(x), int(y)), 1, (255, 0, 0), 5)

        plt.axis("off")
        plt.imshow(self.image_rgb)

        plt.savefig('./output/test.jpg')

        return arr
