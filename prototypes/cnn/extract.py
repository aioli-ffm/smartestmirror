#!/usr/bin/python

import cv2
import glob
import os

cascPath = "./haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascPath)                

files = glob.glob("./all/*.jpg")

try:
    os.mkdir("./all_extracted/")
except:
    print "Could not create dir"

for f in files:
    img = cv2.imread(f)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        patch = img[y:y+h, x:x+w,:]
        cv2.imwrite("./all_extracted/extracted_%s" % (f.split('/')[-1]), patch)

