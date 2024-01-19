import cv2
import asyncio
import websockets
import numpy as np

class ImageClient:
    def __init__(self, host, port) -> None:
        self.uri = f"ws://{host}:{port}"
        self.image_server_connection_status = None

    async def handler(self):
        print(f"Connecting to {self.uri}")
        async with websockets.connect(self.uri, ping_interval=None) as websocket:
            self.image_server_connection_status = "open"
            image_display = asyncio.create_task(self.display_image(websocket))
            await asyncio.gather(image_display)

    async def display_image(self,websocket):
        # async with websockets.connect() as websocket:
        print("reached display image", self.image_server_connection_status)
        while self.image_server_connection_status=="open":
            try:
                data = await websocket.recv()
                image_data, target, goal1, goal2 = eval(data)
                # print("target", target, type(target))
                # print(image_data)
                if image_data == []:
                    # print("image data", image_data)
                    self.image_server_connection_status = "closed"
                    break
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # Draw the marker.
                cv2.drawMarker(image, position=target, color=(0,0,255), thickness=10)
                cv2.drawMarker(image, position=goal1, color=(0,255,255), thickness=10)
                cv2.drawMarker(image, position=goal2, color=(0,255,255), thickness=10)
                cv2.imshow("Received Image", image)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    cv2.destroyAllWindows
                    break
            except websockets.ConnectionClosed:
                print("display_image WebSocket connection closed")
                self.image_server_connection_status = "closed"
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image_server_host = "localhost"  # Change to the actual host where the image server is running
    image_server_port = 8081  # Change to the port where the image server is running
    image_client = ImageClient(image_server_host, image_server_port)
    asyncio.run(image_client.handler())
