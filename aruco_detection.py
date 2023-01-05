import cv2
from cv2 import aruco
import cv2.aruco as aruco
from scipy.spatial import distance as dist
import imutils
from imutils import contours
from imutils imporbt perspective
import numpy as np
import os


def findArucoMarker(img,markerSize= 6, totalMarkers=250,
      draw=True):
    imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    #load the dictionary that was used to generate the markers
    arucoDict= aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    
            
    imgGray = imutils.resize(imgGray, width=500)
    imgGray=cv2.GaussianBlur(imgGray,(7,7),0)



    #perform edge detection, then perform 
    #dilation + erosion to close gaps in between edges

    imgGray=cv2.dilate(imgGray, None, iterations=1)
    imgGray = cv2.erode(imgGray , None, iterations=1)

    #find contours in edge map
    cnts = cv2.findContours(imgGray.copy(),
                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)

    #sort the contours from left-to-right and initialize 
    (cnts,_)= contours.sort_contours(cnts)
    #for pixel to inch calibration


    pixelsPerMetric=None
    arucofound= findArucoMarker(img , totalMarkers=100)
    if len(arucofound[0])!=0:
        aruco_perimeter = cv2.arcLength(arucofound[0][0][0], True)

        #Pixel to inch ratio
        #perimeter of the aruco marker is 8 inches

        pixelsPerMetric = aruco_perimeter /8
        print(" pixel to inch", pixelsPerMetric)

    else:
        pixelsPerMetric  = 38.0
        

    for c in cnts:

        #if the contour is not sufficiently large, 
        #ignore it
        if cv2.contourArea(c)<2000:
            continue

#bounding rectangle is drawn within the minimum area , 
#so it considers the rotation also
  # the function used is cv.minAreaRect(). it returns
  #a box2D structure which contains following details:
     

    # Detect aruco marker and use
    # it's dimension to calculate the pixel to inch ratio
    (tl, tr, br, bl) = box
    width_1 = (dist.euclidean(tr, tl))
    height_1 = (dist.euclidean(bl, tl))
    d_wd= width_1/pixelsPerMetric
    d_ht= height_1/pixelsPerMetric        


    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
        bboxs, ids, rejected= aruco.detectMarkers(imgGray,
             arucoDict, parameters=arucoParam)
        print(ids)
    return[ bboxs, ids, rejected]

    

def main():
    cap= cv2.VideoCapture(0)

    while True:
        success,img=cap.read()
        findArucoMarker(img)
        cv2.imshow("Image",img)
        if cv2.waitKey(1) == ord('s'):
            break

if __name__ == "__main__":
    main()
