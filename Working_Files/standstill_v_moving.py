#https://chat.openai.com/share/ef1b16d3-02b0-4815-b7e6-8848304c511c

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import os

def load_data(file_path):
    return np.genfromtxt(file_path, delimiter=',', names=['t', 'x', 'y'], skip_header=1)

def plot_single_subplot(ax, data, bbox_data):
    avg_width, avg_height = bbox_data['average_width'], bbox_data['average_height']
    avg_box_diagonal = np.sqrt(avg_height**2 + avg_width**2)

    time_and_time_missed = 0
    time_and_time_still = 0
    prev_t, prev_y, prev_x = 0, 0, 0
    first_row = True
    for row in data:
        t, y, x = row['t'], row['x'], row['y']
        if first_row:
            prev_t, prev_x, prev_y = t, x, y
            first_row = False
        elif prev_t < t - 5:
            # Check if euclidean distance in five seconds between detections is greater or less than the average diagonal of a bbox
            # Apply to flag_still file
            if np.sqrt((x-prev_x)**2 + (y-prev_y)**2) <= avg_box_diagonal:
                time_and_time_still += t - prev_t
            elif np.sqrt((x-prev_x)**2 + (y-prev_y)**2) > avg_box_diagonal:
                time_and_time_missed += t - prev_t

        prev_t, prev_x, prev_y = t, x, y

    return time_and_time_missed, time_and_time_still

def plot_movement(csv_folder, bbox_metadata):
    # Generate subplots
    fig, axs = plt.subplots(2, 4, figsize=(15, 8))
    fig.suptitle("Time in States")

    # Gather bbox data 
    bbox_data = np.genfromtxt(bbox_metadata, delimiter=',', names=['average_width', 'average_height'], skip_header=1)
    


    # Iterate through files in csv_folder and the subplots
    for filename, ax in zip(os.listdir(csv_folder), axs.flatten()):
        if filename.endswith('.csv'):
            # Load data from csv file
            unsorted_data = load_data(os.path.join(csv_folder, filename))
            # sort data by t 
            sorted_indices = np.argsort(unsorted_data['t'])

            # Sort the data based on the 't' column
            data = unsorted_data[sorted_indices]
            # Process data
            time_missed, time_still = plot_single_subplot(ax, data, bbox_data)
            print(filename[0:len(filename)-9] + " total missed = " + str(time_missed) + ", total still = " + str(time_still) + ", total time = " + str(time_missed + time_still))

            # Customize the subplot
            ax.bar(["missed", "still"], [time_missed/60, time_still/60])
            ax.set_title(filename[0:len(filename)-9])

    # Set common x-axis and y-axis labels for the entire chart
    fig.text(0.5, 0.04, 'State', ha='center', va='center', fontsize=14)
    fig.text(0.06, 0.5, 'Total Time (minutes)', ha='center', va='center', rotation='vertical', fontsize=14)

    # Adjust layout to prevent clipping of subplot titles and y-axis label
    plt.tight_layout(rect=[0.075, 0.05, 1, 1])

    # Show the plot
    plt.show()

if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('csv_folder', type=str, help='Path to the CSV folder')
    parser.add_argument('bbox_metadata', type=str, help='Path to average bbox size for file')
    # Parse the arguments
    args = parser.parse_args()

    # Call the plot_movement function with the provided CSV file
    plot_movement(args.csv_folder, args.bbox_metadata)