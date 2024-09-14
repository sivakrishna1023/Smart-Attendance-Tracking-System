import cv2
import sys
from time import sleep
import os
import shutil

# Find the path to the haarcascade file relative to the script's location
cascPath = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cascPath)

# Initialize the webcam and other components
key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)
cnt = 0

# Create a new directory to save images
new = 'class_room_images'
if not os.path.exists(new):
    os.mkdir(new)

# Capture and save 10 images
while True:
    check, frame = webcam.read()
    print(check)  # Prints True as long as the webcam is running
    
    if cnt < 10:
        filename = f'{cnt}_img.jpg'
        cv2.imwrite(os.path.join(new, filename), img=frame)
        cnt += 1
    else:
        webcam.release()
        cv2.destroyAllWindows()
        break

# Release the webcam and destroy all windows
webcam.release()
cv2.destroyAllWindows()
