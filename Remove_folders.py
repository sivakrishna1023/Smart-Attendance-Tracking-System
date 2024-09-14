import os
import shutil


if os.path.exists("class_room_images"):
    shutil.rmtree("class_room_images")
    print("Deleted the class_room_images")
else:
    print("Directory 'class_room_images' does not exist.")


if os.path.exists("pre_process_images"):
    shutil.rmtree("pre_process_images")
    print("Directory 'pre_process_images' has been removed.")
else:
    print("Directory 'pre_process_images' does not exist.")

if os.path.exists("attendance_file.csv"):
    os.remove("attendance_file.csv")
    print("File 'attendance_file.csv' has been removed.")
else:
    print("File 'attendance_file.csv' does not exist.")
	


		
