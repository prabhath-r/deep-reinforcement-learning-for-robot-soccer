import asyncio
import websockets
from video_streamer import VideoStreamer
from botarmy import Botarmy

class WebSocketClient_Camera:
    def __init__(self,uri):
        self.connection_Status = None
        self.uri = uri

    async def send_data(self, vs, websocket):
        while self.connection_Status == "open":
            try:
                data = vs.stream()
                # print(data.keys())
                await websocket.send(str(data))
                await asyncio.sleep(0.05)
            except websockets.ConnectionClosed:
                print("send_data WebSocket connection closed")
                self.connection_Status = "closed"
                break

            
    async def connect(self,vs):
        print(f"Camera Connecting to {self.uri}")
        async with websockets.connect(self.uri, ping_interval=None) as websocket:
            self.connection_Status = "open"
            # print("reached inside")
            await self.send_data(vs, websocket)


    # def run_client(self,vs):
    #     asyncio.run(self.connect(vs))


if __name__== "__main__":
    uri = "ws://localhost:8080"
    wsc = WebSocketClient_Camera(uri)
    vs = VideoStreamer()
    # wsc.run_client()
    asyncio.run(wsc.connect(vs))
    vs.release_cam()
    print("done and closing camera")