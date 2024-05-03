# https://chat.openai.com/share/71845f0f-ea52-47b1-b6e5-f92ab1c97715
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr

def smooth(data, window_size):
    smoothed_data = []
    half_window = window_size // 2
    data_length = len(data)

    for i in range(data_length):
        start_index = max(0, i - half_window)
        end_index = min(data_length, i + half_window + 1)
        window = data[start_index:end_index]
        smoothed_data.append(sum(window) / len(window))

    return smoothed_data

def plot_movement(csv_folder, smoothing_window=3):
    # Generate subplots
    fig, axs = plt.subplots(1,2,figsize=(15, 8))
    fig.suptitle("Detection Over Time")

    # Set common x-axis and y-axis labels for the entire chart
    fig.text(0.5, 0.04, 'Time (minutes)', ha='center', va='center', fontsize=14)
    fig.text(0.06, 0.5, 'Detection', ha='center', va='center', rotation='vertical', fontsize=14)

    for filename, ax in zip(os.listdir(csv_folder), axs.flatten()): 
        if filename.endswith('.csv'):
            # Load data from csv file
            data = np.genfromtxt(os.path.join(csv_folder,filename), delimiter=',', names=['t', 'x', 'y'], skip_header=1)

            # gather time values
            t = data['t']
            video_length = t.max()

            # Create a list of times where detections occurred
            detection_times = t.tolist()

            # Create a list of all times within the video
            all_times = list(range(int(video_length) + 1))

            # Create a list to represent the presence of detections (1) or absence (0)
            presence = [1 if t in detection_times else 0 for t in all_times]

            # Smooth the presence data
            smoothed_presence = smooth(presence, smoothing_window)

            # Convert times to minutes
            all_times_in_minutes = [t / 60 for t in all_times]

            # scatter plot
            ax.plot(all_times_in_minutes, smoothed_presence, color='blue', marker='.')

            # customize plot
            ax.set_title(filename[0:len(filename)-9])
            ax.set_xticks(range(0, int(video_length / 60) + 1, 2))
            ax.set_xticklabels(ax.get_xticks(), fontsize=7)
            ax.set_xlim(0, video_length / 60)
            ax.set_yticks([0, 1])
            ax.grid(False)
  
    # Adjust layout to prevent clipping of subplot titles
    plt.tight_layout(rect=[0.075, 0.05, 1, 0.95])

    # Show the plot
    plt.show()

if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('csv_folder', type=str, help='Path to the CSV folder')
    parser.add_argument('--smoothing_window', type=int, default=3, help='Size of the smoothing window')

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot_movement function with the provided CSV file
    plot_movement(args.csv_folder, args.smoothing_window)
