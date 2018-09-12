"""Detect pupil using PyPupil

Use the pupil labs software to detect a pupil

Author
------
Shankar Kulumani		GWU		skulumani@gwu.edu
"""

import cv2
import numpy as np

import circle_detector

# read the image and convert to grayscale
filename = "/tmp/cut.jpg"
img = cv2.imread(filename)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cd_clss = circle_detector.CircleTracker()
# run circle marker detector
ellipses_list = circle_detector.find_pupil_circle_marker(gray_img, 1.0)

gray_img_size = gray_img.shape[::-1]
# Resize the image
gray_img_resize = cv2.resize(gray_img, dsize=(0, 0), fx=1.0, fy=1.0)

# Use three kinds of adaptive threshold to extract the edges of the image
# The first one is for complicated scene
# The Second one is for normal scene
# The last one is for marker in low contrast
img_resize_blur = cv2.GaussianBlur(gray_img_resize, (3, 3), 0.25)
edges = [cv2.adaptiveThreshold(img_resize_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 36),
         cv2.adaptiveThreshold(img_resize_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 18),
         cv2.adaptiveThreshold(img_resize_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 29, 3)]


