import cv2
import numpy as np

# Capture video from the Raspberry Pi camera
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame from the camera
    ret, frame = cap.read()

    # Convert the image from the BGR color space to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of colors to detect (in this case, red)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the image to get only the red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find the coordinates of all non-zero pixels in the mask
    coords = np.column_stack(np.where(mask > 0))

    # Print the coordinates of the red pixels
    print(coords)

    # Bitwise-AND the mask and the original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the images
    cv2.imshow("Original", frame)
    cv2.imshow("Red", res)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()