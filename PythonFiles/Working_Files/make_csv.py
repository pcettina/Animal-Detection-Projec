import csv


def make_csv_file():
    output_csv = "video_info_3_5.csv"
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['video_height', 'video_width']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow({'video_height': 1080, 'video_width': 1920})

if __name__ == "__main__":
    make_csv_file()