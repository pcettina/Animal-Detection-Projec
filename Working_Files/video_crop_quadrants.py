#https://chat.openai.com/share/f7d127f8-7da4-4751-9683-243c82731246
#help above


import cv2
import numpy as np
import os

cwd = os.getcwd()

video_name = 'Snapper_12_Exploration_part_1.MP4'
video_path = os.path.join(cwd, video_name)

print('Video path: ', video_path)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened(): #if video opened successfully 
    print('Error: Could not open the video.')
    exit()

#video info

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))


#quadrant borders 
quadrants = [(0, 0, frame_width // 2, frame_height // 2),
             (frame_width // 2, 0, frame_width, frame_height //2),
             (0, frame_height // 2, frame_width // 2, frame_height),
             (frame_width // 2, frame_height // 2, frame_width, frame_height)]

fourcc = cv2.VideoWriter_fourcc(*'mp4v') # codec for output video

output_videos = [cv2.VideoWriter(f'output_{video_name}_quadrant_{i+1}.mp4', fourcc, fps, (frame_width //2, frame_height //2))
                 for i in range(len(quadrants))] #create videowriter for each quadrant


#frame processing
while True:
    ret, frame = cap.read()
    if not ret:
        break


    #crop frames into quadrants and save to outputVid
    for i, (x, y, w, h) in enumerate(quadrants):
        quadrant_frame = frame[y:y+h, x:x+w]
        output_videos[i].write(quadrant_frame)

#save to output folder Cropped_Videos

cap.release()
for output_video in output_videos:
    output_video.release()

print('Video processing completed. Output saved to: ', end=' ')
for i in range(len(quadrants)):
    print(f'output_{video_name[:len(video_name)-5]}_quadrant_{i+1}.mp4', end=', ' if i < len(quadrants) - 1 else '\n')
