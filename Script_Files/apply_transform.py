import numpy as np
import csv
import argparse

def estimate_transformation(radius, data_points, ellipse_axes_data):
    # Extract data from arrays
    r_original = float(radius)  # Radius of original circle

    
    # Load the CSV file into a NumPy array
    data = np.genfromtxt(data_points, delimiter=',', names=['t', 'x', 'y'], skip_header=1)
    ellipse_data = np.genfromtxt(ellipse_axes_data, delimiter=',', names=['Metric', 'x', 'y'], skip_header=1)
    
    # Sort data by time (t)
    data.sort(order='t')
        
    #removes time duplicates from data set due to detection overlap and average coordinates
    # data = un_dup(data)

    # Extract x, y, and t columns
    t = data['t']
    x, y = data['x'], data['y']
    print(str(x[0:10]) + ', ' + str(y[0:10]))

    a, b = ellipse_data['x'], ellipse_data['y']  # Major and minor axes lengths of the ellipse
    print(str(a[1]) + " " + str(b[1]))
    width = a[1]
    height = b[1]


    # Estimate the transformation
    aspect_ratio = width / height
    print("aspect ration = " + str(aspect_ratio))
    scale_factor_major = r_original / width
    scale_factor_minor = r_original / height
    avg_scale_factor = (scale_factor_major + scale_factor_minor) / 2
    transformation_matrix = np.array([[avg_scale_factor, 0], [0, avg_scale_factor]])

    # Apply the transformation to all data points
    transformed_xy = np.dot(transformation_matrix, [x, y])

    # Transpose back to have x and y as columns
    transformed_data_points = np.vstack((transformed_xy[0], transformed_xy[1])).T

    return [t, transformed_data_points[:, 0], transformed_data_points[:, 1]]

def save_to_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['t', 'x', 'y'])  # Write header
        for i in range(len(data[0])):
            writer.writerow([data[0][i], data[1][i], data[2][i]])  # Write data row by row

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply transform due to video being shot at an angle')
    parser.add_argument('radius', type=int, help='radius of ellipse')
    parser.add_argument('data_csv', type=str,help='Path to the movement data CSV file')
    parser.add_argument('ellipse_csv', type=str, help='Path to the CSV file containing ellipse metadata (center & width and height)')
    parser.add_argument('output_csv', type=str, help='Path to the transformed csv file')
    
    args = parser.parse_args()

    transformed_data_points = estimate_transformation(args.radius, args.data_csv, args.ellipse_csv)
    save_to_csv(args.output_csv, transformed_data_points)
