import numpy as np
import cv2
import glob

chessboardSize= (24,17)
frameSize=(1440,1080)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER ,30, 0.001)

#prepare object points, like (0,0,0), (1,0,0) ,(2,0,0)  .....(6,5,0)
objp= np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] =np.mgrid[0:chessboardSize, 0:chessboardSize[1]].T.reshape(-1,2)

#Arrays to store object points and image points from all the images
objPoints=[]
imgPoints=[]

image = glob.glob('*.png')

for image in images:
     print(image)
     img= cv2.imread(image)
     gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     # find the chess board corners
     ret, corners= cv2.findChessboardCorners(gray, chessboardSize , None)

     if ret == True:

        objPoints.append(objp)
        corners2 =cv2.cornerSubPix(gray, corners, (11,11),(-1,-1) , criteria)
        imgPoints.append(corners)

        #draw and display the corners
        cv2.drawChessboardCorners(img, chessboardSize , corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows() 

#print("object points: ", objPoints)
#print("image points: ", imgPoints)


############Calibration###################

ret, cameraMatrix , dist , rvecs , tvecs =cv2.calibrateCamera(objPoints , imgPoints , frameSize , None , None)

print("Camera Calibrated: ", ret)
print("\nCamera Matrix:\n" , cameraMatrix)
print("\nDistortion Parameters:\n" , dist)
print("\nRotation Vectors:\n"  , rvecs)
print("\nTranslation Vectors:\n" , tvecs)

##########Undistortion##########

