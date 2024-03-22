#https://chat.openai.com/share/ef1b16d3-02b0-4815-b7e6-8848304c511c

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr

def plot_movement(csv_file, video_csv_file):
    fps = 30
    # Load the CSV file into a NumPy array
    data = np.genfromtxt(csv_file, delimiter=',', names=['t', 'x', 'y'], skip_header=1)
    vid_data = np.genfromtxt(video_csv_file, delimiter=',', names=['video_width', 'video_height'], skip_header=1)

    vid_height = vid_data['video_width']
    vid_width = vid_data['video_height']

    quadrants = { "Q1":0, "Q2":0, "Q3":0, "Q4":0}
    for row in data:
        y_cord, x_cord = row['x'], row['y']
        print(str(x_cord) + ", " + str(y_cord))
        if x_cord >= vid_width*0.5 and y_cord >= vid_height*0.5:
            quadrants["Q3"] +=1
        elif x_cord <= vid_width*0.5 and y_cord >= vid_height*0.5:
            quadrants["Q4"] +=1
        elif x_cord <= vid_width*0.5 and y_cord <= vid_height*0.5:
            quadrants["Q1"] +=1
        elif x_cord >= vid_width*0.5 and y_cord <= vid_height*0.5:
            quadrants["Q2"] +=1 
      

    # Calculate the time spent in each quadrant
    total_frames = sum(quadrants.values())
    print("sum= " + str(total_frames) + ", total seconds = " + str(total_frames/fps))
    print("vid_width, vid_height = " + str(vid_width) + ", " + str(vid_height))
    time_in_each_quadrant = {quadrant: count / fps for quadrant, count in quadrants.items()}

    # Create a bar chart
    quad_list = list(time_in_each_quadrant.keys())
    times = list(time_in_each_quadrant.values())

    # Customize the plot
    plt.bar(quad_list, times)
    plt.title("Time in Quadrants")
    plt.xlabel("Quadrant")
    plt.ylabel("Total Time")

    # Show the plot
    plt.show()

if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('csv_file_points', type=str, help='Path to the CSV file')
    parser.add_argument('csv_file_vidData', type=str, help='Path to the video data file')
    # Parse the arguments
    args = parser.parse_args()

    # Call the plot_movement function with the provided CSV file
    plot_movement(args.csv_file_points, args.csv_file_vidData)
