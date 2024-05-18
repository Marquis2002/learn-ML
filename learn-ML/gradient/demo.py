import functorch.dim
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
# PyTorch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
# Gym
import gym
import imageio
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
env_id = "CartPole-v1"

env = gym.make(env_id, render_mode='human')
eval_env = gym.make(env_id, render_mode='human')

s_size = env.observation_space.shape[0]
a_size = env.action_space.n

print(s_size, a_size)

class Policy(nn.Module):
    def __init__(self, s_size, a_size, h_size): # hidden layer
        super(Policy, self).__init__()
        self.fc1 = nn.Linear(s_size, h_size)
        self.fc2 = nn.Linear(h_size, a_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

    def act(self, state): # (45, )
        try:
            torch.from_numpy(state[0]).float().unsqueeze(0).to(device)
        except:
            torch.from_numpy(state).float().unsqueeze(0).to(device)
        probs = self.forward(state).cpu()
        m = Categorical(probs)
        action = m.sample()
        return action.item(), m.log_prob(action)
