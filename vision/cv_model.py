import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
import os
from pathlib import Path

class CV_model:
    def __init__(self) -> None:
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        cwd = Path( __file__ ).parent.absolute()
        self.model = YOLO(f'{cwd}/foot.pt') #{0: 'football', 1: 'sphero'}
        # self.perspective_matrix = np.load('perspective_matrix.npy')
        self.frame_num = 0
        self.mujoco_x_range = [-5,5]
        self.mujoco_y_range = [-5,5]
        self.mujoco_width = self.mujoco_x_range[1]-self.mujoco_x_range[0]
        self.mujoco_height = self.mujoco_y_range[1]-self.mujoco_y_range[0]

    def get_coords(self,frame):
        # Run YOLOv8 tracking on the frame
        self.frame_num+=1
        self.frame_width = frame.shape[1]
        self.frame_height = frame.shape[0]
        # transformed_frame = cv2.warpPerspective(frame, self.perspective_matrix, (self.frame_width, self.frame_height))
        try:
            results = self.model.track(frame, conf=0.3, persist=True, tracker="botsort.yaml", device='cpu')
            classes = results[0].names
        except Exception as e:
            print("Exception in Yolo tracking: ", e)
            return {}
        coords = {}
        
        if results[0].boxes.id is None:
            return coords
        else:
            boxes = results[0].boxes.xywh.cpu()
            # track_ids = results[0].boxes.id.int().cpu().tolist()
            box_classes = results[0].boxes.cls.int().cpu().tolist()
            # get the coords in list
            for box, box_cls  in zip(boxes, box_classes):
                x, y, w, h = box
                # mid_x = x + w / 2
                # mid_y = y + h / 2
                # print(f"{self.frame_num} actual coords - [{mid_x},{mid_y}]")
                new_mid_x,new_mid_y=self.transform_mujoco_coords(x, y) # transformed x, y center point
                # print(f"{self.frame_num} transformed coords - [{new_mid_x},{new_mid_y}]")
                coords[classes[box_cls]] = [float(new_mid_x), float(new_mid_y)]
        return coords

    def transform_mujoco_coords(self,real_x,real_y):
        new_x = self.mujoco_x_range[0] + (real_x/self.frame_width)*self.mujoco_width
        new_y = self.mujoco_y_range[0] + (real_y/self.frame_height)*self.mujoco_height
        return new_x, new_y

    def transform_real_coords(self,virt_x,virt_y):
        real_x = (virt_x - self.mujoco_x_range[0])*self.frame_width//self.mujoco_width
        real_y = (virt_y - self.mujoco_y_range[0])*self.frame_height//self.mujoco_height
        return int(real_x), int(real_y)

    # Define a function to transform the coordinates
    def transform_coords(self,width, height,x,y):
        center_x = width // 2
        center_y = height // 2
        new_x = x - center_x
        new_y = center_y - y
        return new_x, new_y

if __name__=="__main__":
    video_path = 0
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    cv_model = CV_model()
    
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            cv_model.get_coords(frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cap.release()
    print("done")
            