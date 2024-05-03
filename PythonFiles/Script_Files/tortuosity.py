import argparse
import os
import csv
import numpy as np
import math

def remove_duplicates(data):
    # Remove duplicates from the dataset
    new_data = []

    for i in range(len(data)):
        if i == 0 or data[i]['t'] != data[i-1]['t']:
            new_data.append(data[i])

    return np.array(new_data, dtype=data.dtype)

def euclidean_dist(point1, point2):
    # Calculate Euclidean Distance
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calc_tortuosity(csv_file):
    # Load the CSV file into a NumPy array
    data = np.genfromtxt(csv_file, delimiter=',', names=['t', 'x', 'y'], skip_header=1)

    # Sort data by time (t)
    data.sort(order='t')

    # Remove duplicates
    data = remove_duplicates(data)

    # Extract x, y, and t columns
    t = data['t']
    x = data['x']
    y = data['y']

    total_distance = 0
    first_to_last = euclidean_dist([x[0], y[0]], [x[-1], y[-1]])

    # Gather total distance traveled
    for i in range(len(t) - 1):
        total_distance += euclidean_dist([x[i], y[i]], [x[i+1], y[i+1]])

    tortuosity = total_distance / first_to_last

    return tortuosity

def calculate_tortuosity_for_folder(input_folder, output_file):
    # Create a list to store results
    results = []

    # Iterate through all CSV files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            csv_file = os.path.join(input_folder, file_name)
            try:
                # Calculate tortuosity for the current CSV file
                tortuosity = calc_tortuosity(csv_file)
                # Append the result along with the file name to the results list
                results.append((file_name, tortuosity))
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Write the results to the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Tortuosity'])
        writer.writerows(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate tortuosity of organisms given their x,y movements stored in CSV files.')
    parser.add_argument('input_folder', help='Path to the folder containing input CSV files')
    parser.add_argument('output_file', help='Path to the output CSV file where tortuosity measurements will be saved')
    args = parser.parse_args()

    calculate_tortuosity_for_folder(args.input_folder, args.output_file)
