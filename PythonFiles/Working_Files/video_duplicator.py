
import cv2
import os
import argparse
import csv

def dup_video(folder_path):
    file_path = os.listdir(folder_path)
    print(file_path)
    for input_video in file_path:
        if input_video.endswith('.mp4'):

            # Open the video
            video_path = os.path.join(folder_path, input_video)
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print('Error: Could not open the video.')
                exit()

            # Get video information
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            
            # Horizontal Half borders
            top_half_height = int(frame_height * 0.4)  # Adjust the portion of the top half as needed
            bottom_half_height = frame_height - top_half_height
            # Vertical Half borders
            left_half_width = int(frame_width * 0.5)  # Adjust the portion of the top half as needed
            right_half_width = frame_width - left_half_width

            # Create VideoWriter objects for each quadrant
            output_top_left_video = cv2.VideoWriter(f'{input_video[:len(input_video)-4]}_top_left_crop.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
            output_top_right_video = cv2.VideoWriter(f'{input_video[:len(input_video)-4]}_top_right_crop.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
            output_bottom_video = cv2.VideoWriter(f'{input_video[:len(input_video)-4]}_foreground_crop.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        #an issue is with bottom v foreground naming
            while True:
                ret, frame = cap.read()
                if not ret:
                    break


                # Write the output frames to separate videos
                output_top_left_video.write(frame)
                output_top_right_video.write(frame)
                output_bottom_video.write(frame)

            # Release resources
            cap.release()
            output_top_left_video.release()
            output_top_right_video.release()
            output_bottom_video.release()

            print('Video processing completed. Output saved to: output_top_left.mp4, output_top_right.mp4, output_bottom.mp4')

    # Write video information to a CSV file
    with open('video_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['video_height', 'video_width']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'video_height': frame_height, 'video_width': frame_width})

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Split a video into Trident and save each part as a separate video.')
    parser.add_argument('input_folder', help='Input video folder path')
    args = parser.parse_args()

    # Get the input video path
    input_folder = args.input_folder

    # Check if the input video file exists
    if not os.path.exists(input_folder):
        print('Error: Input video file not found.')
        exit()

    # Call the function to split the videos and create CSV
    dup_video(input_folder)