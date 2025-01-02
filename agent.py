import torch
import random
import numpy as np 
from collections import deque
from game import GameAI, Direction
from model import DQN
from helper import plot
import os
from AgentConfig import *
from Trainer import Trainer
from Optimizer import Optimizer



class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon =  EPSILON_INITIAL # exploration vs exploitation
        self.gamma =  GAMMA # discount rate for future rewards
        self.experience_replay = deque(maxlen=REPLAY_BUFFER_SIZE) # popleft() when needed
        self.update_target_network = UPDATE_TARGET_EVERY_N_STEPS
        # (input size, hidden size, output size)
        self.policy_network = DQN()
        self.target_network = DQN()
        self.optimizer = Optimizer(self.target_network, self.policy_network, lr=LR, gamma=self.gamma)
        self.step = 0
        self.decay_rate = DECAY_RATE
        self.n_episodes = EPOCHS # number of episodes/epochs to train over
        
    def get_state(self, game):
        # 4. New way to return inputs to the neural netwrok already normalized using log2
        board = np.array(game)
        board = np.where(board > 0, np.log2(board), 0)
        return torch.tensor(board).unsqueeze(0)
    
    def get_n_games(self):
        return self.n_games
    
    def update_target(self):
        self.target_network.load_state_dict(self.policy_network.state_dict())
    
    def remember(self, s, a, r, s_prime):
        self.experience_replay.append((s, a, r, s_prime)) #popleft if MAX_MEMORY is reached
    
    def train_long_memory(self):
        losses = []
        if len(self.experience_replay) > BATCH_SIZE:
            mini_sample = random.sample(self.experience_replay, BATCH_SIZE) # Random sampling (Uniform sampling)
        else:
            mini_sample = self.experience_replay

        states, actions, rewards, next_states = zip(*mini_sample)
        for state, action, reward, next_state in zip(states, actions, rewards, next_states):
            update, loss = self.optimizer.train_step(state, action, reward, next_state)
            losses.append(loss)
            if update:
                self.update_target()
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)
        return losses


    def train_short_memory(self, s, a, r, s_prime):
        update, loss = self.optimizer.train_step(s, a, r, s_prime)
        if update:
            self.update_target()
        return loss
        

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = max(self.decay_rate * self.epsilon, MIN_EPSILON)
        # self.epsilon = max(0.1, 80 - self.n_games)  # Cap at 0.1 to avoid excessive randomness
        # self.epsilon = max(0.1, self.epsilon * 0.995)  # Decay epsilon by 0.995 after each game
                    # Up, Right, Down, Left
        final_move = [0,0,0,0]
        probability = np.random.random()
        if probability < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.policy_network(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
    def get_epsilon(self):
        return self.epsilon
    
    

    
    
    