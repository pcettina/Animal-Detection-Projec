#https://chat.openai.com/share/f7d127f8-7da4-4751-9683-243c82731246
#help above

import cv2
import numpy as np
import os

cwd = os.getcwd()

video_name = 'output_Snapper_12_Exploration_part_background.mp4'
video_path = os.path.join(cwd, video_name)

print('Video path:', video_path)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print('Error: Could not open the video.')
    exit()

# Video info
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Half borders
left_half_width = int(frame_height * 0.5)  # Adjust the portion of the top half as needed
right_half_width = frame_height - left_half_width

output_right_video = cv2.VideoWriter(f'{video_name[:len(video_name)-4]}_top.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, left_half_width))
output_left_video = cv2.VideoWriter(f'{video_name[:len(video_name)-4]}_bottom.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height - left_half_width))


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Split the frame into top and bottom halves
    left_half = frame[:, 0:left_half_width]
    right_half = frame[:, left_half_width:frame_width]

    # Write the output frames to separate videos
    output_right_video.write(left_half)
    output_left_video.write(right_half)

# Release resources
cap.release()
output_right_video.release()
output_left_video.release()

print('Video processing completed. Output saved to: output_top_video.mp4 and output_bottom_video.mp4')
