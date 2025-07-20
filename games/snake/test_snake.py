#!/usr/bin/env python3
"""
Test script for Snake Game
Tests the core game logic without the GUI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from snake_game import Snake, Food, GRID_WIDTH, GRID_HEIGHT, UP, DOWN, LEFT, RIGHT

def test_snake_movement():
    """Test snake movement functionality"""
    print("Testing snake movement...")
    snake = Snake()
    initial_position = snake.body[0]
    
    # Test moving right (default direction)
    snake.move()
    new_position = snake.body[0]
    assert new_position[0] == initial_position[0] + 1, "Snake should move right"
    print("✓ Snake moves right correctly")
    
    # Test changing direction
    snake.change_direction(DOWN)
    snake.move()
    assert snake.body[0][1] == new_position[1] + 1, "Snake should move down"
    print("✓ Snake changes direction correctly")

def test_food_generation():
    """Test food generation and respawning"""
    print("Testing food generation...")
    food = Food()
    initial_pos = food.position
    
    # Test that food position is within bounds
    assert 0 <= initial_pos[0] < GRID_WIDTH, "Food X position should be within bounds"
    assert 0 <= initial_pos[1] < GRID_HEIGHT, "Food Y position should be within bounds"
    print("✓ Food generates within bounds")
    
    # Test food respawn
    snake_body = [(5, 5), (4, 5), (3, 5)]
    food.respawn(snake_body)
    assert food.position not in snake_body, "Food should not spawn on snake body"
    print("✓ Food respawns correctly avoiding snake body")

def test_collision_detection():
    """Test collision detection"""
    print("Testing collision detection...")
    snake = Snake()
    
    # Test wall collision
    snake.body = [(-1, 5)]  # Outside left wall
    assert snake.check_collision(), "Should detect left wall collision"
    
    snake.body = [(GRID_WIDTH, 5)]  # Outside right wall
    assert snake.check_collision(), "Should detect right wall collision"
    
    snake.body = [(5, -1)]  # Outside top wall
    assert snake.check_collision(), "Should detect top wall collision"
    
    snake.body = [(5, GRID_HEIGHT)]  # Outside bottom wall
    assert snake.check_collision(), "Should detect bottom wall collision"
    print("✓ Wall collision detection works")
    
    # Test self collision
    snake.body = [(5, 5), (4, 5), (3, 5), (5, 5)]  # Head collides with body
    assert snake.check_collision(), "Should detect self collision"
    print("✓ Self collision detection works")
    
    # Test no collision
    snake.body = [(5, 5), (4, 5), (3, 5)]  # Normal position
    assert not snake.check_collision(), "Should not detect collision for normal position"
    print("✓ No false collision detection")

def test_snake_growth():
    """Test snake growth mechanism"""
    print("Testing snake growth...")
    snake = Snake()
    initial_length = len(snake.body)
    
    # Trigger growth
    snake.grow_snake()
    snake.move()
    
    assert len(snake.body) == initial_length + 1, "Snake should grow by one segment"
    print("✓ Snake grows correctly when eating food")

def test_direction_restrictions():
    """Test that snake cannot move in opposite direction"""
    print("Testing direction restrictions...")
    snake = Snake()
    snake.direction = RIGHT
    
    # Try to move left (opposite of right) - should be ignored
    snake.change_direction(LEFT)
    assert snake.direction == RIGHT, "Snake should not be able to reverse direction"
    print("✓ Snake cannot reverse direction")
    
    # Try to move up (allowed)
    snake.change_direction(UP)
    assert snake.direction == UP, "Snake should be able to change to perpendicular direction"
    print("✓ Snake can change to perpendicular direction")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Snake Game Logic Tests")
    print("=" * 50)
    
    try:
        test_snake_movement()
        test_food_generation()
        test_collision_detection()
        test_snake_growth()
        test_direction_restrictions()
        
        print("=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("The Snake game logic is working correctly.")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR DURING TESTING: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)