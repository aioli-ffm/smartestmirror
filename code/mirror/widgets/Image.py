#!/usr/bin/python
'''
author: Tobias Weis
'''

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import os
import glob
import logging
import random
import numpy as np
from widgets.Base import *

class Image(QLabel,Base):
    """
    Display time and date
    """
    def __init__(self, title, parent, serviceRunner):
        super(Image,self).__init__(title,parent)
        self.parent = parent
        self.logger = logging.getLogger(__name__)

    def choose_image(self):
        extensions = ['*.png', '*.jpg']
        image_dir = os.path.join(self.res_path, "slideshow_images")
        # parse directory of images and select one randomly
        img_list = []
        for ext in extensions:
            for fname in glob.glob(image_dir + "/" + ext):
                img_list.append(fname)
        self.logger.debug("Found %d image files in directory %s" % (len(img_list), image_dir))
        chosen_fname = random.choice(img_list)
        self.logger.debug("Chose " + chosen_fname)
        return cv2.cvtColor(self.image_resize(cv2.imread(chosen_fname)), cv2.COLOR_BGR2RGB)

    def setimg(self,img):
        img = np.require(img, np.uint8, 'C')
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap)

    def image_resize(self, image, inter = cv2.INTER_AREA):
	dim = None
	(h, w) = image.shape[:2]

	if h > w:
            height = int(self.config['height'])
            width = None
        else:
            width = int(self.config['width'])
            height = None

	if width is None:
	    r = height / float(h)
	    dim = (int(w * r), height)
	else:
	    r = width / float(w)
	    dim = (width, int(h * r))

	resized = cv2.resize(image, dim, interpolation = inter)
        # now put the image in the lower-left
        w = int(self.config['width'])
        h = int(self.config['height'])
        final_img = np.zeros((h, w,3), np.uint8)
        final_img[h-resized.shape[0]:, w-resized.shape[1]:,:] = resized
	return final_img

    def update(self):
        self.setimg(self.choose_image())
