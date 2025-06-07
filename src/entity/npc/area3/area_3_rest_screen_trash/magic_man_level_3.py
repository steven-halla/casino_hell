import math
import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class MagicManLevel3(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("./assets/music/BFBuyingSelling.wav")
        self.buy_sound.set_volume(0.3)
        self.cant_buy_sound = pygame.mixer.Sound("./assets/music/cantbuy3.wav")
        self.cant_buy_sound.set_volume(0.5)
        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")
        self.menu_movement_sound.set_volume(0.2)

        # Textbox used for the shop items
        self.textbox = ShopNpcTextBox([""], (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()
        self.input_time = pygame.time.get_ticks()
        self.magic_man_level_3_vanished = False

        # Message textboxes for welcome and defeated messages.
        self.messages = {
            "welcome": NpcTextBox(
                ["Magic Man: I will let you buy 1 magic spell?"],
                (50, 450, 700, 130), 36, 500
            ),
            "defeated": NpcTextBox(
                ["Magic Man: Thank you for your purchase, if you make it to level 4 come see me."],
                (50, 450, 700, 130), 36, 500
            )
        }

        # Possible states: waiting, welcome, shop, defeated, vanished.
        self.state = "waiting"

        # Shop items and costs.
        self.shop_items = [Magic.BLACK_JACK_REDRAW.value, Magic.PEEK.value]
        self.shop_costs = ["3000", "3000"]
        self.selected_item_index = 0
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0

        # Flag to indicate a purchase was made.
        self.purchase_made = False

        self.in_shop = False

    def show_shop(self, state: "GameState"):
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True

    def update(self, state: "GameState"):
        current_time = pygame.time.get_ticks()

        # Set player's visibility and movement based on current NPC state.
        if self.state in ["welcome", "shop", "defeated"]:
            state.player.canMove = False
        elif self.state == "waiting":
            state.player.canMove = True

        if self.state == "waiting":

            # Wait until the player presses T to start conversation.
            if state.controller.isTPressed and (current_time - self.state_start_time) > 500 and not state.player.menu_paused:
                state.controller.isTPressed = False
                state.player.hide_player = True

                self.state = "welcome"
                self.messages["welcome"].reset()  # Reset the welcome message textbox.
                self.state_start_time = current_time

        elif self.state == "welcome":
            # Update the welcome message.
            self.messages["welcome"].update(state)
            # When the welcome message is finished and the confirm button is pressed, switch to shop.
            if self.messages["welcome"].is_finished() and state.controller.confirm_button:
                self.textbox.reset()
                self.show_shop(state)
                self.state = "shop"
                self.state_start_time = current_time

        elif self.state == "shop":
            state.player.hide_player = True

            self.textbox.update(state)
            # Shop navigation.
            if state.controller.isUpPressed and (current_time - self.input_time) > 400:
                self.input_time = current_time
                self.menu_movement_sound.play()
                if self.selected_item_index > 0:
                    self.selected_item_index -= 1
                    self.selected_money_index -= 1
            elif state.controller.isDownPressed and (current_time - self.input_time) > 400:
                self.input_time = current_time
                self.menu_movement_sound.play()
                if self.selected_item_index < len(self.shop_items) - 1:
                    self.selected_item_index += 1
                    self.selected_money_index += 1

            # Exit shop with the B button.
            if (state.controller.isBPressed or state.controller.isBPressedSwitch) and (current_time - self.input_time) > 500:
                self.input_time = current_time
                self.state = "waiting"
                self.textbox.reset()
                state.player.canMove = True
                self.state_start_time = current_time

            # Process a purchase if the shop textbox is finished and confirm button is pressed.
            if self.textbox.message_index == 0 and self.textbox.is_finished():
                if state.controller.confirm_button:
                    # Do not modify confirm_button since it is read-only.
                    if self.selected_item_index == 0:
                        cost = 3000
                        if state.player.money - cost < 500 or Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Magic.BLACK_JACK_REDRAW.add_magic_to_player(state.player, Magic.BLACK_JACK_REDRAW)
                            state.player.money -= cost
                            self.purchase_made = True
                    elif self.selected_item_index == 1:
                        cost = 3000
                        if state.player.money - cost < 500 or Magic.PEEK.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Magic.PEEK.add_magic_to_player(state.player, Magic.PEEK)
                            state.player.money -= cost
                            self.purchase_made = True

                    # After a successful purchase, switch to the defeated message state.
                    if self.purchase_made:
                        self.messages["defeated"].reset()
                        self.state = "defeated"
                        self.state_start_time = current_time

        elif self.state == "defeated":
            self.messages["defeated"].update(state)
            # When the defeated message is finished and the confirm button is pressed, vanish the NPC.
            if self.messages["defeated"].is_finished() and state.controller.confirm_button:
                self.state = "vanished"
                state.player.canMove = True
                state.player.level_three_npc_state.append("magic_man_level_3_vanished")

                self.state_start_time = current_time

        elif self.state == "vanished":
            # In the vanished state, the NPC is effectively removed from the game.
            pass

    def draw(self, state):
        # Only draw the NPC if it hasn't vanished.
        if self.state != "vanished":
            sprite_rect = pygame.Rect(5, 6, 18, 25)
            sprite = self.character_sprite_image.subsurface(sprite_rect)
            scaled_sprite = pygame.transform.scale(sprite, (50, 50))
            sprite_x = self.collision.x + state.camera.x - 20
            sprite_y = self.collision.y + state.camera.y - 10
            state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the active textbox.
        if self.state == "welcome":
            self.messages["welcome"].draw(state)
        elif self.state == "shop":
            self.textbox.draw(state)
        elif self.state == "defeated":
            self.messages["defeated"].draw(state)