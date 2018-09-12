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
filename = "/tmp/combined.jpg"
img = cv2.imread(filename)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cd_clss = circle_detector.CircleTracker()
# run circle marker detector
ellipses_list = circle_detector.find_pupil_circle_marker(gray_img, 1.0)
