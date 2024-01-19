import cv2
import pickle



class VideoStreamer:
    '''
    This class is used to collect the sensor data 
    from all the sphero robots along with live images 
    from the camera. The data from each robot is queried 
    simultaneously using the Sphero Apis and multithreading.'''
    def __init__(self) -> None:
        self.cam = None
        self.start_camera()


    def start_camera(self):
        '''Starts the camera object'''
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3,700)
        self.cam.set(4,700)
    

    def release_cam(self):
        self.cam.release()
        cv2.destroyAllWindows()


    def stream(self):
        data = dict()
        _, img = self.cam.read()
        _, buffer = cv2.imencode(".jpg",img,[int(cv2.IMWRITE_JPEG_QUALITY),30])
        x_as_bytes = pickle.dumps(buffer)
        data['image'] = x_as_bytes
        return data
    


if __name__=="__main__":
    vs = VideoStreamer()
    data = vs.stream()
    print(type(data),type(data['image']))
    vs.release_cam()
   
        
    