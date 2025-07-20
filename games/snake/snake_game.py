#!/usr/bin/env python3
"""
Snake Game Implementation
A classic Snake game using pygame library.
"""

import pygame
import random
import sys
from typing import List, Tuple

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 150, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body: List[Tuple[int, int]] = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction: Tuple[int, int]):
        # Prevent the snake from moving in the opposite direction
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def check_collision(self) -> bool:
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        
        # Check self collision
        if self.body[0] in self.body[1:]:
            return True
        
        return False

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self) -> Tuple[int, int]:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake_body: List[Tuple[int, int]]):
        while True:
            new_position = self.generate_position()
            if new_position not in snake_body:
                self.position = new_position
                break

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        if not self.game_over:
            self.snake.move()
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow_snake()
                self.food.respawn(self.snake.body)
                self.score += 10
            
            # Check game over conditions
            if self.snake.check_collision():
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            color = GREEN if i == 0 else DARK_GREEN  # Head is brighter
            pygame.draw.rect(self.screen, color, 
                           (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw food
        x, y = self.food.position
        pygame.draw.rect(self.screen, RED, 
                        (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, WHITE)
            restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for a moderate game speed
        
        pygame.quit()
        sys.exit()

def main():
    """Main function to start the Snake game."""
    try:
        game = Game()
        print("Starting Snake Game...")
        print("Controls:")
        print("  Arrow Keys - Move snake")
        print("  R - Restart game (when game over)")
        print("  ESC - Quit game")
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        print("Make sure pygame is installed: pip install pygame")
        sys.exit(1)

if __name__ == "__main__":
    main()