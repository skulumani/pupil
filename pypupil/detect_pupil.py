"""Detect pupil using PyPupil

Use the pupil labs software to detect a pupil

Author
------
Shankar Kulumani		GWU		skulumani@gwu.edu
"""

from pupil import circle_detector
from pupil.detectors import detector_2d
from pupil.detectors import detector_3d
from pupil import methods_python
from pupil.video_capture.file_backend import Frame

import cv2
import numpy as np
import av

import pdb

def threshold_example():
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

    edge = edges[1]
    found_pos = []
    found_size = []
    circle_clusters = circle_detector.find_concentric_circles(edge, None, None, found_pos, found_size, first_check=True, min_ellipses_num=2)

def detector2d_example(filename="../../distortion/data/visor/Calibration - Short-Long Blink for Start and Stop.h264"):
    """Try to test out the detector 2d code
    
    Filename should be mp4 video
    """
    container = av.open(filename)
    
    detector_cpp = detector_2d.Detector_2D()
    
    # ouput video to save for visualization
    fourcc = cv2.VideoWriter_fourcc('X', '2', '6', '4')
    output_video = cv2.VideoWriter('/tmp/detector2d_output.mp4', fourcc, 25, (640, 480))

    pupil_center = []
    pupil_axes = []
    pupil_angle = []

    pupil_confidence  = [] 
    pupil_diameter = [] 
    pupil_norm_pos = []

    # get frames from the video
    for f in container.decode(video=0):
        # frame.to_image().save('/tmp/frame_{}.jpg'.format(frame.index))

        # create frame object
        frame = Frame(f.index, f, f.index)
        # create  Roi object
        u_r = methods_python.Roi(frame.img.shape)

        # try to detect
        results_cpp = detector_cpp.detect(frame, u_r, visualize=True)
         
        # extract out the ellipse center, axes, and angle
        pupil_center.append([results_cpp['ellipse']['center'][0], results_cpp['ellipse']['center'][1]])
        pupil_axes.append([results_cpp['ellipse']['axes'][0], results_cpp['ellipse']['axes'][1]])
        pupil_angle.append(results_cpp['ellipse']['angle'])

        pupil_confidence.append(results_cpp['confidence'])
        pupil_diameter.append(results_cpp['diameter'])
        pupil_norm_pos.append([results_cpp['norm_pos'][0], results_cpp['norm_pos'][1]])

        output_video.write(frame.img)

        # visualize
        cv2.imshow('frame', frame.img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    pupil_center = np.array(pupil_center)
    pupil_axes = np.array(pupil_axes)
    pupil_angle = np.array(pupil_angle)

    pupil_confidence = np.array(pupil_confidence)
    pupil_diamter = np.array(pupil_diameter)
    pupil_norm_pos = np.array(pupil_norm_pos)

    return pupil_confidence
    # try to plot the center onto the image

def detector3d_example(filename="../../distortion/data/visor/Calibration - Short-Long Blink for Start and Stop.h264"):
    """Try out the detector 3d
    """

    container = av.open(filename)
    
    detector_cpp_3 = detector_3d.Detector_3D()
    detector_cpp = detector_2d.Detector_2D()

    # ouput video to save for visualization
    fourcc = cv2.VideoWriter_fourcc('X', '2', '6', '4')
    output_video = cv2.VideoWriter('/tmp/detector3d_output.mp4', fourcc, 25, (640, 480))

    pupil_center = []
    pupil_axes = []
    pupil_angle = []

    pupil_confidence  = [] 
    pupil_diameter = [] 
    pupil_norm_pos = []

    # get frames from the video
    for f in container.decode(video=0):
        # frame.to_image().save('/tmp/frame_{}.jpg'.format(frame.index))

        # create frame object
        frame = Frame(f.index, f, f.index)
        # create  Roi object
        u_r = methods_python.Roi(frame.img.shape)

        # try to detect
        results_2d = detector_cpp.detect(frame, u_r, visualize=True)
        # results_3d = detector_cpp.detect(frame, u_r, visualize=True)
         
        # # extract out the ellipse center, axes, and angle
        # pupil_center.append([results_cpp['ellipse']['center'][0], results_cpp['ellipse']['center'][1]])
        # pupil_axes.append([results_cpp['ellipse']['axes'][0], results_cpp['ellipse']['axes'][1]])
        # pupil_angle.append(results_cpp['ellipse']['angle'])

        # pupil_confidence.append(results_cpp['confidence'])
        # pupil_diameter.append(results_cpp['diameter'])
        # pupil_norm_pos.append([results_cpp['norm_pos'][0], results_cpp['norm_pos'][1]])

        output_video.write(frame.img)

        # visualize
        cv2.imshow('frame', frame.img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        # print(results_cpp['confidence'])
    
    return 0
    # pupil_center = np.array(pupil_center)
    # pupil_axes = np.array(pupil_axes)
    # pupil_angle = np.array(pupil_angle)

    # pupil_confidence = np.array(pupil_confidence)
    # pupil_diamter = np.array(pupil_diameter)
    # pupil_norm_pos = np.array(pupil_norm_pos)

    # return pupil_center 
    # try to plot the center onto the image

if __name__ == "__main__":
    # detector2d_example()
    detector3d_example()
