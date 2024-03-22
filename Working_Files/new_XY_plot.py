import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.widgets import Slider

def plot_movement(csv_file, video_metadata_csv):
    with open(video_metadata_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_width = int(row['video_width'])
            video_height = int(row['video_height'])
            break  # Assuming there is only one row in the CSV for a single video
    
    # Load the CSV file into a NumPy array
    data = np.genfromtxt(csv_file, delimiter=',', names=['t', 'x', 'y'], skip_header=1)
    
    # Sort data by time (t)
    data.sort(order='t')

    # Extract x, y, and t columns
    t = data['t']
    x = data['x']
    y = data['y']
    
    avg_x = []
    avg_y = []
    avg_t = []
    
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(t)):
        if i%10 == 0:
            print(str(np.average(x[i-10:i])) + " " + str(np.average(y[i-10:i])) + " " + str(np.average(t[i-10:i])))
            avg_x.append(np.average(x[i-10:i]))
            avg_y.append(np.average(y[i-10:i]))
            avg_t.append(np.average(t[i-10:i]))
        elif i >= len(t):
            avg_x.append(np.average(x[i-10:i]))
            avg_y.append(np.average(y[i-10:i]))
            avg_t.append(np.average(t[i-10:i]))
        elif i == 0:
            avg_x.append(x[i])
            avg_y.append(y[i])
            avg_t.append(t[i])
        

    t_normalized = (avg_t - avg_t[0]) / (avg_t[len(avg_t)-1] - avg_t[0])
    color_gradient = clr.Normalize(vmin=0, vmax=1)(t_normalized)
    
    # Plot (x, y) movement with a color gradient
    scatter = ax.scatter(avg_y, avg_x, marker="x", c=color_gradient, cmap='viridis', s=5)
    
    ax.invert_yaxis()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Movement Plot with Color Gradient')
    ax.grid(True)
    
    # Add color bar
    cbar = plt.colorbar(scatter, ax=ax, label='Time Progression')
    
    # Slider
    ax_slider = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Time', 0, len(avg_t) - 1, valinit=0, valstep=1)

    def update(val):
        index = int(slider.val)
        ax.set_title(f'Movement Plot with Color Gradient - Time: {avg_t[index]:.2f}')
        scatter.set_offsets(np.column_stack((avg_y[:index], avg_x[:index])))
        scatter.set_array(color_gradient[:index])
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()

if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Plot (x, y) movement from a CSV file')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('video_info', type=str, help='Path to the CSV file')
    # Parse the arguments
    args = parser.parse_args()

    # Call the plot_movement function with the provided CSV file
    plot_movement(args.csv_file, args.video_info)
