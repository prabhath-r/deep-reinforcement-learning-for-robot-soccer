# Yolo APP 
 # Updates (Latest to oldest): 
 
4) MultiSphero </br>
 ![screenshot](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/multi.png?raw=true)

3) Nvidia Dockerfile
   > **_NOTE:_**  Make sure nvidia runtime is installed, instructions [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).   
 ```console
docker build -t yoloapp .
```
```console
docker run --rm --runtime=nvidia --gpus all -it -v $PWD:/app/ --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY yoloapp
```

2) DockerFile has been added to the repo </br>
> **_NOTE:_**  CUDA docker image is available in gpu folder
 * Run the below commands to build and run the docker image
```console
docker build -t yoloapp .
```
```console
docker run -it -v $PWD:/app/ --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY yoloapp
```

 1) Football have been added to dataset </br>
 ![screenshot](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/footballsphero.png?raw=true)

 # Steps to run the program
 1) Run the webcamtransformation.py program </br>

![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/before.png?raw=true)

2) Select the points in clockwise direction to select the Region of Interest </br>
![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/during.png?raw=true)

3) We will get the transformed image </br>
![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/transformed.png?raw=true)

4) The coordinates information is stored in an .npy file </br>
![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/npyfile.png?raw=true)
5) Load the transformation file into yolo_transformed.py </br>

6) before the transformation yolo  </br>
![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/yolo%20before.png?raw=true)
7) after the transformation yolo </br>
![alt text](https://github.com/CMPE-295-CYPHAI/Integration/blob/main/yolo/images/yolo%20after.png?raw=true)
