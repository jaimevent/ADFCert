#import numpy as np
import cv2
import matplotlib.pyplot as plt
#used for accessing url to download files
import urllib.request as urlreq
# used to access local directory
import os

import glob
import itertools

def getFilenames(exts):
    fnames = [glob.glob(ext) for ext in exts]
    fnames = list(itertools.chain.from_iterable(fnames))
    return fnames

LBFmodel_url = "https://github.com/kurnianggoro/GSOC2017/raw/master/data/lbfmodel.yaml"
# save facial landmark detection model's name as LBFmodel
LBFmodel = "lbfmodel.yaml"

# check if file is in working directory
if not (LBFmodel in os.listdir(os.curdir)):
    # download picture from url and save locally as lbfmodel.yaml, < 54MB
    urlreq.urlretrieve(LBFmodel_url, LBFmodel)

mainArr = []

# get `.png` in  current folder and subfolders
exts = ["./dataset/*.png"]
images = getFilenames(exts)

iLoop = 1
for image in images:
    #read the image
    image = cv2.imread(image)

    #plot image with matplotlib package
    plt.imshow(image)

    # convert image to RGB colour
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # plot image with matplotlib package
    plt.imshow(image_rgb)

    # convert image to Grayscale
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

    # remove axes and show image
    plt.imshow(image_gray, cmap = "gray")

    haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    faces_rects = haar_cascade_face.detectMultiScale(image_gray);

    #Print the no. of faces found
    #print('Faces found: ', len(faces_rects))

    if(len(faces_rects) > 0):
        # create an instance of the Facial landmark Detector with the model
        landmark_detector  = cv2.face.createFacemarkLBF()
        landmark_detector.loadModel(LBFmodel)

        # Detect landmarks on "image_gray"
        _, landmarks = landmark_detector.fit(image_gray, faces_rects)

        for landmark in landmarks:
            arr = []
            for x,y in landmark[0]:
                #push into array
                arr.append(tuple([float(x), float(y)]))
        mainArr.append(tuple(arr))
    print("Face #", iLoop)
    iLoop = iLoop+1

print("result: ", len(mainArr))
print("result: set(): ", len(set(tuple(mainArr))))
