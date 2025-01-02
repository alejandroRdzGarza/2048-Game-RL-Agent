import numpy as np
from helper import plot
from AgentConfig import *
import threading
import torch


class Trainer:
    
    def __init__(self, agent, game, n_episodes):
        self.agent = agent
        self.game = game
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.ep_score = 0
        self.record = 0
        self.total_reward = 0
        self.ep_reward = 0
        self.step = 0
        self.step_improved = 0
        self.current_episode = 0
        self.n_episodes = n_episodes
        self.ep_largest_tile = 0
        self.ep_actions = {
                        "UP" : 0,
                        "DOWN" : 0,
                        "LEFT" : 0,
                        "RIGHT" : 0,
                    }
        self.losses = []
        

        
    def play_step(self):
        self.step += 1
        
        state_old = self.agent.get_state(self.game.get_state())
        final_move = self.agent.get_action(state_old)
        reward, done, score = self.game.play_step(final_move)
        state_new = self.agent.get_state(self.game.get_state())
        
        mono = self.calculate_monotonicity(state_new)
        
        self.ep_actions
        reward_for_increasing_score = int((score - self.ep_score) / 10)
        if self.ep_score != score:
            self.step_improved += 1
            
        self.ep_score = score
        
        success_case = SUCCESS_CASE in state_new
        
        # DOWN
        if np.array_equal(final_move, [1, 0, 0, 0]):
            self.ep_actions["DOWN"]+=1
        # RIGHT
        elif np.array_equal(final_move, [0, 1, 0, 0]):
            self.ep_actions["RIGHT"]+=1
        # LEFT
        elif np.array_equal(final_move, [0, 0, 1, 0]):
            self.ep_actions["LEFT"]+=1
        # UP
        else:
            self.ep_actions["UP"]+=1
                    
        
        if torch.equal(state_new, state_old):
            reward-=10
        else:
        
            # Reward for merging tiles
            merge_reward = self.calculate_merge_reward(np.array(state_old), np.array(state_new))
            reward += merge_reward
            reward += reward_for_increasing_score
        
        self.total_reward += reward
        self.ep_reward += reward
        
        
        loss = self.agent.train_short_memory(state_old, final_move, reward, state_new)
        self.losses.append(loss)
        self.agent.remember(state_old, final_move, reward, state_new)
        
        move_efficiency = {"total":0, "improved":0}
        reward = self.ep_reward
        ep_actions = {
            "UP" : self.ep_actions["UP"],
            "DOWN" : self.ep_actions["DOWN"],
            "LEFT" : self.ep_actions["LEFT"],
            "RIGHT" : self.ep_actions["RIGHT"],
        }
        
        epsilon = self.agent.get_epsilon()
        if done:
            move_efficiency["total"] = self.step
            move_efficiency["improved"] = self.step_improved
            self.ep_score = 0
            self.current_episode += 1
            self.ep_reward = 0
            self.step = 0
            self.end_episode(score, state_old)
            largest_tile = state_new.max()
            self.ep_actions["UP"]=0
            self.ep_actions["DOWN"]=0
            self.ep_actions["RIGHT"]=0
            self.ep_actions["LEFT"]=0
            return False, success_case, move_efficiency, reward, self.total_reward, largest_tile.item(), ep_actions, epsilon, self.losses, score
        else:
            return True, success_case, move_efficiency, reward, self.total_reward, 0, ep_actions, epsilon, self.losses, score
            
            
            
    def end_episode(self, score, state_old):
        self.game.reset()
        self.agent.n_games += 1
        loss = self.agent.train_long_memory()
        self.losses += loss

        if score > self.record:
            self.record = score
            self.agent.policy_network.save(MODEL_PATH)
            

        #self.update_plot(score)

        
        
    # def update_plot(self, score):
    #         self.plot_scores.append(score)
    #         self.total_score += score
    #         mean_score = self.total_score / self.agent.get_n_games()
    #         self.plot_mean_scores.append(mean_score)
    #         plot(self.plot_scores, self.plot_mean_scores)
            
    
    def calculate_merge_reward(self, prev_state, curr_state):
        merge_reward = 0
        
        prev_flat = prev_state.flatten()
        new_flat = curr_state.flatten()
        
        for prev, new in zip(prev_flat, new_flat):
            if new > prev and new != 0:
                merge_reward += int(new/10)
                
        return merge_reward
    
    def calculate_monotonicity(self, state):
        first = state[0][0].tolist()
        second = state[0][1].tolist()[::-1]
        third = state[0][2].tolist()
        fourth = state[0][3].tolist()[::-1]
        
        board = []
        board += fourth
        board += third
        board += second
        board += first
        
        for i in range(len(board)):
            board[i] = int(board[i])
            
        ordered = sorted(board, reverse=True)
        
        reward = 0
        visited_indices = set()  # Track visited indices to avoid duplicate issues
    
        for i in range(len(ordered)):
            if ordered[i] == board[i]:
                reward += ordered[i] * 10
            else:
                # Find correct index of the current value in board
                for j, val in enumerate(board):
                    if val == ordered[i] and j not in visited_indices:
                        visited_indices.add(j)
                        distance = abs(j - i)  # Absolute distance
                        dif = abs(ordered[i] - board[i])  # Absolute difference
                        reward -= distance * dif * 10
                        break
                    
        return reward
        


    
        
            

            

            