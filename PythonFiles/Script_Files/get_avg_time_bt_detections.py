
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import os


def load_data(file_path):
    return np.genfromtxt(file_path, delimiter=',', names=['t', 'x', 'y'], skip_header=1)

def get_avg_time(csv_folder):
    tot_time = 0
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            # Load data from csv file
            unsorted_data = load_data(os.path.join(csv_folder, filename))
            # sort data by t 
            sorted_indices = np.argsort(unsorted_data['t'])

            # Sort the data based on the 't' column
            data = unsorted_data[sorted_indices]
            prev_t = 0
            total_bt_detections = 0
            misses = 0
            first_row = True
            for row in data:
                t = row['t']
                if first_row: #checks for first row to set prev t to not 0
                    prev_t = t
                    first_row = False
                elif prev_t < t - 0.033: #check between frames
                    total_bt_detections += t - prev_t
                    misses += 1
                prev_t = t
            tot_time += total_bt_detections/misses
            print(filename[0:len(filename)-9] + " avg. missed time = " + str(tot_time) + " misses = " + str(misses))

    print("Complete average = " + str(tot_time/4))


if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('csv_folder', type=str, help='Path to the CSV folder')

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot_movement function with the provided CSV file
    get_avg_time(args.csv_folder)