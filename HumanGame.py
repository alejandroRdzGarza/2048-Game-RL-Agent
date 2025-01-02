import pygame
import sys
import random
import time
from enum import Enum

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

class GameAI:
    
    def __init__(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Modes")
        
        mode = self.openingScreen(screen)
        
        if mode == "autoplay":
            self.score  = 0
            self.state = [
                [0, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 2],
                [0, 0, 2, 2],
            ]
            # Create screen
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("2048 Game")
            self.autoPlay(self.state, self.score)
        elif mode == "selfplay":
            # Create screen
            self.display = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("2048 Game")
            self.selfPlay()





    # Draw the grid
    def draw_grid(self, grid, score):
        # Draw the score area
        pygame.draw.rect(self.display, SCORE_BACKGROUND_COLOR, (0, 0, WIDTH, 50))  # Top white space
        scoreText = FONT.render(f"Score: {score}", True, (0, 0, 0))  # Black text for score
        scoreRect = scoreText.get_rect(center=(WIDTH // 2, 25))  # Centered in the white area
        self.display.blit(scoreText, scoreRect)
        
        # Draw the grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
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
                
                    
    def addRandomNumber(self, grid, score):
        zeroes = list()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    zeroes.append((row, col))
        if len(zeroes) > 0:
            randomNewValue = random.randrange(len(zeroes))
            first, second = zeroes[randomNewValue]
            # 3. Added random spawning of 4 with a 10% chance
            r = random.randrange(0,10)
            if r < 9:
                grid[first][second] = 2
            else:
                grid[first][second] = 4
            self.highlightTile(first, second, grid, score)
            return True
        else:
            return False
        
    def highlightTile(self, row, col, grid, score):
        """Highlights a newly added tile with a black border for 1 second."""
        start_time = time.time()
        while time.time() - start_time < 0.1:
            self.draw_grid(grid, score)  # Redraw the grid
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display, (0, 0, 0), rect, 5)  # Draw a thick black border
            pygame.display.flip()
            pygame.time.delay(50)  # Prevent overloading the loop
    
        
    def moveUp(grid):
        ogGrid = [row[:] for row in grid]
        extraScore = 0
                
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
                        extraScore+=positiveValues[ind]
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
                    return True, extraScore
                        
        return False, extraScore
                        

    def moveDown(grid):
        ogGrid = [row[:] for row in grid]
        newScore = 0
                
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
                        newScore+=positiveValues[ind]
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
                    return True, newScore
                        
        return False, newScore
        
                    
            
        


    def moveLeft(grid):
        ogGrid = [row[:] for row in grid]
        extraScore = 0
                
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
                        extraScore+=positiveValues[ind]
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
                    return True, extraScore
                        
        return False, extraScore

    def moveRight(grid):
        
        ogGrid = [row[:] for row in grid]
        extraScore = 0
                
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
                        extraScore+=positiveValues[ind]
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
                    return True, extraScore
                        
        return False, extraScore
        

    # Function to display the end screen
    def displayEndScreen(self, score):
        self.display.fill(BACKGROUND_COLOR)
        game_over_text = FONT.render("Game Over!", True, GAME_OVER_COLOR)
        score_text = FONT.render(f"Final Score: {score}", True, GAME_OVER_COLOR)
        restart_text = FONT.render("Press R to Restart", True, GAME_OVER_COLOR)
        
        self.display.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        self.display.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        self.display.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
        pygame.display.flip()
    
    
    def createButton(self, screen, text, x, y, width, height, button_color, hover_color, font, text_color):
        """
        Draw a button with hover effect and return its rect.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(screen, button_color, (x, y, width, height))

        # Add text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

        return False

    def openingScreen(self, screen):
        """
        Displays the opening screen with two buttons.
        Returns the chosen mode: 'autoplay' or 'selfplay'.
        """
        while True:
            screen.fill(BACKGROUND_COLOR)
            title = FONT.render("Choose a Mode", True, TEXT_COLOR)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title, title_rect)

            autoplay_clicked = self.createButton(
                screen, "Autoplay", 
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 
                200, BUTTON_WIDTH, BUTTON_HEIGHT, 
                BUTTON_COLOR, HOVER_COLOR, FONT, TEXT_COLOR
            )
            selfplay_clicked = self.createButton(
                screen, "Self-Play", 
                SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 
                300, BUTTON_WIDTH, BUTTON_HEIGHT, 
                BUTTON_COLOR, HOVER_COLOR, FONT, TEXT_COLOR
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if autoplay_clicked:
                return "autoplay"
            if selfplay_clicked:
                return "selfplay"

            pygame.display.flip()
                
    

    # Main loop
    def autoPlay(self, grid, score):
        
        
        running = True
        gameOver = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if gameOver and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    grid = [
                        [0, 2, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 2],
                        [0, 0, 2, 2],
                    ]
                    gameOver = False
                    time.sleep(1)
                    
            
            
            for i in range(GRID_SIZE):
                print(grid[i])
            print("\n")
            if gameOver:
                self.displayEndScreen(score)
            else:
                moved, extraScore = self.moveDown(grid)
                score+=extraScore
                if moved:
                    self.addRandomNumber(grid, score)
                else:
                    moves, extraScore =self.moveRight(grid)
                    score+=extraScore
                    if moves != 0:
                        self.addRandomNumber(grid, score)
                    else:
                        moves, extraScore = self.moveLeft(grid)
                        score+=extraScore
                        if moves != 0:
                            self.addRandomNumber(grid, score)
                        else:
                            moves, extraScore = self.moveUp(grid)
                            score+=extraScore
                            if moves != 0:
                                self.addRandomNumber(grid, score)
                            else:
                                gameOver = True
                print(f"score is: {score}")
            
            
            
                self.draw_grid(grid, score)
                
            pygame.display.flip()
            time.sleep(0.1)
            

        pygame.quit()
        sys.exit()
        
        
    def selfPlay(self):
        score  = 0
        grid = [
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 2],
            [0, 0, 2, 2],
        ]
        
        running = True
        gameOver = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif gameOver and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    grid = [
                        [0, 2, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 2],
                        [0, 0, 2, 2],
                    ]
                    gameOver = False
                    time.sleep(1)
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    moved, extraScore = self.moveUp(grid)
                    score+= extraScore
                    self.addRandomNumber(grid, score)
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    moved, extraScore = self.moveDown(grid)
                    score+= extraScore
                    self.addRandomNumber(grid, score)
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    moved, extraScore = self.moveRight(grid)
                    score+= extraScore
                    self.addRandomNumber(grid, score)
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    moved, extraScore = self.moveLeft(grid)
                    score+= extraScore
                    self.addRandomNumber(grid, score)
                
                    
            
            
            
                print(f"score is: {score}")
            
            
            
                self.draw_grid(grid, score)
                
            pygame.display.flip()
            time.sleep(0.1)
            

        pygame.quit()
        sys.exit()
        


