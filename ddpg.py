# DDPG agent
import numpy as np
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from tensorboardX import SummaryWriter

from actor_critic import Actor, Critic
from replay_buffer import ReplayBuffer, OUNoise
from hyperparams import LR_ACTOR, LR_CRITIC, WEIGHT_DECAY, BATCH_SIZE, GAMMA, TAU

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # current state_size -> 11
        # current action_size -> 2

class DDPG:
    def __init__(self, state_size, action_size, hidden_size):

        self.actor_loss_value = 0
        self.critic_loss_value = 0
        self.actor = Actor(state_size, action_size, hidden_size).to(device)
        self.target_actor = copy.deepcopy(self.actor).to(device)
        self.critic = Critic(state_size, action_size, hidden_size).to(device)
        self.target_critic = copy.deepcopy(self.critic).to(device)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=LR_ACTOR)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=LR_CRITIC, weight_decay=WEIGHT_DECAY)
        self.replay_buffer = ReplayBuffer()
        
        # Initialize Ornstein-Uhlenbeck noise
        self.noise = OUNoise(action_size)
        self.writer = SummaryWriter()
		
    def write_summary(self, episode, reward, loss_actor, loss_critic):
        #log values for evaluation curves
        self.writer.add_scalar('Reward', reward, episode)
        self.writer.add_scalar('Loss/Actor', loss_actor, episode)
        self.writer.add_scalar('Loss/Critic', loss_critic, episode)
        

    def act(self, state, epsilon=0):
        # print(state.shape)
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        self.actor.eval()
        with torch.no_grad():
            action = self.actor(state).cpu().data.numpy()
        self.actor.train()
        action += epsilon * self.noise.sample()  
        return np.clip(action, -1, 1)
    
    def train(self):
        if len(self.replay_buffer.buffer) < BATCH_SIZE:
            return
        
        state, action, reward, next_state, done = self.replay_buffer.sample(BATCH_SIZE)
        state = torch.FloatTensor(state).to(device)
        action = torch.FloatTensor(action).to(device)
        reward = torch.FloatTensor(reward).to(device)
        next_state = torch.FloatTensor(next_state).to(device)
        done = torch.FloatTensor(done).to(device)
        
        # Update critic
        #print(action)
        Q = self.critic(state, action)
        next_action = self.target_actor(next_state)
        next_Q = self.target_critic(next_state, next_action.detach())
        target_Q = reward + GAMMA * next_Q * (1 - done)
        critic_loss = nn.MSELoss()(Q, target_Q.detach())
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        self.critic_loss_value = critic_loss.item()
        
        # Update actor
        actor_loss = -self.critic(state, self.actor(state)).mean()
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        self.actor_loss_value = actor_loss.item()

        
        # Update target networks
        for target, source in zip(self.target_critic.parameters(), self.critic.parameters()):
            target.data.copy_(TAU * source.data + (1 - TAU) * target.data)
        for target, source in zip(self.target_actor.parameters(), self.actor.parameters()):
            target.data.copy_(TAU * source.data + (1 - TAU) * target.data)
        
    def update_replay_buffer(self, state, action, reward, next_state, done):
        self.replay_buffer.add(state, action, reward, next_state, done)
        
    def save(self, filename):
        torch.save(self.actor.state_dict(), filename + "_actor.pth")
        torch.save(self.critic.state_dict(), filename + "_critic.pth")
        
    def load(self, filename):
        self.actor.load_state_dict(torch.load(filename + "_actor.pth", map_location=device))
        self.target_actor = copy.deepcopy(self.actor)
        self.critic.load_state_dict(torch.load(filename + "_critic.pth", map_location=device))
        self.target_critic = copy.deepcopy(self.critic)
