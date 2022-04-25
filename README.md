# duplicate_remove

Approach steps : 

Step 1 : Check if all the files in the directory are valid or not, if valid then append it onto a list, if not then then remove the image from the directory.

Step 2 : Initialise two new directories. One new directory where all the resized images are kept and another new directory where all the removed images are kept (in order to have the last look at them before permanently deleting them)

Step 3 : After removing all the faulty files from the original directory, resize all the images to a certain dimesnion, default value is taken (480,640), and store these images into a new resized directory.

Step 4 : Now remove the duplicate files by comparing one image to rest of the images in the directory using the given two functions (preprocess and compare). As a result of this comparison we will get a score value for these 2 images.

Step 5 : Put a threshold score value condition (default is 50), if the score value is lesser than threshold value then it gets categorised as duplicate otherwise it isn't duplicate. If it is duplicate then it gets pushed onto another dictionary where we are keeping a count of how many duplicates (and which one) 

Step 6 : Compare the resized and removed images directory. If there is an image that exists in both of these directories then it should be removed from resized directory, leading to removing of all duplicated/non-essential files. This option is kept by default False so that accidentally we don't end up removing images without being sure.

In order to run the file, following command can be used to run after installing the libraries using "requirements.txt" file :
~~~
python solution.py --original_dir /path/to/dataset --resized_dir /path/to/resized_dataset --rmvd_dir /path/to/removed_dataset --width 640 --height 480 --min_contour_area 750 --thresh_score 50 --rmv_dupes False
~~~
