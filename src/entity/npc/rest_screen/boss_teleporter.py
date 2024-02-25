import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class BossTeleporter(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["Hero: I need the boss key to pass through...Boss key? That was the name they came up with!?"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Do you want to go to the boss area? There is no turning back.  "],
                (50, 450, 700, 130), 36, 500),
            "watch_cut_scene_2_message": NpcTextBox(
                ["You need to watch both cut scenes from the bar, remeember your promise to sir Leopold, go grab a drink or a sandwhich."],
                (50, 450, 700, 130), 36, 500),
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.flipping_ted_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/Game Boy Advance - Breath of Fire - Doof.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if distance < 40 and state.controller.isTPressed and \
                (pygame.time.get_ticks() - self.state_start_time) > 500:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()
            # Reset the message depending on the game state
            if "boss key" in state.player.npc_items and state.restScreen.barscene2 == False:
                self.flipping_ted_messages["watch_cut_scene_2_message"].reset()
            elif "boss key" in state.player.npc_items and state.restScreen.barscene2 == True:
                self.flipping_ted_messages["defeated_message"].reset()

            else:
                self.flipping_ted_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        current_message = self.flipping_ted_messages["defeated_message"] if "boss key" in state.player.npc_items else self.flipping_ted_messages["welcome_message"]
        if state.restScreen.barscene2 == False and "boss key" in state.player.npc_items:
            current_message = self.flipping_ted_messages["watch_cut_scene_2_message"]
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False

        if "boss key" in state.player.npc_items and current_message.message_at_end():
            if state.controller.isUpPressed:
                state.controller.isUpPressed = False

                self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                print("Up pressed, arrow_index:", self.arrow_index)  # Debugging line

            elif state.controller.isDownPressed:
                state.controller.isDownPressed = False

                self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                print("Down pressed, arrow_index:", self.arrow_index)  # Debugging line

        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and state.controller.isTPressed and "boss key" in state.player.npc_items and state.restScreen.barscene2 == True and self.arrow_index == 0:
            state.rest_area_to_boss_area_entry_point = True

            state.currentScreen = state.bossScreen
            state.bossScreen.start(state)
            # Handle the selected option
            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # Check if the selected option is "Yes" and execute the code you provided




        if state.controller.isTPressed and current_message.is_finished():
            # Exiting the conversation
            self.state = "waiting"
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):

        # sprite_rect = pygame.Rect(5, 6, 24, 28)
        #
        # # Get the subsurface for the area you want
        # sprite = self.character_sprite_image.subsurface(sprite_rect)
        #
        # # Scale the subsurface to make it two times bigger
        # scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88
        #
        # # Define the position where you want to draw the sprite
        # sprite_x = self.collision.x + state.camera.x - 20
        # sprite_y = self.collision.y + state.camera.y - 10
        #
        # # Draw the scaled sprite portion on the display
        # state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            current_message = self.flipping_ted_messages["defeated_message"] if "boss key" in state.player.npc_items else self.flipping_ted_messages["welcome_message"]
            if state.restScreen.barscene2 == False and "boss key" in state.player.npc_items:
                current_message = self.flipping_ted_messages["watch_cut_scene_2_message"]

            current_message.draw(state)

            # Draw the "Yes/No" box only on the last message
            if current_message.message_at_end() and "boss key" in state.player.npc_items and state.restScreen.barscene2 == True:
                bet_box_width = 150
                bet_box_height = 100
                border_width = 5

                screen_width, screen_height = state.DISPLAY.get_size()
                bet_box_x = screen_width - bet_box_width - border_width - 48
                bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

                bet_box = pygame.Surface((bet_box_width, bet_box_height))
                bet_box.fill((0, 0, 0))
                white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
                white_border.fill((255, 255, 255))
                white_border.blit(bet_box, (border_width, border_width))

                # Calculate text positions
                text_x = bet_box_x + 50 + border_width
                text_y_yes = bet_box_y + 20
                text_y_no = text_y_yes + 40
                # Draw the box on the screen
                state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

                # Draw the text on the screen (over the box)
                state.DISPLAY.blit(self.font.render(f"Yes ", True, (255, 255, 255)), (text_x, text_y_yes))
                state.DISPLAY.blit(self.font.render(f"No ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
                arrow_x = text_x - 30  # Adjust the position of the arrow based on your preference
                arrow_y = text_y_yes + self.arrow_index * 40  # Adjust based on the item's height

                # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
                # Here's a simple example using a triangle:
                pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                    [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])
