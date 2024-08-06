import math
import pygame

from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.treasurechests.treasurechests import TreasureChest
from game_constants.treasure import Treasure


class Area2MoneyBag(TreasureChest):
    def __init__(self, x: float, y: float):
        # Pass the hidden item to the superclass constructor
        super().__init__(x, y, "Water Bottle")
        self.hidden_item = 500
        self.isOpened = False  # Define and initialize 'isOpened' attribute
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.treasure_open_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/open_treasure.mp3")  # Adjust the path as needed
        self.treasure_open_sound.set_volume(0.5)
        self.message_displayed = False

        self.text_box = {
            "default_message": NpcTextBox(
                [
                    "Alex: I have  a simple quest for you: win 500 coins from the coin flip and oppossum in a can game in ONE SITTING",
                    "Hero: So no saving/resting of any sort in between?",
                    "Alex: Thats right ,so no cheating on this task, go big or go home....I really want to go home...I dont remember what my children look like",

                ],
                (50, 450, 50, 45), 30, 500
            ),

        }

    def give_item(self, state: "GameState"):
        if state.controller.isTPressed:
            state.player.money += self.hidden_item
            Treasure.add_treasure_to_player(state.player, Treasure.FIVE_HUNDRED_GOLD)
            state.treasurechests.remove(self)  # Remove the chest from the game
            self.isOpened = True
            print("Your level two npc state is :" + str(state.player.level_two_npc_state))
            self.message_displayed = True  # Set the flag to display the message

    def open_chest(self, state: "GameState"):
        # Implement the logic for opening the chest here
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)
            if distance < 40:
                print("Yo ho ho and a bottle of rum")
                self.give_item(state)  # Call the give_item method to add the item to the player's inventory
                self.treasure_open_sound.play()  # Play the sound effect once

    def update(self, state: "GameState"):

        if self.isOpened:
            print("nabba")

            self.text_box.update(state)
        else:
            self.open_chest(state)

    def draw_message(self, state: "GameState"):
        if self.isOpened:
            print("he he")

            self.text_box.draw(state)

