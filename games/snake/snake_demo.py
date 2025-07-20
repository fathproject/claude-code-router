#!/usr/bin/env python3
"""
Text-based Snake Game Demo
A simple text-based version of the snake game that can run in any terminal
"""

import random
import time
import sys
from typing import List, Tuple

class TextSnake:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)  # Right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self) -> Tuple[int, int]:
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
    
    def move(self):
        if self.game_over:
            return
        
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def display(self):
        # Clear screen (works on most terminals)
        print('\033[2J\033[H', end='')
        
        print(f"Score: {self.score}")
        print("=" * (self.width + 2))
        
        for y in range(self.height):
            print("|", end="")
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    print("@", end="")  # Head
                elif (x, y) in self.snake:
                    print("*", end="")  # Body
                elif (x, y) == self.food:
                    print("F", end="")  # Food
                else:
                    print(" ", end="")
            print("|")
        
        print("=" * (self.width + 2))
        
        if self.game_over:
            print("GAME OVER!")
            print(f"Final Score: {self.score}")
        else:
            print("Controls: W=Up, S=Down, A=Left, D=Right, Q=Quit")

def demo_game():
    """Run a demo of the snake game with automatic movement"""
    print("Text-based Snake Game Demo")
    print("Watching AI play automatically...")
    print("Press Ctrl+C to stop")
    
    game = TextSnake(15, 10)
    
    # Simple AI that follows the food
    def get_direction_to_food():
        head_x, head_y = game.snake[0]
        food_x, food_y = game.food
        
        if food_x > head_x:
            return (1, 0)  # Right
        elif food_x < head_x:
            return (-1, 0)  # Left
        elif food_y > head_y:
            return (0, 1)  # Down
        elif food_y < head_y:
            return (0, -1)  # Up
        return game.direction
    
    try:
        while not game.game_over and game.score < 100:  # Stop at score 100 for demo
            # Simple AI strategy
            desired_direction = get_direction_to_food()
            
            # Avoid immediate collision with body
            head_x, head_y = game.snake[0]
            next_pos = (head_x + desired_direction[0], head_y + desired_direction[1])
            
            if next_pos not in game.snake:
                game.direction = desired_direction
            # If collision would occur, try other directions
            else:
                for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    next_pos = (head_x + direction[0], head_y + direction[1])
                    if (next_pos[0] >= 0 and next_pos[0] < game.width and
                        next_pos[1] >= 0 and next_pos[1] < game.height and
                        next_pos not in game.snake):
                        game.direction = direction
                        break
            
            game.move()
            game.display()
            time.sleep(0.3)  # Slower for demo visibility
        
        if game.score >= 100:
            print("Demo completed successfully! Snake reached score 100.")
        
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")
    
    print(f"\nDemo finished. Final score: {game.score}")
    return game.score > 0

if __name__ == "__main__":
    success = demo_game()
    sys.exit(0 if success else 1)