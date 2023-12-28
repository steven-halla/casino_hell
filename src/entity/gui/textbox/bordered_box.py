import pygame

from entity.entity import Entity


class BorderedBox(Entity):
    def __init__(self, rect: tuple[int, int, int, int], border_width: int = 5):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.border_width = border_width

    def update(self, state: "GameState"):
        pass

    def draw(self, state: "GameState"):
        # draw text box border
        black_box = pygame.Surface(
            (self.collision.width, self.collision.height))
        black_box.fill((0, 0, 0))
        # Create the white border
        white_border = pygame.Surface((
                                      self.collision.width + 2 * self.border_width,
                                      self.collision.height + 2 * self.border_width))
        white_border.fill((255, 255, 255))
        black_box = pygame.Surface(
            (self.collision.width, self.collision.height))
        black_box.fill((0, 0, 0))
        white_border.blit(black_box, (self.border_width, self.border_width))
        state.DISPLAY.blit(white_border, (self.position.x, self.position.y))
