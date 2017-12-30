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
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        #print("x:",x)
        x = x.view(-1, 20*24*24)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x)

