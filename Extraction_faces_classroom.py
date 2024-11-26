# import sys
# import tensorflow as tf
# from tensorflow import keras
# import os
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# from PIL import Image
# from numpy import asarray
# import mtcnn
# from mtcnn.mtcnn import MTCNN

# # Setting up environment variables for TensorFlow
# os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# # Handling encoding issues on Windows
# if os.name == 'nt':  # Apply only on Windows
#     import ctypes
#     ctypes.windll.kernel32.SetConsoleCP(65001)
#     ctypes.windll.kernel32.SetConsoleOutputCP(65001)
# sys.stdout.reconfigure(encoding='utf-8')
# sys.stderr.reconfigure(encoding='utf-8')

# # Getting the current working directory
# current_directory = os.getcwd()

# # Define the input and output folder paths dynamically
# input_folder = os.path.join(current_directory, 'class_room_images')
# output_folder = os.path.join(current_directory, 'pre_process_images')

# # Create output directory if it doesn't exist
# if not os.path.exists(output_folder):
#     os.mkdir(output_folder)

# # Function to extract faces from an image
# def extract_face(img, required_size=(224, 224)):
#     # Create the detector, using default weights
#     detector = MTCNN()
#     # Detect faces in the image
#     results = detector.detect_faces(img)
#     face_array = []
#     for i in range(len(results)):
#         x1, y1, width, height = results[i]['box']
#         x2, y2 = x1 + width, y1 + height
#         face = img[y1:y2, x1:x2]
#         # Resize pixels to the model size
#         image = Image.fromarray(face)
#         image = image.resize(required_size)
#         face_array.append(asarray(image))
#     return face_array

# # Processing each image in the input folder
# cnt = 0
# for filename in os.listdir(input_folder):
#     try:
#         # Safely print filenames
#         print(f"Processing file: {filename.encode('utf-8', errors='ignore').decode('utf-8')}")
#         img1 = cv2.imread(os.path.join(input_folder, filename))
        
#         # Skip if the image could not be read
#         if img1 is None:
#             print(f"Failed to read image {filename}. Skipping.")
#             continue

#         # Resize the image
#         img1 = cv2.resize(img1, (224, 224))
#         # Extract faces from the image
#         pixels = extract_face(img1)
#         print(f"Number of faces detected: {len(pixels)}")

#         # Save extracted faces to the output folder
#         for j in range(len(pixels)):
#             output_path = os.path.join(output_folder, filename[:2] + 'f_' + str(cnt) + '.jpg')
#             cv2.imwrite(output_path, pixels[j])
#             cnt += 1

#         print(f"Finished processing {filename}")

#     except UnicodeEncodeError as e:
#         print(f"UnicodeEncodeError processing file {repr(filename)}: {str(e)}")
#     except Exception as e:
#         print(f"Unexpected error processing file {repr(filename)}: {str(e)}")

# print("All images processed successfully.")





import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from numpy import asarray
import mtcnn
from mtcnn.mtcnn import MTCNN
import customtkinter as ctk
import tkinter as tk
import argparse
import cv2
import os
import time

