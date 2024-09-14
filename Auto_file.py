import subprocess

program_list = ['Remove_folders.py', 'Get_class_images.py', 'Extraction_faces_classroom.py', 'Match_with_data.py', 'send_mail.py']

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)
