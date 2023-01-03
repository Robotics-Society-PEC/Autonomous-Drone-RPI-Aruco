import cv2

cap = cv2.VideoCapture(0)
i = 0
while True:
    sucess , img = cap.read()

    cv2.imshow("frame" , img)
    if cv2.waitKey(1) == ord('c'):
        cv2.imwrite(f'images/image{i}.jpg' , img)
        i+=1
    if cv2.waitKey(1) == ord('s'):
        break

cap.release()

