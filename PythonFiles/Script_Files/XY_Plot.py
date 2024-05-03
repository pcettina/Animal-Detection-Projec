import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.widgets import Slider


# have to update this in order to not be affected by non turtle points
# could also be fixed by checking average box size and making sure only those boxes are
# recorded in csv
def un_dup(data):
    # gets rid of duplicates to make smoother data set
    # will have to sort either inside this function or seperate
    new_data = []
    
    data_length = len(data)
    t_step = data['t'][0]
    x_avg, y_avg = 0, 0
    count = 0
    
    for i in range(data_length):
        x_step, y_step = data['x'][i], data['y'][i]
        if (data['t'][i] == t_step):
            x_avg, y_avg = x_avg + x_step, y_avg + y_step
            count = count + 1
            
            continue
        else:
            
            # Have hit a new time step so add previous x_avg & y_avg to new data at that time step
            new_data.append((t_step, x_avg/count, y_avg/count)) 

            # Get next time step and begin new average x,y 
            t_step, x_avg, y_avg = data['t'][i], x_step, y_step
            count = 1
        
    
    data = np.array(new_data, dtype=[('t', float), ('x', float), ('y', float)])
    return data

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
        
    #removes time duplicates from data set due to detection overlap and average coordinates
    data = un_dup(data)

    # Extract x, y, and t columns
    t = data['t']
    x = data['x']
    y = data['y']

    
    
    fig, ax = plt.subplots(figsize=(10, 6))

    t_normalized = (t - t.min()) / (t.max() - t.min())
    color_gradient = clr.Normalize(vmin=0, vmax=1)(t_normalized)

    
    
    # Plot (x, y) movement with a color gradient
    scatter = ax.scatter(y, x, marker="x", c=color_gradient, cmap='viridis', s=5)
    
    ax.invert_yaxis()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Movement Plot with Color Gradient')
    ax.grid(True)
    
    # Add color bar
    cbar = plt.colorbar(scatter, ax=ax, label='Time Progression')
    
    # Slider
    ax_slider = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Time', 0, len(t) - 1, valinit=0, valstep=1)

    def update(val):
        index = int(slider.val)
        ax.set_title(f'Movement Plot with Color Gradient - Time: {t[index]/60:.2f}m {t[index]%60:.2f}s')
        scatter.set_offsets(np.column_stack((y[:index], x[:index])))
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
