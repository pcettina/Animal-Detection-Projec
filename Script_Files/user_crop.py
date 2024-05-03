import cv2
import argparse
import numpy as np
import csv

def select_rectangular_roi(frame):
    # Display the frame and prompt user to select rectangular ROI
    roi = cv2.selectROI("Select Rectangular ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Rectangular ROI")
    return roi

def select_elliptical_roi(frame):
    # Display the frame and prompt user to select elliptical ROI
    roi = cv2.selectROI("Select Elliptical ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Elliptical ROI")
    return roi

def process_video(input_video, output_video, ellipse_data, roi_type):
    # Open the input video file
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    
    if not cap.isOpened():
        print("Error: Couldn't open video file")
        return

    # Get the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read the first frame")
        return

    # Select ROI based on user choice
    if roi_type == 'rectangular':
        roi = select_rectangular_roi(frame)
    elif roi_type == 'elliptical':
        roi = select_elliptical_roi(frame)
    else:
        print("Error: Invalid ROI type")
        return

    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    
    #Show video creation
    show = True
    data_written = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Black out everything outside the ROI
        masked_frame = frame.copy()

        if roi_type == 'rectangular':
            masked_frame[:, :roi[0]] = 0
            masked_frame[:, roi[0] + roi[2]:] = 0
            masked_frame[:roi[1], :] = 0
            masked_frame[roi[1] + roi[3]:, :] = 0
        elif roi_type == 'elliptical':
            mask = np.zeros((frame_height, frame_width), dtype=np.uint8)
            cv2.ellipse(mask, ((roi[0] + roi[2] // 2), (roi[1] + roi[3] // 2)), (roi[2] // 2, roi[3] // 2), 0, 0, 360, (255, 255, 255), -1)
            if(data_written == False):

                with open(ellipse_data, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['Metric', 'x', 'y'])
                    writer.writeheader()
                    center = ((roi[0] + roi[2] // 2), (roi[1] + roi[3] // 2))
                    axis_sizes = (roi[2] // 2, roi[3] // 2)
                    # metrics = [('center', center[0], center[1]), ('axis_sizes', axis_sizes[0], axis_sizes[1])]
                    
                    
                    writer.writerow({'Metric': 'center', 'x': center[0], 'y': center[1]})
                    writer.writerow({'Metric': 'axis_sizes', 'x': axis_sizes[0], 'y': axis_sizes[1]})
                data_written = True

            
            masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
 
        
        out.write(masked_frame)

        # Display the masked frame
        if(show):
            cv2.imshow("Masked Frame", masked_frame)

        # Exit on 'q' press
        if cv2.waitKey(25) & 0xFF == ord('q'):
            show = False 
            cv2.destroyAllWindows()
            print("output video still being made")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('input_video_file', type=str, help='Path to the input video file')
    parser.add_argument('output_video_file', type=str, help='Path to the output video file')
    parser.add_argument('ellipse_size_data', type=str, help='Path to ellipse data output csv')
    parser.add_argument('--roi_type', type=str, choices=['rectangular', 'elliptical'], default='rectangular', help='Type of ROI to select (rectangular or elliptical)')

    # Parse the arguments
    args = parser.parse_args()   
    process_video(args.input_video_file, args.output_video_file, args.ellipse_size_data,args.roi_type)
