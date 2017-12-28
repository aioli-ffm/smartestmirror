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

# Training settings
parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                    help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=25, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

# OWN DATALOADER
import glob
import sys
import cv2
import numpy as np

basefolder = '/home/shared/data/faces/lfw/all_extracted/'
# get all filenames for labels
all_fnames = {}
X_train = []
y_train = []

for l in mylabels:
    all_fnames[l] = glob.glob(basefolder + "/%s/*.jpg" % (l))
    print("Found %d files for label %s" % (len(all_fnames[l]), l))
# now load the patches and labels into arrays
for key in all_fnames.keys():
    for j,f in enumerate(all_fnames[key]):
        try:
            img = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)/255.
            img = cv2.resize(img, (32,32))
            X_train.append(np.array([img.astype(np.float32)]))
            y_train.append(mylabels.index(key))
        except Exception as e:
            print("Exception: ", e)

X_train = np.array(X_train)
y_train = np.array(y_train)

#set aside a random set for testing
indices = np.random.randint(0,len(X_train),int(len(X_train)*0.1))
X_test = X_train[indices]
y_test = y_train[indices]
np.delete(X_train, indices)
np.delete(y_train, indices)

print("X_train.shape: ")
print(X_train.shape)
print("y_train.shape: ")
print(y_train.shape)

print("X_test.shape: ")
print(X_test.shape)
print("y_test.shape: ")
print(y_test.shape)

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}
#-- train loader
train_data = torch.from_numpy(X_train)
our_labels = torch.from_numpy(y_train)
train = torch.utils.data.TensorDataset(train_data, our_labels)
train_loader = torch.utils.data.DataLoader(train, batch_size=args.batch_size, shuffle=True, **kwargs)

#-- test loader
test_data = torch.from_numpy(X_test)
our_test_labels = torch.from_numpy(y_test)
test = torch.utils.data.TensorDataset(test_data, our_test_labels)
test_loader = torch.utils.data.DataLoader(test, batch_size=args.batch_size, shuffle=True, **kwargs)
# OWN DATALOADER END

model = Net()
if args.cuda:
    model.cuda()

optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        #print(data.shape)
        #print(target.shape)
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data[0]))

def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data, volatile=True), Variable(target)
        output = model(data)
        test_loss += F.nll_loss(output, target, size_average=False).data[0] # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1] # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


for epoch in range(1, args.epochs):
    train(epoch)
    torch.save(model.state_dict(), './FACENET.pth') 
    test()
