import asyncio
import websockets
from bot_controller import Bot_Controller
from data_streamer import DataStreamer
from botarmy import Botarmy

class WebSocketClient:
    def __init__(self):
        self.connection_Status = None

    async def send_data(self, ds, websocket):
        while self.connection_Status == "open":
            try:
                data = ds.stream()
                await websocket.send(str(data))
                await asyncio.sleep(1)
            except websockets.ConnectionClosed:
                print("send_data WebSocket connection closed")
                self.connection_Status = "closed"
                break


    async def receive_data(self, websocket, bot_controller):
        await websocket.send(str({'Start':bot_controller.all_bot_names}))
        while self.connection_Status == "open":
            try:
                command = await websocket.recv()
                direction, speed = eval(command)
                execution_handle = bot_controller.command_executor(direction,speed)
                if execution_handle is None:
                    self.connection_Status = "closed"
                    await websocket.send(str({'End':bot_controller.all_bot_names}))
                    break
            except websockets.ConnectionClosed:
                print("receive_data WebSocket connection closed")
                self.connection_Status = "closed"
                break
            
    async def client(self,ds,bot_controller):
        uri = "ws://localhost:8080"
        print(f"Connecting to {uri}")
        async with websockets.connect(uri, ping_interval=None) as websocket:
            self.connection_Status = "open"
            send_task = asyncio.create_task(self.send_data(ds, websocket))
            receive_task = asyncio.create_task(self.receive_data(websocket, bot_controller))
            
            await asyncio.gather(send_task, receive_task)


    def run_client(self, ds, bot_controller):
        asyncio.run(self.client(ds, bot_controller))


if __name__== "__main__":
    army = Botarmy()
    ds = DataStreamer(army)
    bot_controller = Bot_Controller(army.droids,army.all_toy_names)
    wsc = WebSocketClient()
    wsc.run_client(ds,bot_controller)
    bot_controller.stop_bots()
    print("done and closing")