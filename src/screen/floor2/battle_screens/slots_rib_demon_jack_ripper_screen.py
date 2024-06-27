import pygame
from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen


class SlotsRibDemonJackRipperScreen(Screen):
    def __init__(self):
        super().__init__("Casino Slots Screen")

        self.play_again = True
        self.new_font = pygame.font.Font(None, 36)
        self.game_state = "welcome_screen"
        self.bet = 0
        self.money = 1000
        self.font = pygame.font.Font(None, 36)
        self.battle_messages = {
            "welcome_message": TextBox(
                ["Are you here for some rib demon slots?", ""],
                (65, 460, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),


            # You can add more game state keys and TextBox instances here
        }

    def update(self, state: "GameState"):
        if self.game_state == "welcome_screen":
            print("welcome high update")
            self.battle_messages["welcome_message"].update(state)


        if state.controller.isQPressed:
            # Transition to the main screen
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        # Update the controller
        controller = state.controller
        controller.update()

    def draw(self, state: "GameState"):
        state.DISPLAY.fill((0, 0, 51))

        # this is for black box this is just helper code should not stay here forever

        # this box is for hero money, bet amount, and other info
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))
        # holds hero name
        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True, (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(self.font.render(f"HP: {state.player.stamina_points}", True, (255, 255, 255)), (37, 290))
        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True, (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)), (37, 205))
        # holds enemy name
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))
        # holds enemy status, money, and other info
        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.money}", True, (255, 255, 255)), (37, 70))
        state.DISPLAY.blit(self.font.render(f"Status: ", True, (255, 255, 255)), (37, 110))

        state.DISPLAY.blit(self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)), (37, 370))

        black_box_height = 130
        black_box_width = 700
        border_width = 5  # Width of the white border

        # Create the black box
        black_box = pygame.Surface((black_box_width, black_box_height))
        black_box.fill((0, 0, 0))  # Fill the box with black color

        # Create a white border
        white_border = pygame.Surface((black_box_width + 2 * border_width, black_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))  # Fill the border with white color
        white_border.blit(black_box, (border_width, border_width))

        # Determine the position of the white-bordered box
        screen_width, screen_height = state.DISPLAY.get_size()
        black_box_x = (screen_width - black_box_width) // 2 - border_width
        black_box_y = screen_height - black_box_height - 20 - border_width  # Subtract 20 pixels and adjust for border

        # Blit the white-bordered box onto the display
        state.DISPLAY.blit(white_border, (black_box_x, black_box_y))
        if self.game_state == "welcome_screen":
            print("welcome be update")


            self.battle_messages["welcome_message"].draw(state)
        pygame.display.flip()
        super().draw(state)

        # Draw the black square box in the middle of the screen
