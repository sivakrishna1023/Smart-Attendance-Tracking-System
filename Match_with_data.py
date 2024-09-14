import os
import numpy as np
import cv2

import csv
import tensorflow 

from numpy import load
from numpy import expand_dims
from numpy import asarray
from numpy.linalg import norm

from tensorflow import keras 

import collections


# example of loading the resnet50 model
#from keras.applications.resnet50 import ResNet50
# load model
#model = ResNet50()
# summarize the model


from tensorflow.keras.applications import ResNet50


IMG_HEIGHT,IMG_WIDTH=224,224
restnet = ResNet50(include_top=False, weights='imagenet', input_shape=(IMG_HEIGHT,IMG_WIDTH,3))

current_directory = os.getcwd()

Database_path = os.path.join(current_directory, 'Database')

Extracted_images_path = os.path.join(current_directory, 'pre_process_images')

if not os.path.exists(Database_path):
    raise FileNotFoundError(f"Directory {Database_path} not found.")
if not os.path.exists(Extracted_images_path):
    raise FileNotFoundError(f"Directory {Extracted_images_path} not found.")

mylist=np.sort(os.listdir(Extracted_images_path))

Database_list=np.sort(os.listdir(Database_path))

print (len(Database_list))
print (Database_list[0])



db_fd=[]
#print mylist
Image_index=[]
Image_index1=[]
f_cnt=0
for filename in Database_list:
    img=cv2.imread(os.path.join(Database_path,filename),0)	
    img1=cv2.resize(img, (224,224),interpolation = cv2.INTER_NEAREST)
    #print (len(fd1))
    #fd2=list(itertools.chain(*fd1))
    fd2=expand_dims(img1, axis=-1)
    fd3=fd2.repeat(3, axis=-1)
    x1=np.reshape(fd3, (1,224,224,3))
    x1=restnet(x1)   #################RESNET MODEL###############
    f=np.reshape(x1, (1,-1), order='F')
    f=np.reshape(f, f.shape[1], order='F')
    db_fd.append(f)
    

np.save('db_features', db_fd)
print (len(db_fd[0]))

cl_img_f=[]


for filename in mylist:
    img=cv2.imread(os.path.join(Extracted_images_path,filename),0)	
    img1=cv2.resize(img, (224, 224),interpolation = cv2.INTER_NEAREST)
    #print (len(fd1))
    #fd2=list(itertools.chain(*fd1))
    fd2=expand_dims(img1, axis=-1)
    fd3=fd2.repeat(3, axis=-1)
    x1=np.reshape(fd3, (1,224,224,3))
    x1=restnet(x1)   #################RESNET MODEL###############
    f=np.reshape(x1, (1,-1), order='F')
    f=np.reshape(f, f.shape[1], order='F')
    cl_img_f.append(f)


print (len(cl_img_f))


feature_score=[]
cosine_sim_score=[]
for i in range(len(cl_img_f)):
	f1=cl_img_f[i]
	score=[]	
	for j in range(len(db_fd)):
		f2=db_fd[j]
		cosine = np.dot(f1,f2)/(norm(f1)*norm(f2))
		cosine_sim=(cosine+1)/2
		score.append(cosine_sim)
	cosine_sim_score.append(score)


 
print (len(cosine_sim_score))


matched_image_roll=[]

for i in range(len(cosine_sim_score)):
	s=cosine_sim_score[i]
	print (len(s))
	score_indices=np.argmax(s)	
	print (score_indices)
	a,b=[mylist[i], Database_list[score_indices]]
	matched_image_roll.append((a,b))
	
	
	
np.save('mapped_features', matched_image_roll)
	
#print (matched_image_roll)


print (len(matched_image_roll))

attendance_list=[]

for i in range(len(matched_image_roll)):
    a,b= matched_image_roll[i]
    a1=str(b[:-6])
    attendance_list.append((i,a1))

elements_count = collections.Counter(attendance_list)
attendance_list1=[]
keys=[]
# printing the element and the frequency
for key, value in elements_count.items():
	#print (key, value)
	#keys.append(value)
	if value>=2:
		attendance_list1.append(key)
		#print (key)

#print (np.sum(keys))
#print (len(attendance_list1))
with open('attendance_file.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(attendance_list)   




	



	




