import cv2
import numpy as np

# Global variables to store the selected points and the perspective transformation matrix
selected_points = []
perspective_matrix = None
test=False
# Callback function for mouse events
def select_points(event, x, y, flags, param):
    global selected_points, perspective_matrix, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(selected_points) < 4:
            # Left mouse button clicked, save the coordinates
            selected_points.append((x, y))
            # Draw a circle at the clicked point
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            if len(selected_points) == 4:
                # Define the destination points for perspective transformation (a rectangle)
                width, height = frame.shape[1], frame.shape[0]
                dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

                # Calculate the perspective transformation matrix
                perspective_matrix = cv2.getPerspectiveTransform(np.array(selected_points, dtype=np.float32), dst_points)

        else:
            # If four points are already selected, reset the selection
            selected_points = []
            frame_copy = frame.copy()
            cv2.imshow("Select Points", frame_copy)

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Right mouse button clicked, reset the selection
        selected_points = []
        frame_copy = frame.copy()
        cv2.imshow("Select Points", frame_copy)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a window and set the mouse callback function
cv2.namedWindow("Select Points")
cv2.setMouseCallback("Select Points", select_points)

print("Instructions:")
print("1. Click four points on the video to define the edges of a rectangle.")
print("2. Once four points are selected, the perspective transformation will be applied.")
print("3. Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if perspective_matrix is not None:
        # Apply the perspective transformation to the frame
        transformed_frame = cv2.warpPerspective(frame, perspective_matrix, (frame.shape[1], frame.shape[0]))
        
        cv2.imshow("Transformed Stream", transformed_frame)
        print(transformed_frame.shape)

    frame_copy = frame.copy()

    if len(selected_points) == 2:
        # Draw a line between the two selected points
        cv2.line(frame_copy, selected_points[0], selected_points[1], (0, 0, 255), 2)

    elif len(selected_points) == 3:
        # Draw a line between the third point and the previous point
        cv2.line(frame_copy, selected_points[0], selected_points[1], (0, 0, 255), 2)
        cv2.line(frame_copy, selected_points[1], selected_points[2], (0, 0, 255), 2)

    elif len(selected_points) == 4:
        # Draw lines connecting all four selected points to form a rectangle
        cv2.line(frame_copy, selected_points[0], selected_points[1], (0, 0, 255), 2)
        cv2.line(frame_copy, selected_points[1], selected_points[2], (0, 0, 255), 2)
        cv2.line(frame_copy, selected_points[2], selected_points[3], (0, 0, 255), 2)
        cv2.line(frame_copy, selected_points[3], selected_points[0], (0, 0, 255), 2)
    # display the below only if the transformation is not working
    if test==False:
        cv2.imshow("Select Points", frame_copy)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


print(perspective_matrix)
#save perspective matrix to a file
np.save('perspective_matrix.npy', perspective_matrix)
# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

import numpy as np
## load the perspective matrix from the file
perspective_matrix = np.load('perspective_matrix.npy')

print(perspective_matrix)