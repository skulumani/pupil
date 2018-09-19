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

import itertools
from IPython.core.debugger import Pdb
ipdb = Pdb()

def nothing(x):
    pass

def load_distortion_map(filename):
    """Load the distortion map from the file and return as map_x, map_y
    """
    fs = cv2.FileStorage(filename, cv2.FileStorage_READ)
    map_x = fs.getNode('map_x').mat()
    map_y = fs.getNode('map_y').mat()
    fs.release()
    return (map_x, map_y)

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

def define_detector_settings():
    """This creates a dictionary to input into Detector_2D that defines some 
    of the settings used for the pupil detection. 

    This dictionary might also be the same that is given to Detector_3D
    """
    settings = {}
    settings['coarse_detection'] = True
    settings['coarse_filter_min'] = 128
    settings['coarse_filter_max'] = 280
    settings['intensity_range'] = 23
    settings['blur_size'] = 5
    settings['canny_treshold'] = 160
    settings['canny_ration'] = 2
    settings['canny_aperture'] = 5
    settings['pupil_size_max'] = 150
    settings['pupil_size_min'] = 10
    settings['strong_perimeter_ratio_range_min'] = 0.6
    settings['strong_perimeter_ratio_range_max'] = 1.1
    settings['strong_area_ratio_range_min'] = 0.8
    settings['strong_area_ratio_range_max'] = 1.1
    settings['contour_size_min'] = 5
    settings['ellipse_roundness_ratio'] = 0.09
    settings['initial_ellipse_fit_treshhold'] = 4.3
    settings['final_perimeter_ratio_range_min'] = 0.5
    settings['final_perimeter_ratio_range_max'] = 1.0
    settings['ellipse_true_support_min_dist'] = 3.0
    settings['support_pixel_ratio_exponent'] = 2.0

    return settings

def detector2d_example(video_filename="../../distortion/data/visor/Calibration - Short-Long Blink for Start and Stop.h264",
                       combined_map_filename='../../distortion/data/combined_map_interpolation.xml'):
    """Try to test out the detector 2d code
    
    Filename should be mp4 video
    """

    cv2.namedWindow("Frames")
    # create some trackbars for the settings
    cv2.createTrackbar('Pupil Size Min', 'Frames', 10, 100, nothing)
    cv2.createTrackbar('Pupil Size Max', 'Frames', 150, 250, nothing)
    cv2.createTrackbar('Intesity Range', 'Frames', 23, 70, nothing)
    cv2.createTrackbar('ROI Lower X', 'Frames', 100, 400, nothing)
    cv2.createTrackbar('ROI Upper X', 'Frames', 640, 640, nothing)
    cv2.createTrackbar('ROI Lower Y', 'Frames', 100, 400, nothing)
    cv2.createTrackbar('ROI Upper Y', 'Frames', 480, 480, nothing)

    container = av.open(video_filename)
   
    # get the distortion map
    map_x, map_y = load_distortion_map(combined_map_filename)

    # create  Roi object
    u_r = methods_python.Roi((480, 640))
    # set region of interest
    roi_lower_x = 100
    roi_upper_x = 640
    roi_lower_y = 100
    roi_upper_y = 480
    u_r.set((roi_lower_x, roi_lower_y, roi_upper_x, roi_upper_y))

    settings = define_detector_settings()
    detector_cpp = detector_2d.Detector_2D(settings=settings)
    
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
    for f in itertools.cycle(container.decode(video=0)):
        # frame.to_image().save('/tmp/frame_{}.jpg'.format(frame.index))

        # create frame object
        frame = Frame(f.index, f, f.index)
        # remap the image using the distortion map
        frame.remap(map_x, map_y)

        # update settings
        settings['pupil_size_min'] = cv2.getTrackbarPos('Pupil Size Min', 'Frames')
        settings['pupil_size_max'] = cv2.getTrackbarPos('Pupil Size Max', 'Frames')
        settings['intesity_range'] = cv2.getTrackbarPos('Intensity Range', 'Frames')
        detector_cpp.update_settings(settings)
        
        # update the region of interest
        roi_lower_x = cv2.getTrackbarPos('ROI Lower X', 'Frames')
        roi_upper_x = cv2.getTrackbarPos('ROI Upper X', 'Frames')
        roi_lower_y = cv2.getTrackbarPos('ROI Lower Y', 'Frames')
        roi_upper_y = cv2.getTrackbarPos('ROI Upper Y', 'Frames')
        u_r.set((roi_lower_x, roi_lower_y, roi_upper_x, roi_upper_y))

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
        
        # augment the image with a frame number somewhere
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame.img,'{}'.format(frame.timestamp),(frame.width//2, frame.height - 2), font, 1,(0, 0, 255),2,cv2.LINE_AA)
        
        # draw the region of interest rectangle
        cv2.rectangle(frame.img, (roi_lower_x, roi_lower_y), (roi_upper_x, roi_upper_y), (0,0, 255))

        # visualize
        cv2.imshow("Frames", frame.img)
        k = cv2.waitKey(0) & 0xFF
        if k == ord('q') or k == ord('Q') or k == 27:
            cv2.destroyAllWindows()
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
    
    detector3d = detector_3d.Detector_3D()
    detector2d = detector_2d.Detector_2D()

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
        # results_2d = detector2d.detect(frame, u_r, visualize=False)
        results_3d = detector3d.detect(frame, u_r, visualize=False)
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
    video_filename = '/tmp/Calibration - Short-Long Blink for Start and Stop.h264'
    combined_map_filename = '/tmp/combined_map_interpolation.xml'

    detector2d_example(video_filename=video_filename,
                       combined_map_filename=combined_map_filename)
    # detector3d_example()
