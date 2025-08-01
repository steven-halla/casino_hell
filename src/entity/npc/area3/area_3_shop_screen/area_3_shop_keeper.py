import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class Area3ShopKeeper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("./assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("./assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)

        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)


        self.textbox = ShopNpcTextBox(
            [
             ""],
            (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = [Equipment.COIN_SAVE_AREA_3.value , Equipment.LUCKY_ROTTEN_SOCKS.value, Equipment.SPIRIT_SHOES.value, Magic.HEADS_FORCE.value, Magic.BLACK_JACK_REDRAW.value, Magic.BAD_LUCK.value, Equipment.LEVEL_3_BOSS_KEY.value]

        self.shop_costs = ["1200", "1000", "1000","1000", "1000", "1000","1500"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index
        self.stat_point_increase = False
        self.stat_point_increase_index = 0
        self.index_1_bought = False

        self.in_shop = False

    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):


        if self.state == "waiting":
            self.update_waiting(state)
            # state.player.canMove = True
        elif self.state == "talking":

            state.player.hide_player = True

            if Equipment.COIN_SAVE_AREA_3.value in state.player.level_three_npc_state:
                self.shop_items[0] = "sold out"

            if Equipment.LUCKY_ROTTEN_SOCKS.value in state.player.level_three_npc_state:
                self.shop_items[1] = "sold out"

            if Equipment.SLOTS_SHOES.value in state.player.level_three_npc_state:
                self.shop_items[2] = "sold out"

            if Magic.HEADS_FORCE.value in state.player.magicinventory:
                self.shop_items[3] = "sold out"

            if Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                self.shop_items[4] = "sold out"

            if Magic.BAD_LUCK.value in state.player.magicinventory:
                self.shop_items[5] = "sold out"
            if Equipment.LEVEL_3_BOSS_KEY.value in state.player.level_three_npc_state:
                self.shop_items[6] = "sold out"



            cost = int(self.shop_costs[self.selected_item_index])


            if (state.controller.isBPressed or state.controller.isBPressedSwitch) and pygame.time.get_ticks() - self.input_time > 500 and self.stat_point_increase == False:
                self.input_time = pygame.time.get_ticks()
                self.state = "waiting"
                print("Leaving the shop...")
                self.textbox.reset()
                self.stat_point_increase = False
                self.in_shop = False
                state.player.canMove = True


            if self.textbox.message_index == 0 and self.textbox.is_finished():

                if state.controller.confirm_button:

                    # For each shop item, define its cost and check the new minimum condition.
                    if self.selected_item_index == 0:
                        print("Yes")
                        cost = 1200
                        if state.player.money - cost < 500 or Equipment.COIN_SAVE_AREA_3.value in state.player.level_three_npc_state:
                            self.cant_buy_sound.play()  # Not enough money left or already purchased
                        else:
                            self.buy_sound.play()
                            if state.player.enhanced_luck:
                                state.player.luck -= 1
                            Equipment.add_shop_items_to_player_inventory(state.player, Equipment.COIN_SAVE_AREA_3)
                            state.player.money -= cost
                            state.save_game(state.player, state)
                            if state.player.enhanced_luck:
                                state.player.luck += 1

                    elif self.selected_item_index == 1:
                        cost = 1000
                        if state.player.money - cost < 500 or Equipment.LUCKY_ROTTEN_SOCKS.value in state.player.level_three_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player_level_3(state.player, Equipment.LUCKY_ROTTEN_SOCKS)
                            state.player.money -= cost

                    elif self.selected_item_index == 2:
                        cost = 1000
                        if state.player.money - cost < 500 or Equipment.SPIRIT_SHOES.value in state.player.level_three_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player_level_3(state.player, Equipment.SPIRIT_SHOES)
                            state.player.money -= cost

                    elif self.selected_item_index == 3:
                        cost = 1000
                        if state.player.money - cost < 500 or Magic.HEADS_FORCE.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Magic.add_magic_to_player(state.player, Magic.HEADS_FORCE)
                            state.player.money -= cost
                            self.stat_point_increase = True

                    elif self.selected_item_index == 4:
                        cost = 1000
                        if state.player.money - cost < 500 or Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Magic.add_magic_to_player(state.player, Magic.BLACK_JACK_REDRAW)
                            state.player.money -= cost

                    elif self.selected_item_index == 5:
                        cost = 1000
                        if state.player.money - cost < 500 or Magic.BAD_LUCK.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Magic.add_magic_to_player(state.player, Magic.BAD_LUCK)
                            state.player.money -= cost

                    elif self.selected_item_index == 6:
                        cost = 1500
                        if state.player.money - cost < 500 or Equipment.LEVEL_3_BOSS_KEY.value in state.player.level_three_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player_level_3(state.player, Equipment.LEVEL_3_BOSS_KEY)
                            state.player.money -= cost





                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400 and self.stat_point_increase == False:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()  # Play the sound effect once

                    # Decrement the index but prevent it from going below 0
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                        self.selected_money_index -= 1
                    print(f"shop_items: {self.shop_items}")
                    print(f"shop_costs: {self.shop_costs}")
                    print(f"selected_item_index: {self.selected_item_index}")
                    print(f"selected_money_index: {self.selected_money_index}")

                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400 and self.stat_point_increase == False:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()  # Play the sound effect once

                    # Increment the index but prevent it from exceeding the length of the list - 1
                    if self.selected_item_index < len(self.shop_items) - 1:
                        self.selected_item_index += 1
                        self.selected_money_index += 1
                    print(f"shop_items: {self.shop_items}")
                    print(f"shop_costs: {self.shop_costs}")
                    print(f"selected_item_index: {self.selected_item_index}")
                    print(f"selected_money_index: {self.selected_money_index}")


            self.update_talking(state)

    def sold_out(self, item_index: int):
        # Mark the item as sold out
        self.shop_items[item_index] = "sold out"

    def update_waiting(self, state: "GameState"):
        player = state.player

        player.hide_player = False

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500 and state.player.menu_paused == False:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 100 :
                state.controller.isTPressed = False
                # print("start state: talking")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                self.textbox.reset()

    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)

        # If 'B' is pressed, exit the conversation and allow movement
        if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
            self.input_time = pygame.time.get_ticks()
            self.state = "waiting"  # Switch to 'waiting' state
            state.player.canMove = True  # Explicitly set canMove to True when leaving conversation
            self.textbox.reset()  # Reset the textbox
            return

        # If 'T' is pressed and the conversation is finished, exit and allow movement
        if state.controller.isTPressed and self.textbox.is_finished():
            state.controller.isTPressed = False
            self.state = "waiting"  # Switch to 'waiting' state
            state.player.canMove = True  # Explicitly set canMove to True after finishing conversation
            self.textbox.reset()
            return

        # During the conversation, prevent movement
        if self.state == "talking":
            state.player.canMove = False

        # If already in 'waiting' state, ensure player can move
        if self.state == "waiting":
            state.player.canMove = True

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 18, 25)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            self.textbox.draw(state)

            if self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_3.value not in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"There is only 1 of these on this floor so use it wisely.", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"Saves your game.", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_3.value in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Save Coin is Sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 1 and Equipment.LUCKY_ROTTEN_SOCKS.value not in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Increases chance of winning at battle dice", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"For battle dice", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 1 and Equipment.LUCKY_ROTTEN_SOCKS.value in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Lucky rotten socks socks is sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 2 and Equipment.SPIRIT_SHOES.value not in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Adds +1 to spirit", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"The earlier you buy this the better.", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 2 and Equipment.SPIRIT_SHOES.value in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Spirit Shoes are sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 3 and Magic.HEADS_FORCE.value not in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Force Heads", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"Forces coin flips to be heads", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 3 and Magic.HEADS_FORCE.value in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Force Heads is sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 4 and Magic.BLACK_JACK_REDRAW.value not in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Allows you to redraw once in Black Jack.", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"Very useful for difficult hands.", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 4 and Magic.BLACK_JACK_REDRAW.value in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Black Jack Redraw is sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 5 and Magic.BAD_LUCK.value not in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Affects enemy attack rolls in dice fighter.", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"A good investment for tough battles.", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 5 and Magic.BAD_LUCK.value in state.player.magicinventory:
                state.DISPLAY.blit(self.font.render(f"Bad Luck is sold out!", True,
                                                    (255, 255, 255)), (70, 460))

            if self.selected_item_index == 6 and Equipment.LEVEL_3_BOSS_KEY.value not in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Unlocks the path to the boss.", True,
                                                    (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render(f"Required to progress to the next level.", True,
                                                    (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 6 and Equipment.LEVEL_3_BOSS_KEY.value in state.player.level_three_npc_state:
                state.DISPLAY.blit(self.font.render(f"Boss Key is sold out!", True,
                                                    (255, 255, 255)), (70, 460))