class ClassroomImageProcessor:
    def __init__(self, input_folder='class_room_images', output_folder='pre_process_images'):
        """
        Initialize the processor with input and output folders.

        :param input_folder: Directory containing the classroom images.
        :param output_folder: Directory where pre-processed images will be saved.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

        # Initialize variables to track the image with the maximum number of faces
        self.max_faces = 0
        self.image_with_max_faces = None
        self.detected_faces = None
        self.bounding_boxes = None

    def extract_face(self, img, required_size=(224, 224)):
        """Extract faces from an image using MTCNN."""
        detector = MTCNN()
        results = detector.detect_faces(img)
        face_array = []
        for i in range(len(results)):
            x1, y1, width, height = results[i]['box']
            x2, y2 = x1 + width, y1 + height
            face = img[y1:y2, x1:x2]
            image = Image.fromarray(face)
            image = image.resize(required_size)
            face_array.append((asarray(image), (x1, y1, x2, y2)))  # Add face and bounding box
        return face_array, results

    def process_images(self):
        """Process all images in the input folder."""
        for filename in os.listdir(self.input_folder):
            try:
                print(f"Processing file: {filename.encode('utf-8', errors='ignore').decode('utf-8')}")
                img1 = cv2.imread(os.path.join(self.input_folder, filename))

                if img1 is None:
                    print(f"Failed to read image {filename}. Skipping.")
                    continue

                # Extract faces from the image
                faces, results = self.extract_face(img1)
                print(f"Number of faces detected: {len(faces)}")

                if len(faces) > self.max_faces:
                    self.max_faces = len(faces)
                    self.image_with_max_faces = img1.copy()  # Keep the original image
                    self.detected_faces = faces
                    self.bounding_boxes = results

                # Save extracted faces to the output folder
                for j in range(len(faces)):
                    output_path = os.path.join(self.output_folder, filename[:2] + 'f_' + str(j) + '.jpg')
                    cv2.imwrite(output_path, faces[j][0])

            except UnicodeEncodeError as e:
                print(f"UnicodeEncodeError processing file {repr(filename)}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error processing file {repr(filename)}: {str(e)}")

    def process_extra_images(self, input_files=None):
        """
        Process images passed as a list of numpy arrays.
        """
        if input_files is None:
            print("No images provided for processing.")
            return

        for idx, img1 in enumerate(input_files):
            try:
                # Use the index as a placeholder for the filename
                filename = f'image_{idx + 1}'

                print(f"Processing image {filename}...")

                if img1 is None:
                    print(f"Image {filename} is invalid. Skipping.")
                    continue

                # Extract faces from the image
                faces, results = self.extract_face(img1)
                print(f"Number of faces detected in {filename}: {len(faces)}")

                if len(faces) > self.max_faces:
                    self.max_faces = len(faces)
                    self.image_with_max_faces = img1.copy()  # Keep the original image
                    self.detected_faces = faces
                    self.bounding_boxes = results

                # Save extracted faces to the output folder
                for j in range(len(faces)):
                    output_path = os.path.join(self.output_folder, f'{filename}_face_{j}.jpg')
                    cv2.imwrite(output_path, faces[j][0])

            except Exception as e:
                print(f"Unexpected error processing image {idx + 1}: {str(e)}")

        
    
    def show_image_with_faces(self):
        """Display the image with the most detected faces."""
        if self.image_with_max_faces is not None:
            for box in self.bounding_boxes:
                x1, y1, width, height = box['box']
                x2, y2 = x1 + width, y1 + height
                cv2.rectangle(self.image_with_max_faces, (x1, y1), (x2, y2), (0, 255, 0), 2)
            self.image_with_max_faces = cv2.resize(self.image_with_max_faces, (900, 900))
            img_rgb = cv2.cvtColor(self.image_with_max_faces, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)

            root = ctk.CTk()  
            root.title("Detected Faces in Image")

            # Create a frame to hold the buttons and image
            top_frame = ctk.CTkFrame(root)
            top_frame.pack(side=ctk.TOP, fill=ctk.X)

            # Left button (destroy window)
            left_button = ctk.CTkButton(top_frame, text="Close Window", command=root.destroy)
            left_button.pack(side=ctk.LEFT, padx=10, pady=10)

            # Right button (Capture Images, disable button, and then close the window)
            def on_right_button_click():
                right_button.configure(state="disabled")  # Disable the button after click
                self.capture_images()  # Capture the images
                self.process_extra_images(input_files=self.input_extra_images)
                root.destroy()  # Close the window after capturing images

            right_button = ctk.CTkButton(top_frame, text="Add Image's", command=on_right_button_click)
            right_button.pack(side=ctk.RIGHT, padx=10, pady=10)

            # Create a canvas to display the image
            canvas = ctk.CTkCanvas(root, width=900, height=900)
            canvas.pack()

            # Convert the image to Tkinter format and display it
            img_tk = ImageTk.PhotoImage(img_pil)
            canvas.create_image(0, 0, anchor="nw", image=img_tk)

            root.mainloop()
        else:
            print("No image with faces detected.")

    def capture_images(self):
        """
        Capture images from the webcam and store them in memory for processing.
        """
        cnt = 0
        self.num_images = 6
        self.sleep_time = 0  # Adjust sleep time as needed
        self.input_extra_images = []  # List to store captured images as numpy arrays

        # Initialize webcam
        self.webcam = cv2.VideoCapture(0)

        while cnt < self.num_images:
            check, frame = self.webcam.read()

            if check:
                # Store the captured frame in the list
                self.input_extra_images.append(frame)
                print(f"Image {cnt + 1} captured and stored in memory.")

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

# Main function to parse arguments and run the processor
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process classroom images to detect faces.")
    parser.add_argument('--input_folder', type=str, default='class_room_images', help='Directory of input images')
    parser.add_argument('--output_folder', type=str, default='pre_process_images', help='Directory to save pre-processed images')
    parser.add_argument('--showpopup', action='store_true', help='Show pop-up with images if enabled')

    args = parser.parse_args()

    # Initialize the ClassroomImageProcessor class with provided arguments
    processor = ClassroomImageProcessor(input_folder=args.input_folder, output_folder=args.output_folder)

    # Process images and show the one with the most faces
    processor.process_images()
    if(args.showpopup):
        processor.show_image_with_faces()
    
