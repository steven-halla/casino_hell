import math

from entity.treasurechests.treasurechests import TreasureChest
import pygame


class BlueFlower(TreasureChest):
    def __init__(self, x: float, y: float):
        # Pass the hidden item to the superclass constructor
        super().__init__(x, y, "Water Bottle")
        self.hidden_item = "blue flower"
        self.isOpened = False  # Define and initialize 'isOpened' attribute
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.treasure_open_sound = pygame.mixer.Sound("./assets/music/open_treasure.mp3")  # Adjust the path as needed
        self.treasure_open_sound.set_volume(0.5)

    def give_item(self, state: "GameState"):
        if state.controller.isTPressed:
            print("Hi there floewr")
            print(f"Received item: {self.hidden_item}")
            state.player.items.append(self.hidden_item)
            print("Your inventory so far: " + str(state.player.items))
            state.treasurechests.remove(self)  # Remove the chest from the game
            self.isOpened = True  #

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


