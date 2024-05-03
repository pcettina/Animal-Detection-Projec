import argparse
import numpy as np
import os
import csv

def load_data(file_path):
    return np.genfromtxt(file_path, delimiter=',', names=['t', 'x', 'y'], skip_header=1)

def find_states(data, bbox_data, speed_type):
    # flag locations in the dataset where there was a prolonged non detection
    # End goal to give user access the determine where something went wrong
    avg_width, avg_height = bbox_data['average_width'], bbox_data['average_height']
    avg_box_diagonal = np.sqrt(avg_height**2 + avg_width**2)

    states = []
    prev_t, prev_x, prev_y = data[0]['t'], data[0]['x'], data[0]['y']
    first_row = True

    #Different time intervals to check for missed detections given the different speeds organisms exhibit
    time_check = 8

    if(speed_type == "fast"):
        time_check = 2
    elif(speed_type == "medium"):
        time_check = 5


    for row in data[1:]:
        t, y, x = row['t'], row['x'], row['y']
        if first_row:
            first_row = False
        elif prev_t < t - time_check:
            # Check against average size of the bounding box which could become input variable
            # Might have to ensure distance checking is working properly
            # Use euclidean distance between two points to do the check
            if np.sqrt((x-prev_x)**2 + (y-prev_y)**2) <= avg_box_diagonal:
                states.append(('still', prev_t, t))
            else:
                states.append(('missed', prev_t, t))
                
        prev_t, prev_x, prev_y = t, x, y
    return states

def process_csv(csv_folder, bbox_metadata ,output_folder):
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            # Load data from csv file
            unsorted_data = load_data(os.path.join(csv_folder, filename))
            # sort data by t 
            sorted_indices = np.argsort(unsorted_data['t'])
            # Sort the data based on the 't' column
            sorted_data = unsorted_data[sorted_indices]
            # Gather bbox data 
            bbox_data = np.genfromtxt(bbox_metadata, delimiter=',', names=['average_width', 'average_height'], skip_header=1)
            # Find states
            states = find_states(sorted_data, bbox_data)

            
            # Write to output CSV file
            output_filename = os.path.splitext(filename)[0] + '_states.csv'
            with open(os.path.join(output_folder, output_filename), mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['state', 'timestamp_start', 'timestamp_stop'])
                for state, timestamp_start, timestamp_stop in states:
                    writer.writerow([state, timestamp_start, timestamp_stop])

if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Process CSV files and output states to CSV')
    parser.add_argument('csv_folder', type=str, help='Path to the input CSV folder')
    parser.add_argument('bbox_metadata', type=str, help='Path to the avg. bounding box size')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    parser.add_argument('--speed_type', type=str, choices=['fast', 'medium', 'slow'], default='medium', help='Type of movement speed the organism in question will exhibit')

    # Parse the arguments
    args = parser.parse_args()

    # Call the process_csv function with the provided CSV folder
    process_csv(args.csv_folder, args.bbox_metadata, args.output_folder, args.speed_type)
