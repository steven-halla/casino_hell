import pygame


class Screen:
    def __init__(self, screenName: str):
        self.screenName = screenName
        self.startedAt = pygame.time.get_ticks()

    def start(self, state: "GameState"):
        self.startedAt = pygame.time.get_ticks()

        pygame.display.set_caption(self.screenName)

    def update(self, state: "GameState"):
        pass

    def draw(self, state: "GameState"):
        pass
