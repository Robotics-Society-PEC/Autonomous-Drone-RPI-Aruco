import numpy as np
import cv2,time
import cv2.aruco as aruco
import math


cv2.namedWindow("Image Feed")
cv2.moveWindow("Image Feed",  150 , -25)

cap=cv2.VideoCapture(0)

prev_frame_time = time.time()

cal_image_count=0
frame_count=0


#setup camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS , 40)



while True:

    ret, frame = cap.read() #-- read the camera frame

    #processing code goes here
    frame_count +=1

    if frame_count == 30:
        cv2.imwrite("cal_image_"+ str(cal_image_count) + ".jpg" , frame)
        cal_image_count +=1
        frame_count=0

    #calculate the fps and display on frame

    new_frame_time= time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame , "FPS"+ str(int(fps)),(10,40), cv2.FONT_HERSHEY_PLAIN ,
                3, (100,255,0) , 2, cv2.LINE_AA)
    
    cv2.imshow ("Image Feed" , frame)
    print(frame)

    # ----- use "q" to quit

    key= cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()    