import sys
import unittest
from unittest.mock import patch, MagicMock
import pygame
import time

# Add src to PYTHONPATH
sys.path.insert(0, '/Users/stevenhalla/code/casino_hell/src')  # Adjust this path if necessary

from screen.floor2.battle_screens.hungry_starving_hippos import HungryStarvingHippos


class MockController:
    def __init__(self):
        self.isQPressed = False
        self.isTPressed = False
        self.isBPressed = False
        self.isDownPressed = False
        self.isUpPressed = False
        self.isAPressed = False

    def update(self):
        pass


class MockGameState:
    """Mock game state to avoid loading actual game assets."""

    def __init__(self):
        self.controller = MockController()  # Mock controller
        self.player = MagicMock()  # Mock player
        self.player.luck = 1  # Set a default player luck value
        self.DISPLAY = MagicMock()  # Mock display for Pygame


class HungryStarvingHipposTest(unittest.TestCase):

    def setUp(self):
        """Set up the game and state before each test."""
        pygame.init()  # Initialize pygame before running tests that use it
        self.game = HungryStarvingHippos(screenName="Test Screen")
        self.state = MockGameState()  # Use the simplified MockGameState

        # Initialize the human positions using the game method
        self.game.initialize_human_position(self.state)  # Initialize humans with correct speed and position

    def tearDown(self):
        """Clean up after each test."""
        pygame.quit()  # Quit pygame after tests to clean up resources

    def test_all_humans_race_outcome(self):
        """Test race outcome where humans either reach the finish line or get eaten by the hippo."""
        # Ensure that human positions and speeds are correctly initialized
        print(self.game.humans)  # Print to verify the correct initialization

        # Simulate the start of the race by moving humans
        self.game.human_race_start_time = time.time() - 3  # Simulate that 3 seconds have passed to skip the wait time
        self.game.move_human(delta_time=1)

        # Simulate the hippo moving and eating some humans
        self.game.start_time = time.time() - 11  # Simulate 11 seconds passing to trigger hippo movement
        self.game.move_hippo(delta_time=1)

        # At the end, check how many humans made it to the winners list
        for label in self.game.humans.keys():
            if label in self.game.winners:
                print(f"{label} made it to the finish line!")
            else:
                print(f"{label} was eaten or didn't finish.")

        # Check that A1, with a speed of 44, should be in the winners list
        self.assertIn('A1', self.game.winners, "A1 should win the race due to high speed.")


if __name__ == '__main__':
    unittest.main()
