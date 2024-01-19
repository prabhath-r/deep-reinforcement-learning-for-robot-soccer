import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from RL.utility import helper
from pathlib import Path
import math

class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)
    

class find_action_and_create_policy():
    def __init__(self):
        cwd = Path( __file__ ).parent.absolute()
        self.n_actions = 8
        self.n_observations=4
        self.policy_net = DQN(self.n_observations, self.n_actions).to("cpu")
        self.policy_net.load_state_dict(torch.load(f"{cwd}/dqn_model.pth"))
        
    def find_action(self, state):
       action = self.policy_net(state).argmax(dim=1)
       return action.item()
    
    def fixed_action(self, state):
       #action = self.policy_net(state).argmax(dim=1)
       state=state.squeeze(0).numpy()
       #print(state)
       angle_rad = math.atan2(state[3], state[2])
       #print(angle_rad)
       
       angle_deg = math.degrees(angle_rad)
       angle_deg = (angle_deg + 180) % 360 - 180
    #    print(angle_deg)
       return int(angle_deg)
       #return action.item()
   
    def hit_ball(self, state):
       #action = self.policy_net(state).argmax(dim=1)
       state=state.squeeze(0).numpy()
       print(state)
       angle_rad = math.atan2(state[5], state[4])
       #print(angle_rad)
       
       angle_deg = math.degrees(angle_rad)
       angle_deg = (angle_deg + 180) % 360 - 180
    #    print(angle_deg)
       return int(angle_deg)
       #return action.item()

    def get_state(self, agent, target, ball):
        helper_obj = helper()
        relative_target_x, relative_target_y, relative_ball_x, relative_ball_y=helper_obj.find_relative_target_coordinates(agent, target, ball)
        print(relative_target_y,relative_target_x)
        state=np.array([agent[0], agent[1], relative_target_x, relative_target_y, relative_ball_x, relative_ball_y ])
        state=torch.tensor(state, dtype=torch.float32, device="cpu").unsqueeze(0)
        if np.sqrt(relative_target_x**2 + relative_target_y**2)<0.5:
            return state, True
        return state, False
#env=find_action_and_create_policy()
#state=env.get_state()
#print(env.find_action(state))
