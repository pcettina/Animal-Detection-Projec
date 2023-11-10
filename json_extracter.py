# https://chat.openai.com/share/0b6f949b-6358-45d4-bf29-da9ad147f22c
# Now need to figure out how to get actual coordinates and not coordinates from top of bounding box...
# make parallel so it takes much less time
import os
import json
import csv
import argparse

def calculate_midpoint(bbox):
    ymin, xmin, ymax, xmax = bbox
    midpoint_y = (ymin + ymax) / 2
    midpoint_x = (xmin + xmax) / 2
    return [midpoint_y, midpoint_x]

def extract_highest_confidence_midpoints_from_folder(folder_path, output_csv, conf_threshold, video_metadata_csv, frames_per_second=30):
    # Load video metadata from the provided CSV
    with open(video_metadata_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_width = int(row['video_width'])
            video_height = int(row['video_height'])
            break  # Assuming there is only one row in the CSV for a single video

    # Open CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['t', 'x', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through JSON files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
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
                        if detection.get('category') == '1' and confidence > conf_threshold and confidence > highest_confidence:
                            highest_confidence = confidence
                            highest_confidence_detection = detection
                    if highest_confidence_detection is not None:
                        # Calculate the midpoint of the bounding box with highest confidence
                        bounding_box = highest_confidence_detection['bbox']
                        midpoint = calculate_midpoint(bounding_box)

                                        # Adjust x and y coordinates based on filename
                        if 'right' in filename:
                            midpoint[0] += 0.5
                            midpoint[0] *= (video_width) 
                            midpoint[1] *= 0.4
                            midpoint[1] *= (video_height*2)
                            
                        elif 'left' in filename:
                            midpoint[0] *= (video_width)
                            midpoint[1] *= 0.4
                            midpoint[1] *= (video_height*2)
                            

                        elif 'foreground' in filename: # have to figure out how to scale
                            
                            midpoint[0] *= (video_width*2)
                            #midpoint[1] *= (0.6)
                            midpoint[1] +=0.5
                            midpoint[1] *= 0.6 
                            midpoint[1] *= (video_height*2)
                            
                            # midpoint[1] += (video_height*0.4) # find way to add to bottom

                        # Adjust midpoint based on video width and height

                        # Increment time based on the assumption of 30 frames per second
                        time_in_seconds = frame_number / frames_per_second

                        # Write to CSV
                        writer.writerow({'t': time_in_seconds, 'x': midpoint[1], 'y': midpoint[0]})
    

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract highest confidence midpoints from JSON files in a folder and save to a combined CSV.')
    parser.add_argument('json_folder', help='Path to the folder containing input JSON files')
    parser.add_argument('output_csv', help='Path to the output combined CSV file')
    parser.add_argument('video_metadata_csv', help='Path to the CSV file containing video metadata (width and height)')
    parser.add_argument('--confidence_threshold', type=float, default=0.35, help='Confidence threshold (default: 0.35)')

    args = parser.parse_args()

    # Extract highest confidence midpoints and save to combined CSV
    extract_highest_confidence_midpoints_from_folder(args.json_folder, args.output_csv, args.confidence_threshold, args.video_metadata_csv)
