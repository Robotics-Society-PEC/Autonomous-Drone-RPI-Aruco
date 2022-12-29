import cv2
from cv2 import aruco
import cv2.aruco as aruco
import numpy as np
import os


def findArucoMarker(img,markerSize= 6, totalMarkers=250,
      draw=True):
    imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict= aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected= aruco.detectMarkers(imgGray,
             arucoDict, parameters=arucoParam)
    print(ids)         

    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs,ids]




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




