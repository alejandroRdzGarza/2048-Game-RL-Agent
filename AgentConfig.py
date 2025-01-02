
REPLAY_BUFFER_SIZE = 100000 # number of episodes the agent's memory can hold
BATCH_SIZE = 100 # The number of samples taken from the replay buffer for each training step.
LR = 0.001 # The learning rate controls the step size in updating the weights of the neural network during training.
GAMMA = 0.9 # it is the discount factor, it determines how much future rewards contribute to the present decision
EPSILON_INITIAL = 1.0 #controls exploration vs exploitation using the epsilon-greedy approach
MODEL_PATH = 'model.pth'
SCORE_FILE = 'matrix.txt'
UPDATE_TARGET_EVERY_N_STEPS = 1000
DECAY_RATE = 0.9995
MIN_EPSILON = 0.01
EPOCHS = 100
SUCCESS_CASE = 8.0
PENALTY_FOR_LOSING_GAME = -500