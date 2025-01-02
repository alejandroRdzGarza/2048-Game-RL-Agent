import pygame
import sys
import random
import time
from enum import Enum
import numpy as np
from AgentConfig import *

# Initialize Pygame
pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Constants
WIDTH, HEIGHT = 400, 450
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 36)
BACKGROUND_COLOR = (187, 173, 160)
SCORE_BACKGROUND_COLOR = (255, 255, 255)  # White color for the score area
GAME_OVER_COLOR = (0, 0, 0)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 450
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 160, 210)
TEXT_COLOR = (255, 255, 255)

CELL_COLORS = {
    
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (236, 141, 84),
    32: (246, 124, 95),
    64: (234, 89, 55),
    128: (243, 216, 107),
    256: (241, 208, 75),
    512: (228, 192, 42),
    1024: (226, 186, 19),
    2048: (226, 186, 19),
    # Add more colors for larger numbers if needed
}

SPEED = 100000

class GameAI:
    
    def __init__(self):

        # Create screen
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game")
        
        self.score = 0
        self.state = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 2],
            [0, 0, 0, 2],
        ]
        self.clock = pygame.time.Clock()
        self.reset()
        # self.autoPlay(self.state, self.score)
        
    def update_score(self):
        score = 0
        flat = [tile for row in self.state for tile in row]
        for i in range(GRID_SIZE*GRID_SIZE):
            if flat[i] != 2 and flat[i] != 0:
                multi = np.log2(flat[i])
                score += multi * flat[i]
        self.score = int(score)
        return
        
        
    def get_state(self):
        return self.state
        



    def reset(self):
        self.move = Direction.DOWN
        
        self.score = 0
        self.state = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 32, 8, 16],
        ]
        # self.state = [
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 2],
        #     [0, 0, 0, 2],
        # ]
        
        self.frame_iteration = 0
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Collect player input
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
                
        # 2. move
        self.movement(action) 
        
        # 3. check if game is over
        reward = 0
        game_over = False
        self.update_score()
        if self.gameOver():
            game_over = True
            reward = PENALTY_FOR_LOSING_GAME
            return reward, game_over, self.score
        
        #4. Place new tile
        else:
            reward = 10
            self.addRandomNumber()
        
        # 5. update UI and clock
        self.updateUI()
        self.clock.tick(SPEED)
        
        # 6. Return game over and score
        return reward, game_over, self.score
        
    def gameOver(self):
        
        ogGrid = [row[:] for row in self.state]
        
        moved = self.moveDown(ogGrid)
        if moved:
                return False
        else:
            moves =self.moveRight(ogGrid)
            if moves != 0:
                return False
            else:
                moves = self.moveLeft(ogGrid)
                if moves != 0:
                    return False
                else:
                    moves = self.moveUp(ogGrid)
                    if moves != 0:
                        return False
                    else:
                        return True
        

    def updateUI(self):
        # Draw the score area
        pygame.draw.rect(self.display, SCORE_BACKGROUND_COLOR, (0, 0, WIDTH, 50))  # Top white space
        scoreText = FONT.render(f"Score: {self.score}", True, (0, 0, 0))  # Black text for score
        scoreRect = scoreText.get_rect(center=(WIDTH // 2, 25))  # Centered in the white area
        self.display.blit(scoreText, scoreRect)
        
        # Draw the grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.state[row][col]
                color = CELL_COLORS.get(value, (60, 58, 50))  # Default color for larger numbers
                rect = pygame.Rect(
                    col * CELL_SIZE, 
                    row * CELL_SIZE + 50,  # Offset by 50 to account for score area
                    CELL_SIZE, 
                    CELL_SIZE
                )
                pygame.draw.rect(self.display, color, rect)
                pygame.draw.rect(self.display, (187, 173, 160), rect, 3)  # Border
                
                if value != 0:
                    text = FONT.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=rect.center)
                    self.display.blit(text, text_rect)
                    
                    
    def movement(self, action):
                
        # DOWN
        if np.array_equal(action, [1, 0, 0, 0]):
            self.move = Direction.DOWN
            self.moveDown(self.state)
        # RIGHT
        elif np.array_equal(action, [0, 1, 0, 0]):
            self.move = Direction.RIGHT
            self.moveRight(self.state)
        # LEFT
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.move = Direction.LEFT
            self.moveLeft(self.state)
        # UP
        else:
            self.move = Direction.UP
            self.moveUp(self.state)
            

                
                    
    def addRandomNumber(self):
        zeroes = list()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.state[row][col] == 0:
                    zeroes.append((row, col))
        if len(zeroes) > 0:
            randomNewValue = random.randrange(len(zeroes))
            first, second = zeroes[randomNewValue]
            self.state[first][second] = 2
            self.highlightTile(first, second)
            return True
        else:
            return False
        
    def highlightTile(self, row, col):
        """Highlights a newly added tile with a black border for 0.1 seconds."""
        start_time = time.time()
        # Keep track of the position of the tile to highlight
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)  # 50px offset for score bar
        while time.time() - start_time < 0.1:
            self.updateUI()  # Redraw the grid
            pygame.draw.rect(self.display, (0, 0, 0), rect, 5)  # Draw a thick black border
            pygame.display.flip()
            pygame.time.delay(50)  # Delay for a smooth highlight effect
    
        
    def moveUp(self, grid):
        ogGrid = [row[:] for row in grid]
                
        for col in range(GRID_SIZE):
            
            positiveValues = list()
            zeroes = 0
            for row in range(GRID_SIZE):
                if grid[row][col] != 0:
                    positiveValues.append(grid[row][col])
                else:
                    zeroes+=1
            
            if len(positiveValues) > 0:
                
                ind = 0
                while ind < len(positiveValues)-1:
                    if positiveValues[ind] == positiveValues[ind+1]:
                        positiveValues[ind]*=2
                        positiveValues[ind+1]=0
                        ind+=1
                    ind+=1
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] == 0:
                        zeroes+=1
                        
                zeroesInCol = [0]*zeroes
                newCol = list()
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] != 0:
                        newCol.append(positiveValues[i])
                newCol = newCol+zeroesInCol
                        
                for row in range(GRID_SIZE):
                    grid[row][col] = newCol[row]
                    
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ogGrid[row][col] != grid[row][col]:
                    return True
                        
        return False
                        

    def moveDown(self, grid):
        ogGrid = [row[:] for row in grid]
                
        for col in range(GRID_SIZE):
            
            positiveValues = list()
            zeroes = 0
            for row in range(GRID_SIZE):
                if grid[row][col] != 0:
                    positiveValues.append(grid[row][col])
                else:
                    zeroes+=1
            
            if len(positiveValues) > 0:
                
                ind = len(positiveValues)-1
                while ind > 0:
                    if positiveValues[ind] == positiveValues[ind-1]:
                        positiveValues[ind]*=2
                        positiveValues[ind-1]=0
                        ind-=1
                    ind-=1
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] == 0:
                        zeroes+=1
                        
                newCol = [0]*zeroes
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] != 0:
                        newCol.append(positiveValues[i])
                        
                for row in range(GRID_SIZE):
                    grid[row][col] = newCol[row]
                    

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ogGrid[row][col] != grid[row][col]:
                    return True
                        
        return False
        
                    
            
        


    def moveLeft(self, grid):
        ogGrid = [row[:] for row in grid]
                
        for row in range(GRID_SIZE):
            
            positiveValues = list()
            zeroes = 0
            for col in range(GRID_SIZE):
                if grid[row][col] != 0:
                    positiveValues.append(grid[row][col])
                else:
                    zeroes+=1
            
            if len(positiveValues) > 0:
                
                ind = 0
                while ind < len(positiveValues)-1:
                    if positiveValues[ind] == positiveValues[ind+1]:
                        positiveValues[ind]*=2
                        positiveValues[ind+1]=0
                        ind+=1
                    ind+=1
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] == 0:
                        zeroes+=1
                        
                zeroesInCol = [0]*zeroes
                newCol = list()
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] != 0:
                        newCol.append(positiveValues[i])
                newCol = newCol+zeroesInCol
                        
                for col in range(GRID_SIZE):
                    grid[row][col] = newCol[col]
                    
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ogGrid[row][col] != grid[row][col]:
                    return True
                        
        return False

    def moveRight(self, grid):
        
        ogGrid = [row[:] for row in grid]
                
        for row in range(GRID_SIZE):
            
            positiveValues = list()
            zeroes = 0
            for col in range(GRID_SIZE):
                if grid[row][col] != 0:
                    positiveValues.append(grid[row][col])
                else:
                    zeroes+=1
            
            if len(positiveValues) > 0:
                
                ind = len(positiveValues)-1
                while ind > 0:
                    if positiveValues[ind] == positiveValues[ind-1]:
                        positiveValues[ind]*=2
                        positiveValues[ind-1]=0
                        ind-=1
                    ind-=1
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] == 0:
                        zeroes+=1
                        
                newCol = [0]*zeroes
                
                for i in range(len(positiveValues)):
                    if positiveValues[i] != 0:
                        newCol.append(positiveValues[i])
                        
                for col in range(GRID_SIZE):
                    grid[row][col] = newCol[col]
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if ogGrid[row][col] != grid[row][col]:
                    return True
                
                        
        return False
        
        
    


