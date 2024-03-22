#https://chat.openai.com/share/ee71e5e7-5f4c-4f61-ae09-d3f59ccf7b15
import os
import json
import csv
import argparse
from concurrent.futures import ThreadPoolExecutor

def calculate_midpoint(bbox):
    xmin, ymin, width, height = bbox
    midpoint_x = (xmin + width*0.5)
    midpoint_y = (ymin + height*0.5)
    return [midpoint_x, midpoint_y]

def process_file(file_path, video_width, video_height, conf_threshold, frames_per_second):
    with open(file_path, 'r') as f:
        data = json.load(f)['images']

    frame_number = 0
    results = []

    # Determine adjustments based on the filename
    filename = os.path.basename(file_path)
    adjust_midpoint_based_on_filename = get_adjust_midpoint_function(filename)

    for frame_data in data:
        frame_number += 1
        detections = frame_data['detections']

        highest_confidence_detection = None
        highest_confidence = 0.0

        for detection in detections:
            confidence = detection['conf']

            if detection.get('category') == '1' and confidence > conf_threshold and confidence > highest_confidence:
                highest_confidence = confidence
                highest_confidence_detection = detection

        if highest_confidence_detection is not None:
            bounding_box = highest_confidence_detection['bbox']
            midpoint = calculate_midpoint(bounding_box)

            # Apply adjustments based on the filename
            adjust_midpoint_based_on_filename(midpoint, video_width, video_height)

            # Increment time based on the assumption of 30 frames per second
            time_in_seconds = frame_number / frames_per_second

            results.append({'t': time_in_seconds, 'x': midpoint[1], 'y': midpoint[0]})

    return results

def get_adjust_midpoint_function(filename):
    if 'right' in filename:
        return adjust_midpoint_for_right
    elif 'left' in filename:
        return adjust_midpoint_for_left
    elif 'foreground' in filename:
        return adjust_midpoint_for_foreground
    else:
        return adjust_midpoint_default

def adjust_midpoint_for_right(midpoint, video_width, video_height):
    midpoint[0] += 1
    midpoint[0] *= (video_width*0.5) 
    midpoint[1] *= 0.4
    midpoint[1] *= (video_height)

def adjust_midpoint_for_left(midpoint, video_width, video_height):
    midpoint[0] *= (video_width*0.5)
    midpoint[1] *= 0.4
    midpoint[1] *= (video_height)

def adjust_midpoint_for_foreground(midpoint, video_width, video_height):
    midpoint[0] *= (video_width)
    #midpoint[1] *= (0.6)
    
    midpoint[1] *= 0.6 
    midpoint[1] *= (video_height)
    midpoint[1] += (video_height*0.4)

def adjust_midpoint_default(midpoint, video_width, video_height):
    # No adjustments needed for other filenames
    pass

def extract_highest_confidence_midpoints_from_folder(json_folder, output_csv, conf_threshold, video_metadata_csv, frames_per_second=30):
    # Load video metadata from the provided CSV
    with open(video_metadata_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_width = int(row['video_width'])
            video_height = int(row['video_height'])
            break  # Assuming there is only one row in the CSV for a single video

    results = []

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor() as executor:
        for filename in os.listdir(json_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(json_folder, filename)
                results.extend(executor.submit(process_file, file_path, video_width, video_height, conf_threshold, frames_per_second).result())

    # Write results to the output CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['t', 'x', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

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
