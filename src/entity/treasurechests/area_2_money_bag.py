import math

from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.treasurechests.treasurechests import TreasureChest
import pygame

from game_constants.events import Events
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


        self.text_box = NpcTextBox(
            messages=[f"You have received {self.hidden_item} gold!"],
            rect=(50, 450, 50, 45),
            font_size=30,
            delay=100
        )

    def give_item(self, state: "GameState"):
        if state.controller.isTPressed:
            state.player.money += self.hidden_item
            Treasure.add_treasure_to_player(state.player, Treasure.FIVE_HUNDRED_GOLD)


            state.treasurechests.remove(self)  # Remove the chest from the game
            self.isOpened = True  #
            print("YOur level two npc state is :" + str(state.player.level_two_npc_state))
            self.text_box.reset()  # Reset the text box to start displaying the message






    def open_chest(self, state: "GameState"):
        # Implement the logic for opening the chest here
        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (state.player.collision.x - self.collision.x) ** 2 + (
                        state.player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 40:
                print("Yo ho ho and a bottle of bum")
                self.give_item(state)  # Call the give_item method to add the item to the player's inventory
                self.treasure_open_sound.play()  # Play the sound effect once



    def update(self, state: "GameState"):
        if self.message_displayed:
            self.text_box.update(state)
        else:
            self.open_chest(state)

    def draw2(self, state: "GameState"):
        if self.message_displayed:
            self.text_box.draw(state)

