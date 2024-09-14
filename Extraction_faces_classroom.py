import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from mtcnn.mtcnn import MTCNN
import customtkinter as ctk
from tkinter import Label, Canvas, Scrollbar

# Extract faces and return them along with the image with boxes drawn
def extract_face_and_draw_boxes(img, required_size=(224, 224)):
    detector = MTCNN()
    results = detector.detect_faces(img)
    
    face_array = []
    for i, face_data in enumerate(results):
        x1, y1, width, height = face_data['box']
        x2, y2 = x1 + width, y1 + height

        # Make sure box coordinates are within image dimensions
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)

        # Draw green box around the face
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Extract face from the image
        face = img[y1:y2, x1:x2]
        face_image = Image.fromarray(face)
        face_array.append(np.asarray(face_image))

    return face_array, img

# Process images: Extract faces, store them, and return list for GUI display
def process_and_store_images():
    current_directory = os.getcwd()
    input_folder = os.path.join(current_directory, 'class_room_images')
    output_folder = os.path.join(current_directory, 'pre_process_images')

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Directory {input_folder} not found.")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    image_filenames = os.listdir(input_folder)
    images_with_boxes = []
    cnt = 0

    for filename in image_filenames:
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to read {filename}. Skipping.")
            continue

        # Extract faces and draw bounding boxes
        faces, img_with_boxes = extract_face_and_draw_boxes(img)

        # Save the extracted faces in 'pre_process_images' folder
        for i, face in enumerate(faces):
            save_path = os.path.join(output_folder, f'{filename[0:2]}_face_{cnt}.jpg')
            cv2.imwrite(save_path, face)
            cnt += 1

        # Store image with bounding boxes for later display
        images_with_boxes.append(img_with_boxes)

    return images_with_boxes

# Function to display images in the GUI with scrollable grid layout
def display_images(images):
    root = ctk.CTk()  # Create the main window
    root.geometry("1200x800")
    root.title("Face Detection Results")

    # Create a canvas with a scrollbar
    canvas = Canvas(root, width=1100, height=750)
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas)

    # Configure the canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Set fixed image size and number of columns
    image_size = (600, 400)  # Fixed size for each image
    num_columns = 3  # Number of images per row
    row, col = 0, 0

    for img in images:
        # Convert each image to ImageTk format and resize it to fixed size
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize(image_size)  # Resize image to fixed size
        img_tk = ImageTk.PhotoImage(img_pil)

        # Create and display label with image
        label = Label(scrollable_frame, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.grid(row=row, column=col, padx=10, pady=10)

        # Update row and column for the next image
        col += 1
        if col >= num_columns:  # Move to the next row after 3 images
            col = 0
            row += 1

    root.mainloop()

# Main logic
if __name__ == "__main__":
    # First, process the images and store them
    processed_images = process_and_store_images()

    # If there are images, display them in the customtkinter GUI
    if processed_images:
        display_images(processed_images)
    else:
        print("No images to display.")
