from agent import Agent
from game import GameAI
from Trainer import Trainer
from Dashboard import Dashboard
import threading

def main():
    agent = Agent()
    game = GameAI()
    dash = Dashboard()
    trainer = Trainer(agent, game, agent.n_episodes)
    
    move_efficiency = {
        "total" : 0,
        "improved" : 0,
    }
    
    ep_actions = {
        "UP" : 0,
        "DOWN" : 0,
        "LEFT" : 0,
        "RIGHT" : 0,
    }
    
    dash.update_dashboard(success_case=False, move_efficiency=move_efficiency, reward=0, total_reward=0, ep_largest_tile=0, ep_actions=ep_actions, epsilon=1.0, loss=0, score=0)
    
    while agent.n_episodes > 0:
        playing = True
        success_case = False
        move_efficiency = {
            "total" : 0,
            "improved" : 0,
        }
        ep_actions = {
            "UP" : 0,
            "DOWN" : 0,
            "LEFT" : 0,
            "RIGHT" : 0,
        }
        while playing:
            playing, success_case_in_game, move_efficiency, reward, total_reward, largest_tile, ep_actions, epsilon, loss, score = trainer.play_step()
            if success_case_in_game:
                success_case = True
        
        dash.update_dashboard(success_case=success_case, 
                              move_efficiency=move_efficiency, 
                              reward=reward, 
                              total_reward=total_reward, 
                              ep_largest_tile=largest_tile,
                              ep_actions=ep_actions,
                              epsilon=epsilon,
                              loss=loss,
                              score=score
                            )
    return 0

if __name__ == "__main__":
    main()