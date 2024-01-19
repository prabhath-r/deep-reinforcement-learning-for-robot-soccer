import edge
from concurrent.futures import ThreadPoolExecutor
from botarmy import Botarmy
from spherov2.sphero_edu import SpheroEduAPI
import time
import numpy as np

class Bot_Controller:
    '''
    This class serves the purpose to translate the 
    commands from the server side (either directly 
    given by a user or using some ML/RL algorithm)
    to the sphero robots on the client/edge side.
    '''

    def __init__(self,droids, droid_names) -> None:
        self.angle = 0
        self.speed = 15
        self.duration = 0.5
        self.droids = droids
        self.angle_map = {}
        for droid in droids:
            self.angle_map[droid]=0
        self.all_bot_names = droid_names
        self.angle_mapping = {
            '0': -45,    
            '1': 0,         # Right
            '2': 45,     # Down
            '3': 90,     # Left
            '4': 135,   # Up-Left
            '5': 180,       # Up-Right
            '6': -135,  # Down-Left
            '7': -90       # Down-Right
        }



    def execute_command(self):
        print("Executing square command")
        with ThreadPoolExecutor() as executor:
            executor.map(edge.run_zigzag, self.droids)


    def stop_bots(self):
        print("Executing stop command")
        with ThreadPoolExecutor() as executor:
            executor.map(edge.stop_sphero, self.droids)

    def stop_roll(self):
        print("Executing stop roll")
        with ThreadPoolExecutor() as executor:
            executor.map(SpheroEduAPI.stop_roll, self.droids)

    def start_roll(self,droid):
        droid.roll(self.angle,self.speed,self.duration)
        time.sleep(1)     
        droid.stop_roll()

    def move_bots(self,droid):
        print(self.angle_map[droid],self.speed,self.duration)
        droid.roll(self.angle_map[droid],self.speed,self.duration)
        time.sleep(1)     
        droid.stop_roll()


    def run_loop(self,):
        print("enter number of loops")
        num_loops =  int(input())
        i = 0
        while i<num_loops:
            i+=1
            with ThreadPoolExecutor() as executor:
                executor.map(edge.run_circle, self.droids)
        self.stop_roll()
    
    def command_executor(self,command, speed):
        # Check if the command is in the mapping
        # if command in self.angle_mapping:
        #     self.angle = self.angle_mapping[command]
        #     print(self.angle)
        # angle = 90
        # for each in self.droids:
        #     self.angle_map[each] = angle
        #     angle=int((angle+90)%360)
        # with ThreadPoolExecutor() as executor:
        #     executor.map(self.move_bots, self.droids)
        if command and speed:
            self.angle = int(command)
            self.speed = int(speed)
        else:
            self.duration = 0
            self.speed = 0
            return None

        with ThreadPoolExecutor() as executor:
            executor.map(self.start_roll, self.droids)

        return "OK"



if __name__=="__main__":
    army = Botarmy()
    bot_controller = Bot_Controller(army.droids,army.all_toy_names)
    bot_controller.command_executor()
    bot_controller.stop_bots()
    print("done with loop")