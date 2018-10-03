from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

mylabels = [
        "tobi",
        "mari",
        "martin",
        "raj",
        "timm",
        "christian",
        "other"
        ]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.fc1 = nn.Linear(20*24*24, 50)
        self.fc2 = nn.Linear(50, len(mylabels))

    def forward(self, x):
        out1 = F.relu(self.conv1(x))
        out2 = F.relu(self.conv2(out1))
        #print("x:",x)
        out3 = out2.view(-1, 20*24*24)
        out4 = F.relu(self.fc1(out3))
        out5 = self.fc2(out4)
        return F.log_softmax(out5), out1,out2,out3,out4,out5

