import matplotlib.pyplot as plt
from IPython import display
import time

plt.ion()



class Metrics:
    
    def __init__(self):
        self.cumulative_rewards = []
        self.cumulative_mean_rewards = []
        self.total_reward = 0
        self.ep_rewards = []
        self.largest_tiles = []
    

    # displays reward per episode over time
    def cumulative_reward(self, rewards, mean_rewards):
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Reward')
        plt.plot(rewards, label="Rewards")
        plt.plot(mean_rewards, label="Mean Rewards")
        plt.ylim(ymin=0)
        plt.text(len(rewards)-1, rewards[-1], str(rewards[-1]))
        plt.text(len(mean_rewards)-1, mean_rewards[-1], str(mean_rewards[-1]))
        plt.legend()
        plt.draw()
        plt.pause(.1)
        
    def update_cumulative_reward(self, reward, total_reward, n_episodes):
        self.cumulative_rewards.append(reward)
        self.total_reward += reward
        mean_reward = total_reward / n_episodes
        self.cumulative_mean_rewards.append(mean_reward)
        self.cumulative_reward(self.cumulative_rewards, self.cumulative_mean_rewards)
    
    # simple xy plot that displays discounted rewards over episodes
    def discounted_cumulative_reward(self, gamma):
        discounted_rewards = []
        cumulative_reward = 0
        
        for reward in reversed(self.ep_rewards):
            cumulative_reward = reward + gamma * cumulative_reward
            discounted_rewards.insert(0, cumulative_reward)
            
        return discounted_rewards
        
    # pie chart of episodes in which x tile was acheived and rest of episode count
    def success_rate(self):
        pass
        
    # histogram or similar that displays the count for each action
    def action_distribution(self):
        pass
    
    # A measure of how the expected reward (Q-value) increases over time for the chosen actions. 
    def policy_improvement(self):
        pass
    
    # xy plot of difference between inference and target over time
    def loss(self):
        pass
    def mean_absolute_error(self):
        pass
    
    def temporal_difference_error(self):
        pass
    
    def time_convergence(self):
        pass
    
    def computational_cost(self):
        pass
    
    # Tracks the decay of the exploration parameter over time
    # Simple xy plot
    def exploration_rate(self):
        pass
    def state_coverage(self):
        pass
    
    # simple xy plot
    def largest_tile_achieved(self):
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Max Tile')
        plt.plot(self.largest_tiles, label="Rewards")
        plt.ylim(ymin=0)
        plt.text(len(self.largest_tiles)-1, self.largest_tiles[-1], str(self.largest_tiles[-1]))
        plt.legend()
        plt.draw()
        plt.pause(.1)
    
    def update_largest_tile_achieved(self, largest_tile):
        self.largest_tiles.append(largest_tile)
        self.largest_tile_achieved()
    
    # number of score increasing moves / total moves across time (episode discrete count)
    # can also have a mean over all episodes
    # xy plot
    def move_efficiency(self):
        pass

    
