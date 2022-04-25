import cv2
import imutils
import os
#import time
import numpy as np
import imutils
import shutil
import argparse as ap
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from imageio import imread
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection

parser = ap.ArgumentParser(description='Duplicate_Removal')

parser.add_argument('--original_dir', default='../dataset/',
	help='Original dataset directory')
parser.add_argument('--resized_dir', default='../resized_dataset/',
	help='Directory for resized images')
parser.add_argument('--rmvd_dir', default='../rmvd_dataset/',
	help='diretory for removed images')
parser.add_argument('--width', type=int, default=640,
	help='Width of the images to be resized')
parser.add_argument('--height', type=int, default=480,
	help="Height of the images to be resized")
parser.add_argument('--min_contour_area', type = int, default=750,
	help="Value of minimum contour area to be chosen in order to remove duplicates")
parser.add_argument('--thresh_score', type = int, default = 50,
	help="Value of threshold score to accept duplicate images")
parser.add_argument('--rmv_dupes', type = bool, default=False,
	help="True in case you want to remove duplicate files from the resized directory")

args = parser.parse_args()

def get_files(directory):
    file_list = []
    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        if os.path.isfile(full_path):
            file_list.append(full_path)
    return file_list

def img_check(file_list):

    file_size = defaultdict(list)
    faulty_files = []
    for i in range(len(file_list)):

        try:
        	#Read the image using opencv
            ig = cv2.imread(file_list[i])    

            #Get width and height of each image
            dimensions = (ig.shape[0], ig.shape[1])

            #Push dim along with image name onto a dictionary
            file_size[dimensions].append(file_list[i]) 

        except:

            faulty_files.append(file_list[i])

            #Remove the file from the directory
            os.remove(file_list[i])    

    return file_size, faulty_files

def resize_img(file_list, new_path, width, height):

    for i in range(len(file_list)):

        try:

            img = cv2.imread(file_list[i], cv2.IMREAD_UNCHANGED)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            name = file_list[i].split("/")[-1]
            cv2.imwrite(os.path.join(new_path, name), resized)

        except:
            print("File not found/resized, Error with file path", file_list[i])


def rm_duplicates(images, rmvd_path, min_contour_area, thresh_score):

    duplicates = {}
    matched = defaultdict(list)
    print("Starting matching process")

    '''
    In the following for loop, each image is being compared to rest of the images in the directory,
    then gets passed to compare_frame function where it gets the score between these two images. 
    This score is then compared to this threshold value, if it's lesser than value it gets categorized
    as duplicates and then gets pushed onto the matched dictionary along with the image that it's beiing matched.
    This also gets copied to a directory where all the removed images are stored.
    '''

    for i in range(len(images)): #
        if (i % 10 == 0):
            print(i,"files matching done")
        if images[i] in duplicates:
            continue   
        for j in range(i + 1,len(images)):
            if images[j] in duplicates:
                continue
            proc_prev = preprocess_image_change_detection(cv2.imread(images[i]),gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0))
            proc_next = preprocess_image_change_detection(cv2.imread(images[j]),gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0))
            score = compare_frames_change_detection(proc_prev, proc_next, min_contour_area)[0]     
            if(score < thresh_score):
                matched[images[i]].append([images[j]])
                duplicates[images[j]] = 1
                shutil.copy(images[j], rmvd_path)

def rm_duplicates_dir(big_dir, rmvd_dir):

	dir_big = []
	dir_rmvd = set()

	for fileA in os.listdir(big_dir):
		dir_big.append(fileA)
	for fileB in os.listdir(rmvd_dir):
		dir_rmvd.add(fileB)

	for fileA in dir_big:
		if fileA in dir_rmvd:
			os.remove(os.path.join(big_dir,(fileA)))


if __name__ == '__main__':

	file_list = get_files(args.original_dir)
	file_size, faulty = img_check(file_list)  #For visualization and analysis purposes

	print("Total number of images are", len(file_list))
	print("Number of images that are faulty/can't be opened are", len(faulty))

	resize_img(file_list, args.resized_dir, width = args.width, height = args.height)
	img_list = get_files(args.resized_dir)
	print("Total number of resized images to be matched are",len(img_list))

	rm_duplicates(img_list, args.rmvd_dir, args.min_contour_area, args.thresh_score)

	if(args.rmv_dupes):
		rm_duplicates_dir(args.resized_dir, args.rmvd_dir)
