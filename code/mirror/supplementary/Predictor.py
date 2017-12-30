#!/usr/bin/python
'''
author: Tobias Weis
'''
from .Net import *
import os.path
import cv2
import numpy as np
import time


class Predictor:
    def __init__(self):
        self.model = Net()
        if not os.path.isfile("./supplementary/FACENET.pth"):
            print("===========================")
            print(" could not find trained FACENET.pth")
            print("===========================")
        self.model.load_state_dict(torch.load('./supplementary/FACENET.pth'))
        self.model.eval()

        if not os.path.isfile("./supplementary/haarcascade_frontalface_default.xml"):
            print("===========================")
            print(" could not find haarcascade_frontalface_default.xml")
            print("===========================")

        cascPath = "./supplementary/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)

        try:
            os.mkdir("/tmp/patches/")
        except:
            pass

    def extractFace(self, save=False):
        self.patches = []
        self.coordinates = []

        try:
            faces = self.faceCascade.detectMultiScale(
                self.gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50),
                # this is opencv 2
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
        except:
            faces = self.faceCascade.detectMultiScale(
                self.gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(50, 50),
                # this is opencv 3
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        for (x, y, w, h) in faces:
            patch = self.gray[y:y + h, x:x + w]

            if save:
                cv2.imwrite("/tmp/patches/%d_%d_%d_%d_%d.jpg" %
                            (time.time(), x, y, w, h), patch)

            patch = patch / 255.
            patch = cv2.resize(patch, (32, 32))

            self.patches.append(np.array(patch.astype(np.float32)))
            self.coordinates.append([x, x + w, y, y + h])

    def setImage(self, img):
        self.img = img
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def pred(self):
        predictions = []
        if len(self.patches) > 0:
            # get random image patch
            np_patches = np.array([self.patches])
            np_patches = np_patches.transpose(1, 0, 2, 3)
            #patch_data = torch.from_numpy(np.array([self.patches]))
            patch_data = torch.from_numpy(np_patches)
            data = Variable(patch_data, volatile=True)
            outputs = self.model(data)
            for idx, output in enumerate(outputs):
                pred = np.argmax(output.cpu().data.numpy())
                x = self.coordinates[idx][0]
                y = self.coordinates[idx][2]
                x2 = self.coordinates[idx][1]
                y2 = self.coordinates[idx][3]
                cv2.rectangle(self.img, (x, y), (x2, y2), (255, 0, 255), 2)
                predictions.append(mylabels[pred])
        return predictions
