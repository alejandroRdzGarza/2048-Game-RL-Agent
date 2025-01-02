
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os



class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        #1. New network topology and construction
        self.linear_relu_stack = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 4)
        )

    # 2. New feedforward process
    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
        
        

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
        
    def load(self, file_name='model.pth'):
            model_folder_path = './model'
            file_name = os.path.join(model_folder_path, file_name)
            self.load_state_dict(torch.load(file_name))
            self.eval()  # Set the model to evaluation mode
    

