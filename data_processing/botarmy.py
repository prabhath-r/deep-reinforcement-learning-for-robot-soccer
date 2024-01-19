import edge
from spherov2.scanner import *
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


class Botarmy:
    '''
    This class serves as a wrapper to make 
    connections with all the sphero bots. It
    contains some attributes that have 
    information regarding the bots connected.
    '''
    def __init__(self) -> None:
        self.SCRIPT_DIR = Path( __file__ ).parent.absolute()
        self.config = {}
        self.read_config()
        self.all_toy_names = []
        self.get_toy_names()
        self.droids = set()
        self.bots = dict()
        self.toys = []
        self.connect_all_toys()


    def read_config(self):
        '''
        The config file and the script should 
        be in the same directory getting the 
        directory where the script is located
        '''
        try : 
            # Reading the config file
            with open(f"{self.SCRIPT_DIR}/config.yml", "r") as ymlfile:
                self.config = yaml.safe_load(ymlfile)
        except(FileNotFoundError):
            print(f"File does not exist : {str(FileNotFoundError)}")
            exit()
    

    def get_toy_names(self):
        try :
            self.all_toy_names = self.config['toys']
        except(KeyError):
            print(f"Key does not exist : {str(KeyError)}")
            exit() 

        
    def connect_all_toys(self):
        print("Connecting to Bolt...")
        self.toys = find_toys(toy_names=self.all_toy_names, toy_types=[BOLT]) #find toys is a spherov2 api function
        print("toys",self.toys)
        # connecting to all the toys at once using multithreading.  The output is an iterator [SpheroEduApi object, toy_name] consisting of all the droids
        with ThreadPoolExecutor() as executor:
            sphero_iterator = executor.map(edge.connect_to_bolt, self.toys)
        
        for each in sphero_iterator:
            self.droids.add(each[0])
            self.bots[len(self.droids)-1] = each[1]
        print("Connection Completed")