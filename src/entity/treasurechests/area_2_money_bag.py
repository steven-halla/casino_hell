import math
import pygame

from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.treasurechests.treasurechests import TreasureChest
from game_constants.treasure import Treasure

# this item is hidden reward for having a 2 perception
class Area2MoneyBag(TreasureChest):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, "Water Bottle")
        self.hidden_item = 500
        self.isOpened = False
        self.state_start_time = pygame.time.get_ticks()
        self.treasure_open_sound = pygame.mixer.Sound("./assets/music/open_treasure.mp3")
        self.treasure_open_sound.set_volume(0.5)
        self.message_displayed = False
        self.message_closed = False
        self.remove = False  # Flag to mark the chest for removal


        self.text_box_messages = {
            "default_message": NpcTextBox(
                [f"You have received {self.hidden_item} gold!"],
                (50, 450, 50, 45), 30, 500
            )
        }
        self.current_message = self.text_box_messages["default_message"]

    def give_item(self, state: "GameState"):
        state.player.money += self.hidden_item
        Treasure.add_treasure_to_player(state.player, Treasure.FIVE_HUNDRED_GOLD)
        self.isOpened = True
        self.message_displayed = True
        self.current_message.reset()
        self.treasure_open_sound.play()
        print("Your level two npc state is :" + str(state.player.level_two_npc_state))

    def open_chest(self, state: "GameState"):
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)
            if distance < 40:
                print("Yo ho ho and a bottle of rum")
                self.give_item(state)

    def update(self, state: "GameState"):
        if self.message_closed:
            self.remove = True  # Mark the chest for removal
            return  # Do nothing if the message has been closed
        if self.isOpened:
            self.current_message.update(state)
            state.player.canMove = False
            if state.controller.isTPressed and self.current_message.message_at_end():
                self.message_closed = True  # Set the flag to indicate the message is closed
                state.player.canMove = True
        else:
            self.open_chest(state)

    def draw(self, state: "GameState"):
        if not self.isOpened:
            super().draw(state)
        if self.isOpened and not self.message_closed:  # Check if the message is displayed and not closed
            self.current_message.draw(state)
