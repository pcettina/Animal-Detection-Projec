from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import csv
import sys

class VideoPlayerApp(App):
    def build(self):
        # Create a test layout
        layout = BoxLayout(orientation='vertical')

        # Get CSV file path from command-line arguments
        if len(sys.argv) < 2:
            print("Usage: python3 video_player.py <csv_file_path>")
            return layout
        csv_file_path = sys.argv[1]

        # Create labels from CSV data
        csv_labels = self.create_csv_labels(csv_file_path)
        for label in csv_labels:
            layout.add_widget(label)

        return layout

    def create_csv_labels(self, csv_file_path):
        labels = []

        # Load CSV data
        try:
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    start_timestamp = float(row[1])  # Assuming start timestamp is in the second column
                    label = Label(text=f"Start: {start_timestamp:.2f}s")
                    label.bind(on_touch_down=self.on_label_touch)
                    labels.append(label)
        except FileNotFoundError:
            print("CSV file not found.")
        
        return labels

    def on_label_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print("Label clicked")
            print("Touch:", touch)
            print("Instance:", instance)

if __name__ == '__main__':
    VideoPlayerApp().run()
