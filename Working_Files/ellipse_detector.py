import cv2
import numpy as np
import os
import argparse
#have to test
def detect_ellipse(folder_path):
    file_path = os.listdir(folder_path)
    print(file_path)
    for video_name in file_path:
        if video_name.endswith('.mp4' or '.MP4'):
            video_path = os.path.join(folder_path, video_name)
            video_capture = cv2.VideoCapture(video_path)

            # Get the frame width and height
            frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Calculate the new width of the ellipse (a little smaller than the entire frame)
            ellipse_width = int(frame_width * 0.48)  # Adjust this value as needed
            ellipse_height = int(frame_height * 0.46)

            # Calculate the new ellipse center to move it up and to the left slightly
            ellipse_center_x = int(frame_width * 0.5) - 20  # Move to the left
            ellipse_center_y = int(frame_height * 0.5) - 30  # Move up

            # Create a mask for the updated ellipse size and position
            mask = np.zeros((frame_height, frame_width), dtype=np.uint8)
            ellipse_center = (ellipse_center_x, ellipse_center_y)
            ellipse_axes = (ellipse_width, ellipse_height)
            cv2.ellipse(mask, ellipse_center, ellipse_axes, 0, 0, 360, 255, -1)

            # Define the codec and create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'H264')  # Use 'MP4V' for another codec
            out = cv2.VideoWriter(f'{folder_path}/outputs/output_{video_name[:len(video_name)-5]}.mp4', fourcc, 30.0, (frame_width, frame_height))

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break

                # Apply the mask to the frame to black out pixels outside the updated ellipse
                result_frame = cv2.bitwise_and(frame, frame, mask=mask)

                # Write the frame to the output video
                out.write(result_frame)

                # Optional: Uncomment the line below to display the frame (commented to not display)
                # cv2.imshow('Frame', result_frame)

                # Comment the following lines to not wait for user input and automatically process the video
                # if cv2.waitKey(30) & 0xFF == ord('q'):
                #     break

            # Release the VideoCapture and VideoWriter objects
            video_capture.release()
            out.release()

            # Destroy any OpenCV windows
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Black out surround of a detected ellipse')
    parser.add_argument('video_folder', help='Path to the folder containing input video files')
    args = parser.parse_args()

    # Blackout around the ellipse for each video the folder
    detect_ellipse(args.video_folder)
