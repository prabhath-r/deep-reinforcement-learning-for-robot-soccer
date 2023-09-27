import torch
import torch.nn as nn

# Actor network
class Actor(nn.Module):
    def __init__(self, state_size, action_size, hidden_size):
        super(Actor, self).__init__()
        
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        
        self.fc3 = nn.Linear(hidden_size, action_size)
        
        self.lrelu = nn.LeakyReLU()
        self.tanh = nn.Tanh()

    def forward(self, state):
        x = self.fc1(state)
        x = self.bn1(x)
        x = self.lrelu(x)
        
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.lrelu(x)
        
        x = self.fc3(x)
        x = self.tanh(x)
        return x

# Critic network
class Critic(nn.Module):
    def __init__(self, state_size, action_size, hidden_size):
        super(Critic, self).__init__()
        
        self.fc1 = nn.Linear(state_size + action_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.bn3 = nn.BatchNorm1d(hidden_size)
        
        self.fc4 = nn.Linear(hidden_size, 1)
        
        self.lrelu = nn.LeakyReLU()

    def forward(self, state, action):
        # Concatenate state and action
        x = torch.cat([state, action], 1)
        
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.lrelu(x)
        
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.lrelu(x)
        
        x = self.fc3(x)
        x = self.bn3(x)
        x = self.lrelu(x)
        
        x = self.fc4(x)
        
        return x