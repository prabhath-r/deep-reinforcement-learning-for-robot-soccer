# Data Processing

Files deployed on cloud/server side
1. server.py
2. image_server.py
3. image_client.py

Files deployed on edge side
1. botarmy.py
2. bot_controller.py
3. client.py
4. data_streamer.py
5. edge.py

Steps to run server-client model
1. Run server.py on one terminal. This will start a websocket server on localhost port 8080 to get data from the robots(edge). It also starts an image server which is used to stream the images obtained from edge side to other clients who want to remotely control the robots seeing their images. 
2. Run client.py inside another terminal. This will create a websocket client that connects to ther server localhost 8080 port and transfer the data from the edge side. 
3. Run image_client.py on another terminal. On running this we can view the images transmitted to the server side. 
4. To control the robots from the server side, we can use the keys 'w', 'a', 's' and 'd' as arrow keys. If we enter any other keys in the server terminal, its connection with the client will stop and the client.py execution ends