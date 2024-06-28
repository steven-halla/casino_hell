import pygame
import random
from entity.gui.screen.battle_screen import BattleScreen
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen

class SlotsRibDemonJackRipperScreen(Screen):
    def __init__(self) -> None:
        super().__init__("Casino Slots Screen")

        self.slot1: list[int] = [random.randint(0, 9) for _ in range(3)]
        self.slot2: list[int] = [random.randint(0, 9) for _ in range(3)]
        self.slot3: list[int] = [random.randint(0, 9) for _ in range(3)]
        self.slot_positions1: list[int] = [-50, 0, 50]
        self.slot_positions2: list[int] = [-50, 0, 50]
        self.slot_positions3: list[int] = [-50, 0, 50]
        self.last_update_time: int = pygame.time.get_ticks()
        self.spin_delay: int = 44
        self.spinning: bool = False
        self.stopping: bool = False
        self.stop_start_time: int = 0
        self.stopping_first: bool = False
        self.stopping_second: bool = False

        self.go_to_results = False

        self.new_font: pygame.font.Font = pygame.font.Font(None, 36)
        self.game_state: str = "welcome_screen"
        self.bet: int = 0
        self.money: int = 1000
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.battle_messages: dict[str, TextBox] = {
            "welcome_message": TextBox(
                ["Are you here for some rib demon slots?", ""],
                (65, 460, 700, 130),
                36,
                500
            ),
            "spin_message": TextBox(
                ["Press the A key in order to Spin"],
                (65, 460, 700, 130),
                36,
                500
            ),

            "results_message": TextBox(
                ["Your spin is {0} {1} {2}", ""],
                (65, 460, 700, 130),
                36,
                500
            ),

        }

        self.hide_numbers: bool = True

    def print_current_slots(self) -> None:
        visible_slots = [self.slot1[0], self.slot2[0], self.slot3[0]]
        print(f"Current Slots: {visible_slots}")

    def update(self, state: "GameState") -> None:
        current_time: int = pygame.time.get_ticks()

        if self.spinning:
            if current_time - self.last_update_time > self.spin_delay:
                self.last_update_time = current_time
                for i in range(3):
                    if not self.stopping_first:
                        self.slot_positions1[i] += 10
                        if self.slot_positions1[i] >= 100:
                            self.slot_positions1[i] = -50
                            self.slot1[i] = random.randint(0, 9)
                    if not self.stopping_second:
                        self.slot_positions2[i] += 10
                        if self.slot_positions2[i] >= 100:
                            self.slot_positions2[i] = -50
                            self.slot2[i] = random.randint(0, 9)
                    self.slot_positions3[i] += 10
                    if self.slot_positions3[i] >= 100:
                        self.slot_positions3[i] = -50
                        self.slot3[i] = random.randint(0, 9)

            if self.stopping:
                if not self.stopping_first:
                    if current_time - self.stop_start_time >= 2000:
                        self.stopping_first = True
                        self.slot_positions1 = [0, 50, 100]
                elif not self.stopping_second:
                    if current_time - self.stop_start_time >= 3500:
                        self.stopping_second = True
                        self.slot_positions2 = [0, 50, 100]
                elif current_time - self.stop_start_time >= 5000:
                    self.spinning = False
                    self.stopping = False
                    print("Spinning stopped.")
                    self.slot_positions3 = [0, 50, 100]
                    self.print_current_slots()
                    self.go_to_results = True


        if state.controller.isQPressed:
            state.currentScreen = state.mainScreen
            state.mainScreen.start(state)
            return

        if state.controller.isAPressed and self.game_state == "spin_screen" and not self.a_key_pressed:
            self.a_key_pressed = True
            if not self.spinning:
                self.spinning = True
                self.stopping = False
                self.stopping_first = False
                self.stopping_second = False
                self.spin_delay = 70
                print("Spinning started.")
            else:
                self.stopping = True
                self.stop_start_time = current_time
                print("Stopping initiated.")

        if not state.controller.isAPressed:
            self.a_key_pressed = False

        if state.controller.isBPressed:
            self.hide_numbers = not self.hide_numbers



        controller = state.controller
        controller.update()

        if self.game_state == "welcome_screen":
            print("Hi welcome screen")
            self.go_to_results = False

            self.battle_messages["welcome_message"].update(state)

        if self.battle_messages["welcome_message"].message_index == 1:
            self.game_state = "spin_screen"

        if self.game_state == "spin_screen":
            self.battle_messages["spin_message"].update(state)
            if self.go_to_results == True:
                print("resultes here we go")
                self.game_state = "results_screen"

        if self.game_state == "results_screen":
            print("results")
            self.battle_messages["results_message"].text = [
                f"Your spin is {self.slot1[0]} {self.slot2[0]} {self.slot3[0]}",
                ""
            ]
            self.battle_messages["results_message"].update(state)

            if self.battle_messages["results_message"].message_index == 1:
                self.battle_messages["welcome_message"].reset()
                self.battle_messages["results_message"].reset()
                self.game_state = "welcome_screen"

    def draw(self, state: "GameState") -> None:
        state.DISPLAY.fill((0, 0, 51))

        self.draw_hero_info_boxes(state)
        self.draw_grid_box(state)

        if self.hide_numbers:
            self.draw_mask_box(state)

        self.draw_bottom_black_box(state)

        if self.game_state == "welcome_screen":
            self.battle_messages["welcome_message"].draw(state)
        elif self.game_state == "spin_screen":
            self.battle_messages["spin_message"].draw(state)
        elif self.game_state == "results_screen":
            self.battle_messages["results_message"].draw(state)

        pygame.display.flip()

    def draw_grid_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_size = 50
        line_thickness = 2
        start_x1 = (screen_width - box_size * 3 - line_thickness * 2) // 2  # Adjust for three columns
        start_y = (screen_height - box_size) // 2
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)

        font = pygame.font.Font(None, 36)

        # Draw first column
        for i, pos in enumerate(self.slot_positions1):
            box_x = start_x1
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot1[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw second column
        for i, pos in enumerate(self.slot_positions2):
            box_x = start_x1 + box_size + line_thickness
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot2[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw third column
        for i, pos in enumerate(self.slot_positions3):
            box_x = start_x1 + (box_size + line_thickness) * 2
            box_y = start_y + pos
            pygame.draw.rect(state.DISPLAY, black_color, (box_x, box_y, box_size, box_size))
            number_text = font.render(str(self.slot3[i]), True, white_color)
            text_rect = number_text.get_rect(center=(box_x + box_size // 2, box_y + box_size // 2))
            state.DISPLAY.blit(number_text, text_rect)

        # Draw the white lines
        for start_x in [start_x1, start_x1 + box_size + line_thickness, start_x1 + (box_size + line_thickness) * 2]:
            y = start_y - line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + box_size, y), line_thickness)
            y = start_y + box_size + line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (start_x, y), (start_x + box_size, y), line_thickness)
            x = start_x - line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (x, start_y), (x, start_y + box_size), line_thickness)
            x = start_x + box_size + line_thickness // 2
            pygame.draw.line(state.DISPLAY, white_color, (x, start_y), (x, start_y + box_size), line_thickness)

    def draw_hero_info_boxes(self, state: "GameState") -> None:
        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

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

        self.draw_enemy_info_box(state)

    def draw_enemy_info_box(self, state: "GameState") -> None:
        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface((200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        state.DISPLAY.blit(self.font.render("Enemy", True, (255, 255, 255)), (37, 33))

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

    def draw_mask_box(self, state: "GameState") -> None:
        screen_width, screen_height = state.DISPLAY.get_size()
        box_size = 50
        line_thickness = 2
        total_grid_width = box_size * 3 + line_thickness * 2
        start_x = (screen_width - total_grid_width) // 2
        start_y = (screen_height - box_size) // 2

        mask_box_top = pygame.Surface((total_grid_width, start_y))
        mask_box_bottom = pygame.Surface((total_grid_width, screen_height - (start_y + box_size)))
        mask_box_top.fill((0, 0, 51))
        mask_box_bottom.fill((0, 0, 51))

        state.DISPLAY.blit(mask_box_top, (start_x, 0))
        state.DISPLAY.blit(mask_box_bottom, (start_x, start_y + box_size + line_thickness))

    def draw_bottom_black_box(self, state: "GameState") -> None:
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
