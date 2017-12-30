#!/usr/bin/python
'''
author: Tobias Weis
'''

from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from Net import *
import cv2
import numpy as np
import glob

class Predictor:
    def __init__(self):
        self.model = Net()
        self.model.load_state_dict(torch.load('FACENET.pth'))
        self.model.eval()

        cascPath = "./haarcascade_frontalface_alt.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)

    def extractFace(self):
	self.patches = []
	self.coordinates = []

       	faces = self.faceCascade.detectMultiScale(
	    self.gray,
	    scaleFactor=1.1,
	    minNeighbors=5,
	    minSize=(50, 50),
	    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)

        print("Found %d faces" % (len(faces)))

	for (x, y, w, h) in faces:
	    patch = self.gray[y:y+h, x:x+w]/255.
            patch = cv2.resize(patch, (32,32))
	
	    self.patches.append(np.array(patch.astype(np.float32)))
	    self.coordinates.append([x,x+w,y,y+h])

    def setImage(self,imagefilename):
        self.img = cv2.imread(imagefilename)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def pred(self):
        if len(self.patches) > 0:
            # get random image patch
            patch_data = torch.from_numpy(np.array([self.patches]))
            data = Variable(patch_data, volatile=True)
            outputs = self.model(data)
            for idx,output in enumerate(outputs):
                pred = np.argmax(output.cpu().data.numpy())
                x = self.coordinates[idx][0]
                y = self.coordinates[idx][2]
                x2 = self.coordinates[idx][1]
                y2 = self.coordinates[idx][3]
                cv2.rectangle(self.img, (x,y),(x2,y2), (255,0,255),2)
                print(mylabels[pred])
        cv2.imshow("face",self.img)
        cv2.waitKey(0)

#files = glob.glob("/home/shared/data/faces/sequences/Tobi/*.png")
files = glob.glob("/home/shared/data/faces/sequences/Timm/*.png")
Pred = Predictor()
for f in files:
    Pred.setImage(f)
    Pred.extractFace()
    Pred.pred()
