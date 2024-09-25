import os
import numpy as np
import cv2
import csv
import tensorflow as tf
from numpy import expand_dims
from numpy.linalg import norm
from tensorflow.keras.applications import ResNet50
import collections

# Function to run the main logic
def main():
    IMG_HEIGHT, IMG_WIDTH = 224, 224
    restnet = ResNet50(include_top=False, weights='imagenet', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))

    current_directory = os.getcwd()
    Database_path = os.path.join(current_directory, 'Database')
    Extracted_images_path = os.path.join(current_directory, 'pre_process_images')

    # Check if directories exist
    if not os.path.exists(Database_path):
        raise FileNotFoundError(f"Directory {Database_path} not found.")
    if not os.path.exists(Extracted_images_path):
        raise FileNotFoundError(f"Directory {Extracted_images_path} not found.")

    mylist = np.sort(os.listdir(Extracted_images_path))
    Database_list = np.sort(os.listdir(Database_path))

    db_fd = []
    for filename in Database_list:
        img = cv2.imread(os.path.join(Database_path, filename), 0)
        img1 = cv2.resize(img, (224, 224), interpolation=cv2.INTER_NEAREST)
        fd2 = expand_dims(img1, axis=-1)
        fd3 = fd2.repeat(3, axis=-1)
        x1 = np.reshape(fd3, (1, 224, 224, 3))
        x1 = restnet(x1)   # RESNET MODEL
        f = np.reshape(x1, (1, -1), order='F')
        f = np.reshape(f, f.shape[1], order='F')
        db_fd.append(f)

    np.save('db_features', db_fd)
    print(len(db_fd[0]))

    cl_img_f = []
    for filename in mylist:
        img = cv2.imread(os.path.join(Extracted_images_path, filename), 0)
        img1 = cv2.resize(img, (224, 224), interpolation=cv2.INTER_NEAREST)
        fd2 = expand_dims(img1, axis=-1)
        fd3 = fd2.repeat(3, axis=-1)
        x1 = np.reshape(fd3, (1, 224, 224, 3))
        x1 = restnet(x1)   # RESNET MODEL
        f = np.reshape(x1, (1, -1), order='F')
        f = np.reshape(f, f.shape[1], order='F')
        cl_img_f.append(f)

    print(len(cl_img_f))

    feature_score = []
    cosine_sim_score = []
    for i in range(len(cl_img_f)):
        f1 = cl_img_f[i]
        score = []
        for j in range(len(db_fd)):
            f2 = db_fd[j]
            cosine = np.dot(f1, f2) / (norm(f1) * norm(f2))
            cosine_sim = (cosine + 1) / 2
            score.append(cosine_sim)
        cosine_sim_score.append(score)

    print(len(cosine_sim_score))

    matched_image_roll = []
    for i in range(len(cosine_sim_score)):
        s = cosine_sim_score[i]
        score_indices = np.argmax(s)
        a, b = [mylist[i], Database_list[score_indices]]
        matched_image_roll.append((a, b))

    np.save('mapped_features', matched_image_roll)
    print(len(matched_image_roll))

    attendance_list = []
    for i in range(len(matched_image_roll)):
        a, b = matched_image_roll[i]
        a1 = str(b[:-6])
        attendance_list.append((i, a1))

    elements_count = collections.Counter(attendance_list)
    attendance_list1 = []
    keys = []
    for key, value in elements_count.items():
        if value >= 2:
            attendance_list1.append(key)

    unique_rolls = set()
    cleaned_list = []
    counter = 1
    for _, rollnumber in attendance_list:
        cleaned_roll = rollnumber.rstrip('_')
        if cleaned_roll not in unique_rolls:
            unique_rolls.add(cleaned_roll)
            cleaned_list.append((counter, cleaned_roll))
            counter = counter + 1

    # Sort the cleaned list based on roll numbers
    cleaned_list.sort(key=lambda x: x[1])
    attendance_list = cleaned_list

    print(attendance_list)
    with open('attendance_file.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(attendance_list)

# This ensures the main function runs only if this script is executed directly
if __name__ == "__main__":
    # Optional: Disable TensorFlow debugging logs
    tf.get_logger().setLevel('ERROR')
    main()
