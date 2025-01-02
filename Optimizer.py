import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
from AgentConfig import *
import numpy as np

class Optimizer:
    def __init__(self, target_network, policy_network, lr, gamma):
        self.lr = lr # learning rate, ajusta que tanto "salta" la funcion hacia el optimo
        self.gamma = gamma # discount rate
        self.policy = policy_network # neural network
        self.target = target_network
        self.optimizer = optim.Adam(policy_network.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.steps = 0

    def train_step(self, state, action, reward, next_state):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        
        q_values = self.policy(state)
        q_next = self.target(next_state)
        
        target = reward + (self.gamma * torch.max(q_next))
        q_value = q_values[0][action.index(1)]
        q_value = torch.tensor([q_value], requires_grad=True)
        target = torch.tensor([target], requires_grad=True)
    
        
        # Compute loss
        loss = self.criterion(q_value, target)
        
        # Backpropagation
        loss.backward()
    
        # Optimize policy network
        self.optimizer.step()
        
        # Zero gradients
        self.optimizer.zero_grad()

        self.steps += 1
        
        if self.steps % UPDATE_TARGET_EVERY_N_STEPS == 0:
            return True, loss.item()
        else:
            return False, loss.item()
