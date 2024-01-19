import asyncio
import websockets
import datetime
import cv2
import pickle
from image_server import ImageServer
from RL.send_command import find_action_and_create_policy
from RL.utility import helper
from Computer_Vision.cv_model import CV_model

class WebSocketServer:
    def __init__(self):
        self.img = None
        self.cv_model = CV_model()
        self.image_server = ImageServer('localhost', 8081)
        self.image_server.cv_model = self.cv_model
        self.RLModel=find_action_and_create_policy()
        self.helper_obj=helper()
        self.connected_users = {}
        self.user_count = 0


    def get_command(self):
        if self.img is not None and self.user_count>0:
            coords = self.cv_model.get_coords(self.img)
            if coords:
                if 'football' in coords.keys():
                    self.image_server.mujoco_target = self.helper_obj.agents_point([-1,-4], [1,-4], coords["football"], 0.5 )
                if len(coords.keys())==2:
                    print("coords received at server, ",coords)
                    state, reached = self.RLModel.get_state(coords['sphero'], self.image_server.mujoco_target, coords['football'])
                    print(reached)
                    if reached:
                        print("Hitting ball")
                        direction = self.RLModel.hit_ball(state)
                        return [direction, 40]
                    direction=self.RLModel.fixed_action(state)
                    print("direction", direction)
                    return [direction, 20]
                else:
                    print("Both objects not detected")
                    return -1
            print("No detections from CV model")
            return -1
        print("Waiting for camera and robots to connect")
        return -1



    async def receive_data(self, websocket):
        while True:
            try:
                x = await websocket.recv()
                x = eval(x)
          
                if 'image' in x.keys():
                    frame = pickle.loads(x['image'])
                    self.img = cv2.imdecode(frame,cv2.IMREAD_COLOR)
                    self.image_server.image = self.img
                else:
                    if 'Start' in x.keys():
                        self.user_count+=1
                        self.connected_users[''.join(x['Start'])] = x['Start']
                        print(f"New user added at {datetime.datetime.now()}, ",x['Start'])
                    elif 'End' in x.keys():
                        print(f"User disconnected at {datetime.datetime.now()}, ",x['End'])
                        self.user_count-=1
                        del self.connected_users[''.join(x['End'])]
                    else:
                        #handle sensor data
                        pass

                # cv2.imshow('Img Server',data)
            except websockets.ConnectionClosed:
                # self.image_server.image = "stopped streaming"
                print("WebSocket connection closed: Exception in Receive data function")
                break

    async def send_command(self, websocket):
        while True:
            try:    
                command = await asyncio.to_thread(self.get_command)
                if type(command)==list:
                    await websocket.send(str(command))
                await asyncio.sleep(1)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed: Exception in send command function")
                break   

    async def handler(self, websocket):
        recv_task = asyncio.create_task(self.receive_data(websocket))
        send_task = asyncio.create_task(self.send_command(websocket))
        await asyncio.gather(recv_task, send_task)


    async def run_server(self):
        print("Starting main server")
        async with websockets.serve(self.handler, "localhost", 8080, ping_interval=None):
            await asyncio.Future()  # run forever

    async def run_servers(self):
        await asyncio.gather(self.run_server(), self.image_server.run_image_server())


if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.run_servers())
