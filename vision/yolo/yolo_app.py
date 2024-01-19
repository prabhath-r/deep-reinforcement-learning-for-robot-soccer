import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
import os
import time
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
model = YOLO('best2.pt')

# Open the video file
video_path = 2
cap = cv2.VideoCapture(video_path)
if cap is None:
    print("Cannot open video file")
    exit()

# Store the track history
track_history = defaultdict(lambda: [])
fps = 0
frame_count = 0
start_time = time.time()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame,conf=0.3, persist=True, tracker="botsort.yaml",device='cuda')
        frame_count += 1
        if results[0].boxes.id != None:
            # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the tracks
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 90 tracks for 90 frames
                    track.pop(0)

                # Draw the tracking lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
                print(f"Bounding box coordinates: ({x}, {y}), ({x+w}, {y+h})")

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
print(track_history)