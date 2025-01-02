import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import time
from screeninfo import get_monitors
plt.style.use('dark_background')
import psutil



class Dashboard:                                                # 20, 8
    def __init__(self, title="Agent Training Metrics", figsize=(20, 8)):
        self.fig = plt.figure(figsize=figsize)
        self.title = title
        self.fig.suptitle(self.title, fontsize=16)
        self.gs = GridSpec(4, 3, figure=self.fig, height_ratios=[3, 3, 3, 1])  # Last row is smaller
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.05, right=0.95, top=0.95, bottom=0.05)  # Reduced white space
        plt.tight_layout()
        
        self.cumulative_rewards = []
        self.mean_rewards = []
        self.total_reward = 0
        self.scores = []
        self.action_distribution = {
            "UP" : 0,
            "DOWN" : 0,
            "LEFT" : 0,
            "RIGHT" : 0,
        }
        self.move_efficiency = {
            "total" : 0,
            "improved" : 0,
        }
        self.largest_tiles = []
        self.exploration_rates = []
        self.losses = []
        self.MAEs = []
        self.TD_errors = []
        self.system_resource_metrics = {
            "cpu" : [],
            "memory" : [],
            "battery" : [],
            "disk" : [],
        }
        self.n_games = -1
        self.success_cases = 0
        
        

    def plot_cumulative_rewards(self):
        """Plots cumulative rewards and mean rewards."""
        ax = self.fig.add_subplot(self.gs[0, 0])  # Row 0, Col 0-1
        ax.clear()
        ax.set_title("Cumulative Rewards")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Reward")
        ax.plot(self.cumulative_rewards, label="Rewards")
        ax.plot(self.mean_rewards, label="Mean Rewards")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_score(self):
        """Plots discounted rewards over episodes."""

        ax = self.fig.add_subplot(self.gs[0, 1])  # Row 1, Col 0-1
        ax.clear()
        ax.set_title("Scores over episodes")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Score")
        ax.plot(self.scores, label="Discounted Rewards")
        ax.legend()
        ax.grid()
        plt.pause(0.01)

    def plot_loss(self):
        ax = self.fig.add_subplot(self.gs[1, 0])  # Row 0, Col 2-3
        ax.clear()
        ax.set_title("Loss")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Loss")
        ax.plot(self.losses, label="Loss")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_MAE(self):
        ax = self.fig.add_subplot(self.gs[1, 1])  # Row 0, Col 2-3
        ax.clear()
        ax.set_title("Mean Absolute Error")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("MAE")
        ax.plot(self.MAEs, label="MAE")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_TD_Error(self):
        ax = self.fig.add_subplot(self.gs[1, 2])  # Row 0, Col 2-3
        ax.clear()
        ax.set_title("Temporal Difference Error")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("TD Error")
        ax.plot(self.TD_errors, label="TD Error")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_computational_cost(self):
        """Plots system resource usage (CPU, Memory, Battery, Disk) over time."""
        ax = self.fig.add_subplot(self.gs[2, 0])  # Row 2, Col 2
        ax.clear()
        ax.set_title("Computational Cost")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Resource Usage (%)")

        # Plot each resource metric (CPU, Memory, Battery, Disk) on the same plot
        ax.plot(self.system_resource_metrics["cpu"], label="CPU Usage", color='blue')
        ax.plot(self.system_resource_metrics["memory"], label="Memory Usage", color='green')
        ax.plot(self.system_resource_metrics["battery"], label="Battery Usage", color='red')
        ax.plot(self.system_resource_metrics["disk"], label="Disk Usage", color='purple')

        ax.legend()
        ax.grid()
        plt.pause(0.01)


    def plot_exploration_rate(self):
        """Plots exploration rate decay."""
        ax = self.fig.add_subplot(self.gs[0, 2])  # Row 1, Col 2-3
        ax.clear()
        ax.set_title("Exploration Rate Decay")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Exploration Rate")
        ax.plot(self.exploration_rates, label="Exploration Rate", color="orange")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_action_distribution(self):
        
        actions = list(self.action_distribution.keys())
        counts = list(self.action_distribution.values())
        
        ax = self.fig.add_subplot(self.gs[2, 2])  # Row 0, Col 2-3
        ax.clear()
        ax.bar(actions, counts, color = 'maroon', width=0.4)
        ax.set_title("Action Distribution")
        ax.set_xlabel("Action")
        ax.set_ylabel("Count")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    # def plot_move_efficiency(self):
        
    #     labels = ['Good', 'Bad']
    #     sizes = [self.move_efficiency["improved"], self.move_efficiency["total"]-self.move_efficiency["improved"]]
    #     colors = ['#ff9999', '#66b3ff']
        
    #     ax = self.fig.add_subplot(self.gs[3, 2])  # Row 0, Col 2-3
    #     ax.clear()
    #     plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
    #     ax.set_title("Move Efficiency")
    #     ax.legend()
    #     ax.grid()
        
    def plot_largest_tile(self):
        """Plots largest tile achieved over episodes."""
        ax = self.fig.add_subplot(self.gs[2, 1])  # Row 0, Col 2-3
        ax.clear()
        ax.set_title("Largest Tile Achieved")
        ax.set_xlabel("Episodes")
        ax.set_ylabel("Tile Value")
        ax.plot(self.largest_tiles, label="Max Tile")
        ax.legend()
        ax.grid()
        plt.pause(0.01)
        
    def plot_scalar_metric(self, name, value, row, col):
        """Displays scalar metrics as text."""
        ax = self.fig.add_subplot(self.gs[row, col])  # Specified grid cell
        ax.clear()
        ax.axis("off")
        ax.text(0.5, 0.5, f"{name}: {value}", fontsize=14, ha="center", va="center",
                bbox=dict(boxstyle="round", facecolor="lightblue"))
        plt.pause(0.01)
        

    def update_dashboard(self, success_case, move_efficiency, reward, total_reward, ep_largest_tile, ep_actions, epsilon, loss, score):
        """Updates all plots dynamically with the latest metrics."""
        self.n_games += 1
        if success_case: 
            self.success_cases+=1
            
        self.move_efficiency["total"] += move_efficiency["total"]
        self.move_efficiency["improved"] += move_efficiency["improved"]
        
        self.cumulative_rewards.append(reward)
        self.total_reward += reward
        if total_reward != 0:
            self.mean_rewards.append(total_reward / self.n_games)
        else:
            self.mean_rewards.append(0)

        if ep_largest_tile > 1:
            self.largest_tiles.append(np.power(2, int(ep_largest_tile)))
            
        self.action_distribution["UP"] += ep_actions["UP"]
        self.action_distribution["DOWN"] += ep_actions["DOWN"]
        self.action_distribution["LEFT"] += ep_actions["LEFT"]
        self.action_distribution["RIGHT"] += ep_actions["RIGHT"]
        
        self.exploration_rates.append(epsilon)
        
        self.system_resource_metrics["cpu"].append(psutil.cpu_percent(interval=1))
        self.system_resource_metrics["memory"].append(psutil.virtual_memory().percent)
        self.system_resource_metrics["battery"].append(psutil.sensors_battery().percent)
        self.system_resource_metrics["disk"].append(psutil.disk_usage('/').percent)
        
        self.scores.append(score)
        
        if type(loss) == int:
            self.losses.append(loss)
        else:
            self.losses+=loss
        
        plt.clf()
        self.plot_cumulative_rewards()
        self.plot_largest_tile()
        self.plot_score()
        self.plot_exploration_rate()
        self.plot_action_distribution()
        self.plot_loss()
        self.plot_MAE()
        self.plot_TD_Error()
        self.plot_computational_cost()
        

        # Example scalar metrics
        # self.plot_scalar_metric("Total Reward", metrics["total_reward"], 3, 0)
        self.plot_scalar_metric("Games Played", self.n_games, 3, 0)
        
        if self.n_games != 0:
            success_rate_percentage = int((self.success_cases / self.n_games)*100)
        else: 
            success_rate_percentage = 0
        formatted = f"{success_rate_percentage}%"
        self.plot_scalar_metric("Success Rate (256 tile)", formatted, 3, 1)
        
        
        if self.move_efficiency["total"] != 0:
            percent = int((self.move_efficiency['improved'] / self.move_efficiency['total'])*100)
        else:
            percent = 0
        formatted_percen = f"{percent}%"
        self.plot_scalar_metric("Move Efficiency", formatted_percen, 3, 2)

        plt.pause(0.1)  # Pause for real-time updates



# # Initialize metrics
metrics = {
    "cumulative_rewards": [],
    "cumulative_mean_rewards": [],
    "total_reward": 0,
    "ep_rewards": [],
    "largest_tiles": [],
    "exploration_rate": [],
    "n_episodes": 0,
}

# # Initialize dashboard
# dashboard = Dashboard()

# # Training loop example
# for episode in range(100):
#     reward = np.random.randint(0, 100)  # Simulated reward
#     largest_tile = np.random.randint(2, 2048)  # Simulated largest tile
#     exploration_rate = max(0.01, 1 - episode * 0.01)  # Simulated exploration decay

#     # Update metrics
#     metrics["cumulative_rewards"].append(reward)
#     metrics["total_reward"] += reward
#     metrics["n_episodes"] += 1
#     mean_reward = metrics["total_reward"] / metrics["n_episodes"]
#     metrics["cumulative_mean_rewards"].append(mean_reward)
#     metrics["largest_tiles"].append(largest_tile)
#     metrics["exploration_rate"].append(exploration_rate)

#     # Simulate episode rewards
#     metrics["ep_rewards"].append(reward)

#     # Update dashboard
#     dashboard.update_dashboard(metrics)
#     time.sleep(5)

# plt.show()




