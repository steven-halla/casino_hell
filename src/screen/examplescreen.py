

import pygame



def draw(self, state: "GameState"):
    state.DISPLAY.fill((0, 0, 51))

    # this box is for hero info
    box_width = 200 - 10
    box_height = 180 - 10
    new_box_height = box_height + 40
    black_box = pygame.Surface((box_width, new_box_height))
    black_box.fill((0, 0, 0))
    border_width = 5
    white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
    white_border.fill((255, 255, 255))
    white_border.blit(black_box, (border_width, border_width))
    state.DISPLAY.blit(white_border, (25, 235 - 40))

    # Box for hero name
    black_box = pygame.Surface((200 - 10, 45 - 10))
    black_box.fill((0, 0, 0))
    border_width = 5
    white_border = pygame.Surface(
        (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
    white_border.fill((255, 255, 255))
    white_border.blit(black_box, (border_width, border_width))
    state.DISPLAY.blit(white_border, (25, 195 - 40))  # Moved up by 40 pixels
    state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
                                        (255, 255, 255)), (37, 250 - 40))
    state.DISPLAY.blit(
        self.font.render(f"HP: {state.player.stamina_points}", True,
                         (255, 255, 255)), (37, 290 - 40))

    state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                        (255, 255, 255)), (37, 330 - 40))
    state.DISPLAY.blit(
        self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)),
        (37, 370 - 40))

    state.DISPLAY.blit(self.font.render(f"Score: {self.player_score} ", True, (255, 255, 255)), (37, 370))

    state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                       (37, 205 - 40))

    # the below is for enemy boxes
    # holds enemy name
    black_box = pygame.Surface((200 - 10, 110 - 10))
    black_box.fill((0, 0, 0))
    border_width = 5
    white_border = pygame.Surface(
        (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
    white_border.fill((255, 255, 255))
    white_border.blit(black_box, (border_width, border_width))
    state.DISPLAY.blit(white_border, (25, 20))

    state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))

    # holds enemy status, money and other info
    # Original dimensions
    box_width = 200 - 10
    box_height = 130 - 10

    # New height: 40 pixels smaller
    new_box_height = box_height - 40

    # Create the black box with the new height
    black_box = pygame.Surface((box_width, new_box_height))
    black_box.fill((0, 0, 0))
    border_width = 5
    white_border = pygame.Surface((box_width + 2 * border_width, new_box_height + 2 * border_width))
    white_border.fill((255, 255, 255))
    white_border.blit(black_box, (border_width, border_width))
    state.DISPLAY.blit(white_border, (25, 60))

    state.DISPLAY.blit(self.font.render(f"Money: {self.sallyOpossumMoney}", True,
                                        (255, 255, 255)), (37, 70))

    state.DISPLAY.blit(self.font.render(f"Status: normal", True,
                                        (255, 255, 255)), (37, 110))

    # this creates the text box for our below messages
    black_box_height = 130
    black_box_width = 700
    border_width = 5
    black_box = pygame.Surface((black_box_width, black_box_height))
    black_box.fill((0, 0, 0))
    white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
    white_border.fill((255, 255, 255))
    white_border.blit(black_box, (border_width, border_width))
    screen_width, screen_height = state.DISPLAY.get_size()
    black_box_x = (screen_width - black_box_width) // 2 - border_width
    black_box_y = screen_height - black_box_height - 20 - border_width
    state.DISPLAY.blit(white_border, (black_box_x, black_box_y))

    pygame.display.flip()