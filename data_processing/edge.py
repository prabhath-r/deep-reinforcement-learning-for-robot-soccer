#for spherov2 api reference visit: https://spherov2.readthedocs.io/en/latest/sphero_edu.html

from enum import IntEnum
import time
from spherov2.scanner import *
from spherov2.sphero_edu import EventType, SpheroEduAPI
from spherov2.types import Color
from spherov2.toy.bolt import BOLT
import asyncio
from multiprocessing import Process
import threading
import json


class BatteryVoltageStates(IntEnum):  
    '''Battery voltage states.'''

    UNKNOWN = 0
    OK = 1
    LOW = 2
    CRITICAL = 3

def get_all_data(droid):
    '''Get all data from the droid.'''

    data = {}
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
    return data
    
    
def connect_to_bolt(toy):
    '''Connect to the bolt toy.'''

    try:
        print(toy.name + ' powering on!')
        droid = SpheroEduAPI(toy)
        loc = [0.00, 0.00]
        action = "up"
        droid.set_main_led(Color(r=0, g=255, b=0))
        # droids.append(droid)
        bot = toy.name
        
        droid.set_main_led(Color(r=0, g=0, b=255))  # Sets whole Matrix
        print(toy.name + " connected!")
        return droid,bot

    except Exception as e:
        print('Connection failed with ' + toy.name)
        print("error :" + str(e))
        print('Reconnecting to ' + toy.name)
        toys = find_toys(toy_names=[toy.name], toy_types=[BOLT])
        return connect_to_bolt(toys[0])
    
    

def run_in_square(droid): 
    '''Run in a square.'''

    droid.roll(0,80,0.25)
    time.sleep(2)
    droid.roll(90,80,0.25)
    time.sleep(2)
    droid.roll(180,80,0.25)
    time.sleep(2)
    droid.roll(270,80,0.25)
    time.sleep(2)

def run_zigzag(droid):
    '''Run in a zigzag.'''

    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(30,80,0.25)
    time.sleep(0.3)
    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(-30,80,0.25)
    time.sleep(0.3)
    droid.roll(0,80,0.25)
    time.sleep(0.3)
    droid.roll(30,80,0.25)
    time.sleep(0.3)
    droid.roll(-30,80,0.25)

def run_circle(droid):
    i = 0
    while i<360:
        droid.roll(i,80,0.25) 
        time.sleep(0.3)
        i+=40
    return

def ir_follow(droids):
    '''IR follow.'''

    broadcaster = droids[0]
    broadcaster.start_ir_broadcast(0, 1)
    broadcaster.set_main_led(Color(r=255, g=0, b=0))
    for droid in droids:
        if droid != broadcaster:
            droid.start_ir_follow(0, 1)

    # run_zigzag(broadcaster) 
    broadcaster.roll(0,80,0.25)    
    time.sleep(5)  
    broadcaster.stop_roll(0) 
    stop_ir_follow(droids)

def stop_ir_follow(droids):
    '''Stop IR follow.'''

    broadcaster = droids[0]
    broadcaster.stop_ir_broadcast()
    broadcaster.set_main_led(Color(r=0, g=0, b=255))
    for droid in droids:
        if droid != broadcaster:
            droid.stop_ir_follow()

def stop_sphero(droid):
    droid.stop_roll(0)
    droid.__exit__(None, None, None)
    return        
    

def predefined_policy(droids,droid,n):
    '''Run a predefined policy.'''

    if n==1:
        run_in_square(droid)
    elif n==2:
        run_zigzag(droid)   
    elif n==3:
        ir_follow(droids)
    
def main():
   

    global droids, bots, data

    print("Testing Starting...")
    print("Connecting to Bolt...")
    toys = find_toys(toy_names=['SB-C54E','SB-1C88', 'SB-B5BA', 'SB-3D46', 'SB-EE23'], toy_types=[BOLT]) #find toys is a spherov2 api function
    print("toys",toys)
    droids = []
    bots = {}
    for toy in toys:
        print("toy: " + toy.name) 

        connect_to_bolt(toy, droids,bots)
    
    print("bots",bots)
    return droids


if __name__ == "__main__":
    '''Main function.'''

    main()

    processs = []
    data = {}

    for bot in bots:
        data[bots[bot]] = []
    
    
    while True:
        num = int(input("Enter a custom policy number: (1) Square (2) Zigzag (3) IR Follow (10) Exit:"))
        if (num == 10):
            for droid in droids:
                droid.stop_roll(0)
                droid.__exit__(None, None, None)
            break
        else:
           
            for droid in droids:
                predefined_policy(droids,droid,num)
                droid.stop_roll(0)
                data[bots[droids.index(droid)]].append(get_all_data(droid))