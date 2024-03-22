from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import csv
import sys

class VideoPlayerApp(App):
    def build(self):
        # Get input video path and CSV file path from command-line arguments
        if len(sys.argv) < 3:
            print("Usage: python3 video_player.py <input_video_path> <timestamp_csv_path>")
            return
        input_video_path = sys.argv[1]
        timestamp_csv_path = sys.argv[2]

        # Create the main layout
        layout = BoxLayout(orientation='horizontal')

        # Create the video player
        self.video = VideoPlayer(source=input_video_path, state='play')
        layout.add_widget(self.video)

        # Create a button to open the CSV window
        button = Button(text='Open CSV', on_press=self.open_csv_window)
        layout.add_widget(button)

        return layout

    def open_csv_window(self, instance):
        # Create a new window for displaying the CSV file
        csv_window = BoxLayout(orientation='vertical')
        

        # Load the CSV file and populate the Label with its contents, skipping the header row
        with open(sys.argv[2], newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                start_timestamp = float(row[1])  # Start timestamp (assuming it's in the second column)
                end_timestamp = float(row[2])    # End timestamp (assuming it's in the third column)
                state = row[0]                   # State (assuming it's in the first column)
                row_label = Label(text=f'{state}: {start_timestamp:.2f}s - {end_timestamp:.2f}s')
                row_label.bind(on_touch_down=self.seek_to_timestamp)
                row_label.timestamp = start_timestamp
                csv_window.add_widget(row_label)

        # Add the CSV window to the app
        self.csv_popup = Popup(title='Timestamps', content=csv_window, size_hint=(None, None), size=(800, 800))
        self.csv_popup.open()

    def seek_to_timestamp(self, instance, touch):
        if instance.collide_point(*touch.pos) and not touch.is_double_tap:
            # Extract the start timestamp stored as an attribute of the clicked label and seek the video player to that timestamp
            timestamp = instance.timestamp
            self.video.seek(timestamp)

if __name__ == '__main__':
    VideoPlayerApp().run()
