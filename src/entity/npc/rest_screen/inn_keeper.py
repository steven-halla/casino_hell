import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class InnKeeper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sleep_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/02WhiteMagic.wav")  # Adjust the path as needed
        self.sleep_sound.set_volume(0.3)
        self.selected_item_index = 0
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["Inn Keeper Neddry: Wanna stay at our inn and save your game?! Dont' mind the bed bugs, roaches, and rats,  they're very friendly.", "100 gold stay"],
                (50, 450, 700, 130), 36, 500),
            "low_money_message": NpcTextBox(
                ["Inn Keeper Neddry: I can let you sleep here but no saving, sorry don't want to brick your game You need to hold 400 coins min to save. ."],
                (50, 450, 700, 130), 36, 500),
            "rabies_message": NpcTextBox(
                ["I'll allow you to save your game, BUT YOU CANNOT SLEEP HERE, sorry."],
                (50, 450, 700, 130), 36, 500),
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Fisherman.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if distance < 70 and state.controller.isTPressed and \
                (pygame.time.get_ticks() - self.state_start_time) > 500:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()
            # Reset the message depending on the game state
            if state.player.hasRabies == True:
                self.flipping_ted_messages["rabies_message"].reset()
            elif state.player.money < 400:
                self.flipping_ted_messages["low_money_message"].reset()
            else:
                self.flipping_ted_messages["welcome_message"].reset()


    def update_talking(self, state: "GameState"):
        current_message = self.flipping_ted_messages["rabies_message"] if state.player.hasRabies == True else self.flipping_ted_messages["welcome_message"]
        if state.player.money < 400:
            current_message = self.flipping_ted_messages["low_money_message"]

        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False

        # Check for keypresses only once per frame
        if current_message.is_finished():

            if state.controller.isUpPressed:
                state.controller.isUpPressed = False

                self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                print("Up pressed, arrow_index:", self.arrow_index)  # Debugging line

            elif state.controller.isDownPressed:
                state.controller.isDownPressed = False
                self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                print("Down pressed, arrow_index:", self.arrow_index)

        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and state.controller.isTPressed:
            # Handle the selected option
            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # Check if the selected option is "Yes" and execute the code you provided
            if selected_option == "Yes":
                self.sleep_sound.play()  # Play the sound effect once

                state.player.money -= 100



                state.controller.isTPressed = False
                # This code should run regardless of the player's stamina
                self.state = "waiting"
                self.state_start_time = pygame.time.get_ticks()
                state.player.canMove = True
                print("Yes selected, closing shop.")
                self.arrow_index = 0
                state.player.days += 1
                if state.player.body > 0:
                    state.player.food = 1

                if state.player.hasRabies == False:
                    state.player.stamina_points += 500
                    if state.player.stamina_points > state.player.max_stamina_points:
                        state.player.stamina_points = state.player.max_stamina_points
                    state.player.focus_points += 500
                    if state.player.focus_points > state.player.max_focus_points:
                        state.player.focus_points = state.player.max_focus_points


                    print("Yes selected, closing shop.")
                    self.arrow_index = 0
                    self.state = "waiting"
                    self.state_start_time = pygame.time.get_ticks()
                    state.player.canMove = True
                    print("nice")
                    print(str(state.player.hasRabies))

                    if state.player.hasRabies == True:
                        print("Yee haawww")

                if state.player.money < 1:
                    state.currentScreen = state.gameOverScreen
                    state.gameOverScreen.start(state)

                if state.player.money > 399:
                    state.save_game(state.player, state)  # Call the save_game function

            # Call the save_game function

            # Reset the flag when the "T" key is released
            if not state.controller.isTPressed:
                # print("ya")
                self.t_pressed = False

        if state.controller.isTPressed and current_message.is_finished():

            self.arrow_index = 0

            # Exiting the conversation
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 21, 25)

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
            current_message = self.flipping_ted_messages["rabies_message"] if state.player.hasRabies == True else self.flipping_ted_messages["welcome_message"]
            if state.player.money < 400:
                current_message = self.flipping_ted_messages["low_money_message"]
            current_message.draw(state)

            # Draw the "Yes/No" box only on the last message
            if current_message.is_finished():
                bet_box_width = 150
                bet_box_height = 100
                border_width = 5

                screen_width, screen_height = state.DISPLAY.get_size()
                bet_box_x = screen_width - bet_box_width - border_width - 30
                bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

                bet_box = pygame.Surface((bet_box_width, bet_box_height))
                bet_box.fill((0, 0, 0))
                white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
                white_border.fill((255, 255, 255))
                white_border.blit(bet_box, (border_width, border_width))

                # Calculate text positions
                text_x = bet_box_x + 40 + border_width
                text_y_yes = bet_box_y + 20
                text_y_no = text_y_yes + 40
                # Draw the box on the screen
                state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

                # Draw the text on the screen (over the box)
                state.DISPLAY.blit(self.font.render(f"Yes ", True, (255, 255, 255)), (text_x, text_y_yes))
                state.DISPLAY.blit(self.font.render(f"No ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
                arrow_x = text_x - 40  # Adjust the position of the arrow based on your preference
                arrow_y = text_y_yes + self.arrow_index * 40  # Adjust based on the item's height

                # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
                # Here's a simple example using a triangle:
                pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                    [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])
