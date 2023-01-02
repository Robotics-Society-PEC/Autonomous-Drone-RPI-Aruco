import numpy as np
import cv2
import glob

cb_width = 9
cb_height = 6
cb_square_size= 26.3

#termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 30,0.001)

#pepare object points, like{0,0,0},{1,0,0},{2,0,0}....{6,5,0}

cb_3D_points = np.zeroes((cb_width * cb_height, , np.float32))
cb_3D_points[:,:2] = np.mgrid[0:cb_width, 0:cb_height] .T.reshape(-1,2)* cb_square_size

#arrays to store object points and image points from all the images
list_cb_3d_points = [] #3d point in real world space
list_cb_2d_points =[] #2d points in image plane

list_images= glob.glob('*.jpg')

for frame_name in list_images:
    img = cv2.imraed(frame_name)

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #find the aruco board corners

     