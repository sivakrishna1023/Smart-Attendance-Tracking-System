# import cv2
# import sys
# from time import sleep
# import os
# import shutil

# # Find the path to the haarcascade file relative to the script's location
# cascPath = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
# faceCascade = cv2.CascadeClassifier(cascPath)

# # Initialize the webcam and other components
# key = cv2.waitKey(1)
# webcam = cv2.VideoCapture(0)
# sleep(2)
# cnt = 0

# # Create a new directory to save images

# new = 'class_room_images'
# if not os.path.exists(new):
#     os.mkdir(new)

# # Capture and save 10 images
# while True:
#     check, frame = webcam.read()
#     print(check)  # Prints True as long as the webcam is running
    
#     if cnt < 10:
#         filename = f'{cnt}_img.jpg'
#         cv2.imwrite(os.path.join(new, filename), img=frame)
#         cnt += 1
#     else:
#         webcam.release()
#         cv2.destroyAllWindows()
#         break

# # Release the webcam and destroy all windows
# webcam.release()
# cv2.destroyAllWindows()


import cv2
import os
import time
import argparse

class ClassroomImageCapture:
    def __init__(self, selected_time_minutes, num_images=10, save_dir='class_room_images'):
        """
        Initialize the parameters for the image capture process.

        :param selected_time_minutes: Total time in minutes for capturing images.
        :param num_images: Number of images to capture (default is 10).
        :param save_dir: Directory where the images will be saved (default is 'class_room_images').
        """
        self.selected_time_minutes = selected_time_minutes
        print(f"Before operation: {self.selected_time_minutes}")
        self.selected_time_minutes = max(self.selected_time_minutes - 16, 0)
        print(f"After operation: {self.selected_time_minutes}")

        self.num_images = num_images
        self.save_dir = save_dir
        
        # Calculate sleep time based on available time and number of images
        if self.selected_time_minutes > 0 and self.num_images > 0:
            self.sleep_time = (self.selected_time_minutes * 60) / self.num_images  # seconds
        else:
            self.sleep_time = 0  # No sleep time if no effective capture time or images
        
        print(f"Calculated sleep time: {self.sleep_time} seconds")

        # Setup the cascade classifier for face detection
        cascPath = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        
        # Initialize webcam
        self.webcam = cv2.VideoCapture(0)
        
        # Ensure the save directory exists
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
    
    def capture_images(self):
        """
        Capture images and save them to the specified directory.
        """
        cnt = 0
        
        while cnt < self.num_images:
            check, frame = self.webcam.read()

            if check:
                # Save the image
                filename = f'{cnt}_img.jpg'
                cv2.imwrite(os.path.join(self.save_dir, filename), img=frame)
                print(f"Image {cnt + 1} saved.")
                
                # Increment the counter
                cnt += 1

                # Sleep for the calculated sleep time
                time.sleep(self.sleep_time)
            else:
                print("Error capturing image from webcam.")
                break  # Exit loop on failure
        
        # Release resources
        self.cleanup()

    def cleanup(self):
        """
        Release the webcam and close any OpenCV windows.
        """
        self.webcam.release()
        cv2.destroyAllWindows()


# Main function to parse arguments and run the capture
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture classroom images over a period of time.')
    parser.add_argument('selected_time_minutes', type=int, help='Total time in minutes for capturing images')
    parser.add_argument('--num_images', type=int, default=10, help='Number of images to capture (default: 10)')
    
    args = parser.parse_args()

    # Initialize the ClassroomImageCapture class with the provided arguments
    image_capture = ClassroomImageCapture(selected_time_minutes=args.selected_time_minutes, num_images=args.num_images)
    
    # Start capturing images
    image_capture.capture_images()
