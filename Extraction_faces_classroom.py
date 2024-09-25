import sys
import tensorflow as tf
from tensorflow import keras
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from numpy import asarray
import mtcnn
from mtcnn.mtcnn import MTCNN

# Setting up environment variables for TensorFlow
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# Handling encoding issues on Windows
if os.name == 'nt':  # Apply only on Windows
    import ctypes
    ctypes.windll.kernel32.SetConsoleCP(65001)
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Getting the current working directory
current_directory = os.getcwd()

# Define the input and output folder paths dynamically
input_folder = os.path.join(current_directory, 'class_room_images')
output_folder = os.path.join(current_directory, 'pre_process_images')

# Create output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Function to extract faces from an image
def extract_face(img, required_size=(224, 224)):
    # Create the detector, using default weights
    detector = MTCNN()
    # Detect faces in the image
    results = detector.detect_faces(img)
    face_array = []
    for i in range(len(results)):
        x1, y1, width, height = results[i]['box']
        x2, y2 = x1 + width, y1 + height
        face = img[y1:y2, x1:x2]
        # Resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array.append(asarray(image))
    return face_array

# Processing each image in the input folder
cnt = 0
for filename in os.listdir(input_folder):
    try:
        # Safely print filenames
        print(f"Processing file: {filename.encode('utf-8', errors='ignore').decode('utf-8')}")
        img1 = cv2.imread(os.path.join(input_folder, filename))
        
        # Skip if the image could not be read
        if img1 is None:
            print(f"Failed to read image {filename}. Skipping.")
            continue

        # Resize the image
        img1 = cv2.resize(img1, (224, 224))
        # Extract faces from the image
        pixels = extract_face(img1)
        print(f"Number of faces detected: {len(pixels)}")

        # Save extracted faces to the output folder
        for j in range(len(pixels)):
            output_path = os.path.join(output_folder, filename[:2] + 'f_' + str(cnt) + '.jpg')
            cv2.imwrite(output_path, pixels[j])
            cnt += 1

        print(f"Finished processing {filename}")

    except UnicodeEncodeError as e:
        print(f"UnicodeEncodeError processing file {repr(filename)}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error processing file {repr(filename)}: {str(e)}")

print("All images processed successfully.")



# import sys
# import os
# import cv2
# import numpy as np
# from PIL import Image
# from numpy import asarray
# from mtcnn.mtcnn import MTCNN

# # Set TensorFlow environment variables and suppress warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# def main():
#     # Handling encoding issues on Windows
#     if os.name == 'nt':  # Apply only on Windows
#         import ctypes
#         ctypes.windll.kernel32.SetConsoleCP(65001)
#         ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        
#     # Configure stdout and stderr encoding for consistent output
#     sys.stdout.reconfigure(encoding='utf-8')
#     sys.stderr.reconfigure(encoding='utf-8')

#     # Getting the current working directory
#     current_directory = os.getcwd()

#     # Define the input and output folder paths dynamically
#     input_folder = os.path.join(current_directory, 'class_room_images')
#     output_folder = os.path.join(current_directory, 'pre_process_images')

#     # Create output directory if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.mkdir(output_folder)

#     # Function to extract faces from an image
#     def extract_face(img, required_size=(224, 224)):
#         try:
#             # Create the detector, using default weights
#             detector = MTCNN()
#             # Detect faces in the image
#             results = detector.detect_faces(img)
#             face_array = []
#             for i in range(len(results)):
#                 x1, y1, width, height = results[i]['box']
#                 x2, y2 = x1 + width, y1 + height
#                 face = img[y1:y2, x1:x2]
#                 # Resize pixels to the model size
#                 image = Image.fromarray(face)
#                 image = image.resize(required_size)
#                 face_array.append(asarray(image))
#             return face_array
#         except Exception as e:
#             print(f"Error in face extraction: {str(e)}")
#             return []

#     # Processing each image in the input folder
#     cnt = 0
#     for filename in os.listdir(input_folder):
#         try:
#             # Safely print filenames
#             print(f"Processing file: {filename.encode('utf-8', errors='ignore').decode('utf-8')}")
#             img1 = cv2.imread(os.path.join(input_folder, filename))
            
#             # Skip if the image could not be read
#             if img1 is None:
#                 print(f"Failed to read image {filename}. Skipping.")
#                 continue

#             # Resize the image
#             img1 = cv2.resize(img1, (224, 224))
#             # Extract faces from the image
#             pixels = extract_face(img1)
#             print(f"Number of faces detected: {len(pixels)}")

#             # Save extracted faces to the output folder
#             for j in range(len(pixels)):
#                 # Encode the filename to handle any special characters
#                 encoded_filename = filename.encode('utf-8', errors='ignore').decode('utf-8')
#                 output_path = os.path.join(output_folder, encoded_filename[:2] + 'f_' + str(cnt) + '.jpg')
#                 cv2.imwrite(output_path, pixels[j])
#                 cnt += 1

#             print(f"Finished processing {filename}")

#         except UnicodeEncodeError as e:
#             print(f"UnicodeEncodeError processing file {repr(filename)}: {str(e)}")
#         except Exception as e:
#             print(f"Unexpected error processing file {repr(filename)}: {str(e)}")

#     print("All images processed successfully.")

# # This ensures the main function runs only if this script is executed directly
# if __name__ == "__main__":
#     main()
