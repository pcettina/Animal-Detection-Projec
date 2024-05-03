import cv2
import pandas as pd
import argparse
import numpy as np

def add_markers_to_video(input_video_path, timestamp_csv_path, movement_csv_path, output_video_path):
    # Read input video
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read timestamp CSV
    timestamps_df = pd.read_csv(timestamp_csv_path)

    # Read movement CSV
    movement_data = pd.read_csv(movement_csv_path)

    # Convert timestamps from seconds to frames
    timestamps_df['frame_start'] = (timestamps_df['timestamp_start'] * fps).astype(int)
    timestamps_df['frame_stop'] = (timestamps_df['timestamp_stop'] * fps).astype(int)

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for MP4
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Process video and add markers
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Draw markers at timestamps
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        for _, row in timestamps_df.iterrows():
            if row['frame_start'] <= current_frame <= row['frame_stop']:
                cv2.putText(frame, row['state'], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Draw movement trajectory
        current_time = current_frame / fps  # Current time in seconds
        movement_subset = movement_data[movement_data['t'] <= current_time]
        if not movement_subset.empty:
            x = int(movement_subset['x'].iloc[-1] * height)
            y = int(movement_subset['y'].iloc[-1] * width)
            cv2.circle(frame, (y, x), 5, (0, 0, 255), -1)  # Draw a red circle at the current position
        
        # Display frame with circles (for visualization only)
        # cv2.imshow('Frame with Circles', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        
        # Write frame to output video
        out.write(frame)

    # Release video capture and writer
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Add markers to a video based on timestamps.')
    parser.add_argument('input_video', help='Path to the input video file')
    parser.add_argument('timestamp_csv', help='Path to the timestamp CSV file')
    parser.add_argument('movement_csv', help='Path to the movement CSV file')
    parser.add_argument('output_video', help='Path to save the output video file')
    args = parser.parse_args()

    # Add markers to video
    add_markers_to_video(args.input_video, args.timestamp_csv, args.movement_csv, args.output_video)

if __name__ == "__main__":
    main()
