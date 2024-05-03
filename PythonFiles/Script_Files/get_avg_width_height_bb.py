import os
import json
import csv
import argparse



def extract_highest_confidence_midpoints_from_folder(folder_path, output_csv, video_metadata,conf_threshold, frames_per_second=30):
    # Load video metadata from the provided CSV
    with open(video_metadata, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_width = int(row['video_width'])
            video_height = int(row['video_height'])
            break  # Assuming there is only one row in the CSV for a single video
    # Open CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['average_width', 'average_height']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        counter = 0
        width_total = 0
        height_total = 0

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
                        # Grab width and height of bboxes 
                        bounding_box = highest_confidence_detection['bbox']
                        xmin, ymin, width, height = bounding_box

                        #Need to test whether doing these alterations both makes sense and works 
                        # dependent on crop will size of bounding box need to be back adjusted
                        if 'right' in filename:
                            width = (width*.65)

                            height = (height*0.55)
                            
                        elif 'left' in filename:
                            width = (width*.65)
                            height = (height*0.55)
                            

                        elif 'foreground' in filename: 
                            width = width
                            
                            height = (height*0.75)
                        width_total += width
                        height_total += height
                        counter +=1
        #find the average width and height for bounding boxes and adjust from there
        avg_width = (width_total / counter)
        avg_height = (height_total / counter)
        writer.writerow({'average_width': avg_width, 'average_height': avg_height})
        print("average width = " + str(avg_width) + " ,average hegiht = " + str(avg_height) + " ,count = " + str(counter))
 
        



                        
    

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract average bounding box sizes from JSON files in a folder and save to a CSV.')
    parser.add_argument('json_folder', help='Path to the folder containing input JSON files')
    parser.add_argument('output_csv', help='Path to the output combined CSV file')
    parser.add_argument('video_metadata_csv', help='Path to the CSV file containing video metadata (width and height)')
    parser.add_argument('--confidence_threshold', type=float, default=0.35, help='Confidence threshold (default: 0.35)')

    args = parser.parse_args()

    # Extract highest confidence midpoints and save to combined CSV
    extract_highest_confidence_midpoints_from_folder(args.json_folder, args.output_csv, args.video_metadata_csv ,args.confidence_threshold)
