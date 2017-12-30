#!/usr/bin/python

import cv2
import glob
import os

cascPath = "./haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascPath)                

cap = cv2.VideoCapture(0)

try:
    os.mkdir("./all_extracted/")
except:
    print "Could not create dir"

cnt = 0
while True:
    ret,img = cap.read()
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
        cv2.imwrite("./all_extracted/extracted_%d.jpg" % (cnt), patch)
        cv2.imshow("patch", patch)
        cv2.waitKey(5)
    cnt += 1
