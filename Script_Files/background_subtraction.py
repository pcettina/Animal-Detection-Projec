import argparse
import os
import cv2
import numpy as np

def sub_background(input_video_path):
    # Load video
    cap = cv2.VideoCapture(input_video_path)

    # Capture background
    _, background = cap.read()
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute absolute difference between background and frame
        diff = cv2.absdiff(gray, background_gray)
        
        # Apply threshold to get binary mask
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Perform morphological operations (optional)
        kernel = np.ones((5,5),np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Apply mask to original frame
        result = cv2.bitwise_and(frame, frame, mask=thresh)
        
        cv2.imshow('Result', result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Split a video into Trident and save each part as a separate video.')
    parser.add_argument('input_video', help='Input video folder path')
    args = parser.parse_args()

    # Get the input video path
    input_folder = args.input_video

    # Check if the input video file exists
    if not os.path.exists(input_folder):
        print('Error: Input video file not found.')
        exit()

    # Call the function to split the videos and create CSV
    sub_background(input_folder)
