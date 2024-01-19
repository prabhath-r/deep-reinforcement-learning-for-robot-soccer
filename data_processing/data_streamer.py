from concurrent.futures import ThreadPoolExecutor
import time
import datetime        
import cv2
import pickle
from botarmy import Botarmy
from bot_controller import Bot_Controller



class DataStreamer:
    '''
    This class is used to collect the sensor data 
    from all the sphero robots along with live images 
    from the camera. The data from each robot is queried 
    simultaneously using the Sphero Apis and multithreading.'''
    def __init__(self,botarmy) -> None:
        self.botarmy = botarmy
    
    def get_sensor_data(self,droid,bot_num):
        data = {}
        data['bot'] = self.botarmy.bots[bot_num]
        data['acceleration'] = droid.get_acceleration()
        data['vertical acceleration'] = droid.get_vertical_acceleration()
        data['orientation'] = droid.get_orientation()
        data['gyroscope'] = droid.get_gyroscope()
        data['velocity'] = droid.get_velocity()
        data['location'] = droid.get_location()
        data['distance'] = droid.get_distance()
        data['speed'] = droid.get_speed()
        data['heading'] = droid.get_heading()
        if(droid.get_battery_voltage_states() == 0):
            data['battery'] = "UNKNOWN"
        elif(droid.get_battery_voltage_states() == 1):
            data['battery'] = "OK"
        elif(droid.get_battery_voltage_states() == 2):
            data['battery'] = "LOW"
        elif(droid.get_battery_voltage_states() == 3):
            data['battery'] = "CRITICAL"
        data['timestamp'] = datetime.datetime.now()
        return data


    def stream(self):
        with ThreadPoolExecutor() as executor:
            data_iterator = executor.map(self.get_sensor_data, self.botarmy.droids, self.botarmy.bots.keys())
    
        data = dict()
        for bot_data in data_iterator:
            data[bot_data['bot']] = bot_data
        return data
    


if __name__=="__main__":
    army = Botarmy()
    ds = DataStreamer(army)
    bot_controller = Bot_Controller(army.droids, army.all_toy_names)
    for i in range(3):
        print(i)
        print(ds.stream())
        time.sleep(1)
    bot_controller.stop_bots()
        
    