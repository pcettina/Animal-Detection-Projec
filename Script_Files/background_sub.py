import argparse
import os
import cv2
import numpy as np
def sub_background(input_video_path, type, background_video):
    # Load video
    cap = cv2.VideoCapture(input_video_path)
    cap_back = cv2.VideoCapture(background_video)
    # Capture background
    _, background = cap_back.read()
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{input_video_path[:len(input_video_path)-4]}_sub.mp4', fourcc, fps, (width, height))

    green_color = (0, 255, 0)

    if type == "black" :

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
            
            # Write the processed frame to output video
            out.write(result)
    else:
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
            thresh_inv = cv2.bitwise_not(thresh)
            
            # Create green background frame
            green_background = np.full_like(frame, green_color, dtype=np.uint8)
            
            # Combine the original frame and the green background using the mask
            result = cv2.bitwise_and(frame, frame, mask=thresh)
            result += cv2.bitwise_and(green_background, green_background, mask=thresh_inv)
            
            # Write the processed frame to output video
            out.write(result)

    # Release video objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Conduct background subtraction on each frame with a frame that does not contain the animal.')
    parser.add_argument('input_video', type = str, help='Input video folder path')
    parser.add_argument('background', type = str, help='background to subtract')

    parser.add_argument('--type', type=str, choices=['black', 'green'], default='black',help='type of background subtraction')
    args = parser.parse_args()
    # Get the input video path
    input_folder = args.input_video
    type = args.type
    background = args.background
    # Check if the input video file exists
    if not os.path.exists(input_folder):
        print('Error: Input video file not found.')
        exit()
    # Call the function to split the videos and create CSV
    sub_background(input_folder, type, background)