import cv2
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Scale
from PIL import Image, ImageTk
import argparse
import datetime

class VideoPlayerApp:
    def __init__(self, root, input_video_path, timestamp_csv_path, output_video_path):
        self.root = root
        self.input_video_path = input_video_path
        self.timestamp_csv_path = timestamp_csv_path
        self.output_video_path = output_video_path
        self.timestamps_df = pd.read_csv(timestamp_csv_path)
        self.cap = cv2.VideoCapture(input_video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.is_playing = False

        self.create_widgets()

    def create_widgets(self):
        # Create video label
        self.video_label = ttk.Label(self.root)
        self.video_label.pack()

        # Create treeview to display timestamps
        self.treeview = ttk.Treeview(self.root, columns=('timestamp_start', 'timestamp_stop', 'state'), show="headings")
        self.treeview.heading('timestamp_start', text='Start Timestamp')
        self.treeview.heading('timestamp_stop', text='Stop Timestamp')
        self.treeview.heading('state', text='State')
        self.treeview.bind('<ButtonRelease-1>', self.on_treeview_select)
        self.treeview.pack()

        # Insert data into treeview
        for index, row in self.timestamps_df.iterrows():
            self.treeview.insert('', 'end', text=str(index), values=(row['timestamp_start'], row['timestamp_stop'], row['state']))

        # Allow editing of 'state' column
        self.treeview.bind("<Double-1>", self.on_edit_state)

        # Create slider
        self.slider = Scale(self.root, from_=0, to=self.total_frames, orient=tk.HORIZONTAL, command=self.on_slider_move)
        self.slider.pack(fill=tk.X)

        # Create timestamp label
        self.timestamp_label = ttk.Label(self.root, text="00:00")
        self.timestamp_label.pack()

        # Create play button
        self.play_button = ttk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack()

    def on_treeview_select(self, event):
        selected_item = self.treeview.selection()[0]
        index = int(self.treeview.item(selected_item, 'text'))
        timestamp_start = self.timestamps_df.iloc[index]['timestamp_start']
        self.seek_to_timestamp_start(timestamp_start)

    def on_edit_state(self, event):
        item = self.treeview.selection()[0]
        column = self.treeview.identify_column(event.x)
        if column == '#3':  # State column
            cell_value = self.treeview.item(item, 'values')[2]
            entry = ttk.Combobox(self.root, values=['', 'missed', 'still'], width=10)
            entry.set(cell_value)  # Set the initial value to the current state
            entry.bind("<<ComboboxSelected>>", lambda event, item=item, entry=entry: self.update_state(item, entry))
            entry.bind("<Escape>", lambda event, entry=entry: entry.destroy())
            entry.place(relx=0, rely=0, anchor='nw')  # Place the Combobox widget at the top-left corner of the item cell
            entry.focus_set()

    def update_state(self, item, entry):
        state = entry.get()
        self.treeview.set(item, column='#3', value=state)
        entry.destroy()

        # Update DataFrame with the modified state
        index = int(self.treeview.item(item, 'text'))
        self.timestamps_df.at[index, 'state'] = state

        # Save changes back to the CSV file
        self.timestamps_df.to_csv(self.timestamp_csv_path, index=False)

    def on_slider_move(self, value):
        self.current_frame = int(value)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(value))
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img.thumbnail((800, 600))  # Resize image to fit in the window
            img = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img)
            self.video_label.image = img  # Keep reference to prevent garbage collection
            self.update_timestamp_label(int(value))

    def update_timestamp_label(self, frame_number):
        time_in_seconds = frame_number / self.fps
        time_string = str(datetime.timedelta(seconds=int(time_in_seconds)))
        self.timestamp_label.config(text=time_string)

    def play_video(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.config(text="Pause")
            self.show_frame()
        else:
            self.play_button.config(text="Play")

    def seek_to_timestamp_start(self, timestamp_start):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(timestamp_start * self.fps))

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img.thumbnail((800, 600))  # Resize image to fit in the window
            img = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img)
            self.video_label.image = img  # Keep reference to prevent garbage collection
            self.update_timestamp_label(self.current_frame)
            self.current_frame += 1
            if self.current_frame <= self.total_frames and self.is_playing:
                self.root.after(int(1000 / self.fps), self.show_frame)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Add markers to a video based on timestamps.')
    parser.add_argument('input_video', help='Path to the input video file')
    parser.add_argument('timestamp_csv', help='Path to the timestamp CSV file')
    parser.add_argument('output_video', help='Path to save the output video file')
    args = parser.parse_args()

    # Create Tkinter window
    root = tk.Tk()
    root.title("Video Player")

    app = VideoPlayerApp(root, args.input_video, args.timestamp_csv, args.output_video)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, app))

    root.mainloop()

def on_closing(root, app):
    if messagebox.askokcancel("Quit", "Do you want to save changes before quitting?"):
        # Save changes to CSV file
        app.timestamps_df.to_csv(app.output_video_path, index=False)
    root.destroy()

if __name__ == "__main__":
    main()
