# Animal-Detection-Project


[user_crop.py](Script_Files/user_crop.py)

Here is a preprocessing GUI system that allows a user to choose to square or ellipse crop a video that will black out the surround of the chosen ROI. 


[new_video_crop_trident.py](Script_Files/new_video_crop_trident.py)
[video_crop_horizontal_halve.py](Script_Files/video_crop_horizontal_halve.py)
[video_crop_vertical_halve.py](Script_Files/video_crop_vertical_halve.py)

Crop a video into either a trident, horizontal halve, or vertical halve to allow for better detection from MegaDetector. The hope is to have the system try each crop type on a small portion of the input video type and see which has the best detection results. Currently, the trident was used on turtles moving around in an elliptical pen. 


[get_avg_width_height_bb.py](Script_Files/get_avg_width_height_bb.py)

Find the average width and height of the bounding boxes produced by MegaDetector. The average will favor the animal in question being detected so if there are any miscellaneous misdetections we can eliminate them based on a different sized bounding box. 


[json_extracter.py](Script_Files/json_extracter.py)

Take the output .json files from MegaDetector and apply reverse transform from a cropping if needed to combine data into a .csv file that contains the timestamp and x,y coordinates of the detection. Will check to make sure the detection is legitimate based on average bounding box data generated from [get_avg_width_height_bb.py](Script_Files/get_avg_width_height_bb.py). 


[apply_transform.py](Script_Files/apply_transform.py)

Apply a transform to the data based off of major/minor ellipse axis size. Eventually, in a more robust system this file will be able to take in multiple different parameters related to camera angle, camera distance, aspect ration, etc. in order to transform the data back into real metrics. 


[flag_still.py](Script_Files/flag_still.py)

Find and flag locations in the dataset where there were prolonged periods of undetection of the animal in frame. Save in a csv file the timestamp of the start and end of the misdetection and the descriptor ('still' or 'moving'). 


[build_output_video.py](Script_Files/build_output_video.py)

Using the original video file build an output video and mark where in the video there were missed detections based on the [Flag](Script_Files/flag_still.py) file. Also add circular marks to organism throughout the movement of the organism based on the output movement and timestamp data gather from MegaDetector. This video will be used in the [GUI file](Script_Files/add_video_flags_kivy.py).


[GUI add_video_flags_kivy.py](Script_Files/add_video_flags_kivy.py)

This program builds what will be the GUI system that a user interacts with postprocessing of the set of videos. Right now the program will take an input video and a csv file containing where the [Flag](Script_Files/flag_still.py) file finds section of video where the animal was not detected for an extended period of time. 

In the future this program should allow a user to check the states and change it. Then allow the user to input data points by selecting points and possibility of performing polynomial interpolation to add even more data points to the set and create a continous set. 

