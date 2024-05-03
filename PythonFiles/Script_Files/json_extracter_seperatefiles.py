# https://chat.openai.com/share/0b6f949b-6358-45d4-bf29-da9ad147f22c
# make parallel so it takes much less time
import os
import json
import csv
import argparse
import numpy as np

# Might want to check width and height of box against average to 
# eliminate misdetections ... 
# Add in the average width and height csv file to check against
def calculate_midpoint(bbox, bbox_metadata_csv, prev_x, prev_y):
    xmin, ymin, width, height = bbox

    # Gather average bounding box sizes to check against current box
    bbox_data = np.genfromtxt(bbox_metadata_csv, delimiter=',', names=['average_width', 'average_height'], skip_header=1)
    avg_width, avg_height = bbox_data['average_width'], bbox_data['average_height']
    avg_diagonal = np.sqrt(avg_width**2 + avg_height**2)
    


    midpoint_x = (xmin + width*0.5)
    midpoint_y = (ymin + height*0.5)

    if(prev_x != None):

        euclidean_dist = np.sqrt((midpoint_x-prev_x)**2 + (midpoint_y-prev_y)**2)

    # Check if euclidean distance between current and previous point is greater than the avg diagonal size of a bounding box
        if(avg_diagonal > euclidean_dist):
            return None

    return [midpoint_x, midpoint_y]

def extract_highest_confidence_midpoints_from_folder(folder_path, conf_threshold, video_metadata_csv, bbox_metadata_csv,frames_per_second=30):
    # Load video metadata from the provided CSV
    with open(video_metadata_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_width = int(row['video_width'])
            video_height = int(row['video_height'])
            break  # Assuming there is only one row in the CSV for a single video

    

    # Iterate through JSON files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            output_csv = os.path.join(folder_path, filename[:-5] + ".csv")
            with open(output_csv, 'w', newline='') as csvfile:
                fieldnames = ['t', 'x', 'y']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                prev_x = None
                prev_y = None


                with open(os.path.join(folder_path, filename), 'r') as f:
                    data = json.load(f)['images']

                # Iterate through frames
                frame_number = 0
                for frame_data in data:
                    detections = frame_data['detections']
                    frame_number += 1
                    
                    
                    # Initialize variables to track highest confidence detection
                    highest_confidence_detection = None
                    highest_confidence = 0.0

                    # Iterate through detections in the frame
                    for detection in detections:
                        confidence = detection['conf']

                        # Check if this detection is an animal (category '1') and has higher confidence
                        if (detection.get('category') == '1' or detection.get('category') == '2') and confidence > conf_threshold and confidence > highest_confidence:
                            highest_confidence = confidence
                            highest_confidence_detection = detection
                    if highest_confidence_detection is not None:
                        # Calculate the midpoint of the bounding box with highest confidence
                        # Will want to do for all highest confidene and just not add if size of box is not right
                        bounding_box = highest_confidence_detection['bbox']
                        midpoint = calculate_midpoint(bounding_box, bbox_metadata_csv, prev_x, prev_y)

                        if(midpoint == None):
                            continue

                        prev_x = midpoint[0]
                        prev_y = midpoint[1]

                        # Adjust x and y coordinates based on filename
                        if 'right' in filename:
                            midpoint[0] = (midpoint[0]*.65 + 0.35)

                            midpoint[1] = (midpoint[1]*0.55)
                            
                        elif 'left' in filename:
                            midpoint[0] = (midpoint[0]*.65)
                            midpoint[1] = (midpoint[1]*0.55)
                            

                        elif 'foreground' in filename: # have to figure out how to scale
                            midpoint[0] = midpoint[0]
                            
                            midpoint[1] = (midpoint[1]*0.75 +0.25)

                        # Adjust midpoint based on crop for better detection

                        # Increment time based on the assumption of 30 frames per second
                        time_in_seconds = frame_number / frames_per_second

                        # Write to CSV
                        writer.writerow({'t': time_in_seconds, 'x': midpoint[1], 'y': midpoint[0]})

# go through csv and take average when there are points at same time stamp

    

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract highest confidence midpoints from JSON files in a folder and save to a combined CSV.')
    parser.add_argument('json_folder', help='Path to the folder containing input JSON files')
    parser.add_argument('video_metadata_csv', help='Path to the CSV file containing video metadata (width and height)')
    parser.add_argument('bbox_metadata_csv', help='Path to the CSV file containing the average width and height of bbox for a video')
    parser.add_argument('--frames_per_second', type=int, help='Frames per second of video that is processing')
    parser.add_argument('--confidence_threshold', type=float, default=0.35, help='Confidence threshold (default: 0.35)')

    args = parser.parse_args()

    # Extract highest confidence midpoints and save to combined CSV
    extract_highest_confidence_midpoints_from_folder(args.json_folder, args.confidence_threshold, args.video_metadata_csv, args.bbox_metadata_csv, frames_per_second=args.frames_per_second)
