import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class NatNat(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.nelly_opossum_messages = {
            "welcome_message": NpcTextBox(
                ["Natalie: Hi there new guy, I swear to you my opossums are the sweetest things you ever did see. You can play with them for 150 coins."],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Natalie I didn't like playing with you anyway, hmmmp."],
                (50, 450, 700, 130), 36, 500),
            "money_message": NpcTextBox(
            ["Natalie Ewwwwww get away from me you poor bastard and get at least 150 coins, you disgust me!"],
            (50, 450, 700, 130), 36, 500),
            "rabies_message": NpcTextBox(
                ["Natalie Awwwww are you ok? Don't you worry your pretty little head I'll give you home, real soon like. Do you love garbage? Your gonna."],
                (50, 450, 700, 130), 36, 500),
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.nellyOpossumIsDefeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Nina.png").convert_alpha()



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


            # if state.player.hasRabies == True:
            #     self.nelly_opossum_messages["rabies_message"].reset()
            # elif state.opossumInACanNellyScreen.nellyOpossumIsDefeated:
            #     self.nelly_opossum_messages["defeated_message"].reset()
            # else:
            #     self.nelly_opossum_messages["welcome_message"].reset()

            if state.player.hasRabies == True:
                self.nelly_opossum_messages["rabies_message"].reset()
            elif state.player.money < 150:
                self.nelly_opossum_messages["money_message"].reset()
            elif state.opossumInACanNellyScreen.nellyOpossumIsDefeated:
                self.nelly_opossum_messages["defeated_message"].reset()
            else:
                self.nelly_opossum_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        # current_message = self.nelly_opossum_messages["defeated_message"] if state.opossumInACanNellyScreen.nellyOpossumIsDefeated else self.nelly_opossum_messages["welcome_message"]
        current_message = (
            self.nelly_opossum_messages["rabies_message"]
            if state.player.hasRabies
            else (
                self.nelly_opossum_messages["money_message"]
                if state.player.money < 150
                else (
                    self.nelly_opossum_messages["defeated_message"]
                    if state.opossumInACanNellyScreen.nellyOpossumIsDefeated
                    else (
                        self.nelly_opossum_messages["no_play_message"]
                        if state.player.money < 150
                        else self.nelly_opossum_messages["welcome_message"]
                    )
                )
            )
        )
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False

        # Check for keypresses only once per frame
        if current_message.is_finished() and current_message.message_at_end():

            if state.controller.isUpPressed:
                self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                state.controller.isUpPressed = False

            elif state.controller.isDownPressed:
                self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                state.controller.isDownPressed = False

        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and state.controller.isTPressed and state.opossumInACanNellyScreen.nellyOpossumIsDefeated == False and state.player.hasRabies == False and state.player.money > 149:
            # Handle the selected option
            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # need to add a check here for the item work
            ##
            ##
            ##look above its imoprtant !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if selected_option == "Yes":
                state.currentScreen = state.opossumInACanNellyScreen
                state.opossumInACanNellyScreen.start(state)

            # Reset the flag when the "T" key is released
            if not state.controller.isTPressed:
                self.t_pressed = False

        if state.controller.isTPressed and current_message.is_finished():
            state.controller.isTPressed = False
            # Exiting the conversation
            self.state = "waiting"
            self.menu_index = 0
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):

        sprite_rect = pygame.Rect(147, 6, 18.6, 24)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            # current_message = self.nelly_opossum_messages["defeated_message"] if state.opossumInACanNellyScreen.nellyOpossumIsDefeated else self.nelly_opossum_messages["welcome_message"]
            current_message = (
                self.nelly_opossum_messages["rabies_message"]
                if state.player.hasRabies
                else (
                    self.nelly_opossum_messages["defeated_message"]
                    if state.opossumInACanNellyScreen.nellyOpossumIsDefeated
                    else (
                        self.nelly_opossum_messages["money_message"]
                        if state.player.money < 150
                        else self.nelly_opossum_messages["welcome_message"]
                    )
                )
            )
            current_message.draw(state)

            # Draw the "Yes/No" box only on the last message
            if current_message.is_finished()and current_message.message_at_end() and state.opossumInACanNellyScreen.nellyOpossumIsDefeated == False and state.player.hasRabies == False and state.player.money > 149:
                # print("better not see this shit")
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
