import cv2
import numpy as np


selected_points = []
image_copy = None  

# Callback function for mouse events
def select_points(event, x, y, flags, param):
    global selected_points, image_copy  # Declare global variables

    if event == cv2.EVENT_LBUTTONDOWN:
        # Left mouse button clicked, save the coordinates
        selected_points.append((x, y))
        # Draw a circle at the clicked point
        cv2.circle(image_copy, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select ROI", image_copy)

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Right mouse button clicked, reset the selection
        selected_points = []
        image_copy = image.copy()
        cv2.imshow("Select ROI", image_copy)

# Load the image
image = cv2.imread('tests.jpg')
image_copy = image.copy()

# Create a window and set the mouse callback function
cv2.namedWindow("Select ROI")
cv2.setMouseCallback("Select ROI", select_points)

print("Instructions:")
print("1. Click the left mouse button to select four points in clockwise order to define the ROI.")
print("2. Press 'r' to reset the selection.")
print("3. Press 'c' to crop and transform the selected region.")
print("4. Press 'q' to quit.")

while True:
    cv2.imshow("Select ROI", image_copy)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        # Reset the selected points
        selected_points = []
        image_copy = image.copy()
        cv2.imshow("Select ROI", image_copy)

    elif key == ord('c') and len(selected_points) == 4:
        # Check if four points are selected
        # Define the destination points for perspective transformation (a rectangle)
        width, height = 800, 800
        dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

        # Calculate the perspective transformation matrix
        perspective_matrix = cv2.getPerspectiveTransform(np.array(selected_points, dtype=np.float32), dst_points)

        # Apply the perspective transformation
        transformed_image = cv2.warpPerspective(image, perspective_matrix, (width, height))

        # Display the transformed image
        cv2.imshow("Transformed Image", transformed_image)
        cv2.waitKey(0)

    elif key == ord('q'):
        break

cv2.destroyAllWindows()
