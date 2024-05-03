# Animal-Detection-Project


[user_crop.py](Script_Files/user_crop.py)

Here is a preprocessing GUI system that allows a user to choose to square or ellipse crop a video that will black out the surround of the chosen ROI. 

[background_sub.py](Script_Files/background_sub.py)

Apply background subtraction to an entire video using either an input frame or the first frame of the video. There are two options: blacking out the entire background or greenscreening it for increased contrast and better detection.

[new_video_crop_trident.py](Script_Files/new_video_crop_trident.py)
[video_crop_horizontal_halve.py](Script_Files/video_crop_horizontal_halve.py)
[video_crop_vertical_halve.py](Script_Files/video_crop_vertical_halve.py)

Crop a video into either a trident, horizontal halve, or vertical halve to allow for better detection from MegaDetector. The hope is to have the system try each crop type on a small portion of the input video type and see which has the best detection results. Currently, the trident is used on turtles moving around in an elliptical pen. 


[get_avg_width_height_bb.py](Script_Files/get_avg_width_height_bb.py)

Find the average width and height of the bounding boxes produced by MegaDetector. The average will favor the animal in question being detected, so if there are any miscellaneous misdetections, we can eliminate them based on a different-sized bounding box. 


[json_extracter.py](Script_Files/json_extracter.py)

Take the output .json files from MegaDetector and apply reverse transform from cropping if needed to combine data into a .csv file that contains the timestamp and x,y coordinates of the detection. I will check to make sure the detection is legitimate based on average bounding box data generated from [get_avg_width_height_bb.py](Script_Files/get_avg_width_height_bbb.py). 

[json_extracter_seperatefiles.py](Script_Files/json_extracter_seperatefiles.py)

It is the same as [json_extracter.py](Script_Files/json_extracter.py) but will take multiple JSON files for separate animals and save the data to a CSV for each individual animal.

[apply_transform.py](Script_Files/apply_transform.py)

Apply a transform to the data based on the major/minor ellipse axis size. Eventually, in a more robust system, this file will be able to take in multiple different parameters related to camera angle, camera distance, aspect ratio, etc. to transform the data back into real metrics. 


[flag_still.py](Script_Files/flag_still.py)

Find and flag locations in the dataset where the animal in the frame was undetected for prolonged periods. Save in a CSV file the timestamp of the start and end of the misdetection and the descriptor ('still' or 'moving'). 


[build_output_video.py](Script_Files/build_output_video.py)

Using the original video file, build an output video and mark where in the video there were missed detections based on the [Flag](Script_Files/flag_still.py) file. Also, add circular marks to the organism throughout its movement based on the output movement and timestamp data gathered from MegaDetector. This video will be used in the [GUI file](Script_Files/add_video_flags_kivy.py).


[GUI add_video_flags_kivy.py](Script_Files/add_video_flags_kivy.py)

This program builds what will be the GUI system that a user interacts with after processing the set of videos. Right now, the program will take an input video and a CSV file containing where the [Flag](Script_Files/flag_still.py) file finds a section of the video where the animal was not detected for an extended period of time. 

In the future, this program should allow a user to check the states and change them. Then, it should allow the user to input data points by selecting points and performing polynomial interpolation to add even more data points to the set and create a continuous set. 

[tortuosity.py](Script_Files/tortuosity.py)



