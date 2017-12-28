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

def pred():
    model = Net()
    model.load_state_dict(torch.load('FACENET.pth'))
    model.eval()
    # get random image patch
    img = cv2.imread("./extracted_300.jpg")
    img = cv2.resize(img, (32,32))
    patch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)/255.

    patch_data = torch.from_numpy(np.array([[patch]]).astype(np.float32))
    data = Variable(patch_data, volatile=True)
    output = model(data)
    #pred = output.data.max(1, keepdim=True)[1]
    pred = np.argmax(output.cpu().data.numpy())
    print(mylabels[pred])
    cv2.imshow("face",patch)
    cv2.waitKey(10)

pred()
