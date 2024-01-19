import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
import os
import time
import torch


## check device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using {device} device')

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# model = YOLO('best2.pt')
model= YOLO('foot.pt') #{0: 'football', 1: 'sphero'}
# perspective_matrix = np.load('perspective_matrix.npy')
# Open the video file
video_path = 0


cap = cv2.VideoCapture(video_path)
# def make_square():
#     cap.set(3, 500)
#     cap.set(4, 500)

width = int(cap.get(3))
height = int(cap.get(4))



print("The webcam resolution is {}x{}".format(width, height))
if cap is None:
    print("Cannot open video file")
    exit()

# Define a function to transform the coordinates
def transform_coords(width, height,x,y):
    center_x = width // 2
    center_y = height // 2
    new_x = x - center_x
    new_y = center_y - y
    return new_x, new_y


# Store the track history
track_history = defaultdict(lambda: [])
fps = 0
frame_count = 0
start_time = time.time()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    resize=(640,640)
    frame = cv2.resize(frame, resize)

    if success:
        # Run YOLOv8 tracking on the frame
        # transformed_frame = cv2.warpPerspective(frame, perspective_matrix, resize)
        # transformed_frame = cv2.warpPerspective(frame, perspective_matrix, (frame.shape[1], frame.shape[0]))
        results = model.track(frame, conf=0.3, persist=True, tracker="botsort.yaml", device=device, )
        frame_count += 1
        print("results names :",results[0].names)
        # Even if there are no detections, visualize the frame
        annotated_frame = frame.copy()

        if results[0].boxes.id is not None:
            # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            print("boxes",boxes)
            print("class", results[0].boxes.cls.int().cpu().tolist())
            print("track_id",track_ids)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the tracks
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                mid_x = x + w / 2
                mid_y = y + h / 2
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 90 tracks for 90 frames
                    track.pop(0)

                # Draw the tracking lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
                print(f"Bounding box coordinates: ({x}, {y}), ({x + w}, {y + h})")
                # print(f"Mid points of bounding box: ({mid_x}, {mid_y})")
                # newx,newy=transform_coords(width, height, x, y)
                # print(f'transformed coordinates: ({newx}, {newy})')


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
# print(track_history)
