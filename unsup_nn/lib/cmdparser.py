"""
Command line argument options parser.
Adopted and modified from https://github.com/pytorch/examples/blob/master/imagenet/main.py

Usage with two minuses "- -". Options are written with a minus "-" in command line, but
appear with an underscore "_" in the attributes' list.

Attributes:
    data (str): Path to dataset directory
    workers (int): Number of data loading workers (default: 4)
    patch_size (int): Length of shorter side for face patches (default: 64)
    architecture (str): Model architecture (default: cnn_maxpool_bn)
    weight_init (str): Weight-initialization scheme (default: kaiming-normal)
    optimizer (str): Choice of optimizer (default: Adam)
    epochs (int): Number of epochs to train (default: 30)
    batch_size (int): Mini-batch size (default: 128)
    learning_rate (float): Initial learning rate (default: 0.1)
    momentum (float): Momentum value (default: 0.9)
    weight_decay (float): L2-norm/weight-decay value (default: 0.0005)
    batch_norm (float): Batch normalization value (default: 0.001)
    print_freq (int): Print frequency in amount of batches (default: 100)
"""

import argparse

parser = argparse.ArgumentParser(description='PyTorch SmartestMirror Unsupervised Training')

# Dataset and loading
parser.add_argument('-data', '--data-dir', metavar='DATADIR',
                    help='path to dataset')
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('-p', '--patch-size', default=32, type=int,
                    metavar='P', help='length of shorter side for patches')


# Architecture and weight-init
parser.add_argument('-a', '--architecture',
                    metavar='ARCH', default='CAE',
                    choices=["CAE", "VCAE"],
                    help='model architecture')
parser.add_argument('--weight-init', default='kaiming-normal', metavar='W',
                    help='weight-initialization scheme (default: kaiming-normal)')

# Training hyper-parameters
parser.add_argument('-optim', '--optimizer', default='ADAM',
                    help='Optimizer choice: ADAM / SGD')
parser.add_argument('--epochs', default=20, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('-b', '--batch-size', default=64, type=int,
                    metavar='N', help='mini-batch size (default: 128)')
parser.add_argument('-lr', '--learning-rate', default=1e-3, type=float,
                    metavar='LR', help='initial learning rate (default: 0.001)')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum (default 0.9)')
parser.add_argument('-wd', '--weight-decay', default=0, type=float,
                    metavar='W', help='weight decay (default: 5e-4)')
parser.add_argument('-bn', '--batch-norm', default=1e-3, type=float,
                    metavar='BN', help='batch normalization (default 1e-3)')
parser.add_argument('-pf', '--print-freq', default=100, type=int,
                    metavar='N', help='print frequency (default: 100)')

# Variational unsupervised learning
parser.add_argument('-var', '--variational', default=False, type=bool,
                    help='')
