import pygame
import logging
from game_state import GameState

# logging.basicConfig(
#     level=logging.INFO,  # INFO
#     format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
# )

# Instantiate mixer
# this is where we get our music:
# https://soundimage.org/chiptunes-2/

class Game:
    def __init__(self):
        # global logging
        pygame.init()
        pygame.display.set_caption("Casino Man")
        self.state = GameState()  # create a new GameState()

    def start(self):
        clock = pygame.time.Clock()
        # print(clock)

        self.state.currentScreen.start(self.state)

        while self.state.isRunning:

            self.state.delta = clock.tick(60)

            # will need to move this to Screen class
            # TODO maintain framerate pygame.
            self.state.currentScreen.update(self.state)
            self.state.currentScreen.draw(self.state)
            # self.textBox.update(self.state)
            # self.textBox.display()

        pygame.quit()
