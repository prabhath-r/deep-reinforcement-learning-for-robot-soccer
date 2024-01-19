import asyncio
import websockets
import cv2
import numpy as np

class ImageServer:
    def __init__(self, host, port):
        self.image = None
        self.host = host
        self.port = port
        self.cv_model = None
        self.mujoco_target = [0,0]
        self.mujoco_goal1 = [-1,-4]
        self.mujoco_goal2 = [1,-4]

    async def send_image(self, websocket, path):
        while True:
            try:
                if self.image is not None:
                    self.cv_model.get_coords(self.image)
                    encoded_image = cv2.imencode('.jpg', self.image)[1].tobytes()
                    real_target = self.cv_model.transform_real_coords(self.mujoco_target[0],self.mujoco_target[1])
                    real_goal1 = self.cv_model.transform_real_coords(self.mujoco_goal1[0],self.mujoco_goal1[1])
                    real_goal2 = self.cv_model.transform_real_coords(self.mujoco_goal2[0],self.mujoco_goal2[1])
                    await websocket.send(str([encoded_image,real_target, real_goal1, real_goal2]))
                await asyncio.sleep(0.01)  # Adjust the interval as needed
            except websockets.ConnectionClosed:
                print("send_image WebSocket connection closed")
                break   

    async def run_image_server(self):
        print("Starting image server")
        async with websockets.serve(self.send_image, self.host, self.port, ping_interval=None):
            await asyncio.Future()  # run forever

