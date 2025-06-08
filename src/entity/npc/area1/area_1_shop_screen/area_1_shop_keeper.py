import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class Area1ShopKeeper(Npc):
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
        self.shop_items = [Equipment.BLACK_JACK_HAT.value, Equipment.OPOSSUM_REPELLENT.value, Magic.REVEAL.value, Events.LEVEL_1_BOSS_KEY.value ]

        self.shop_costs = ["500", "500", "500", "1000"]

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

            if Equipment.BLACK_JACK_HAT.value in state.player.items:
                self.shop_items[0] = "sold out"

            if Equipment.OPOSSUM_REPELLENT.value in state.player.items:
                self.shop_items[1] = "sold out"

            if Magic.REVEAL.value in state.player.magicinventory:
                self.shop_items[2] = "sold out"

            if Events.LEVEL_1_BOSS_KEY.value in state.player.level_one_npc_state:
                self.shop_items[3] = "sold out"





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
                        cost = 500
                        if state.player.money - cost < 800 or Equipment.BLACK_JACK_HAT.value in state.player.level_one_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.BLACK_JACK_HAT.add_equipment_to_player_level_1(state.player,
                                                                                        Equipment.BLACK_JACK_HAT)
                            state.player.money -= cost

                    elif self.selected_item_index == 1:
                        cost = 500
                        if state.player.money - cost < 800 or Equipment.OPOSSUM_REPELLENT.value in state.player.level_one_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.OPOSSUM_REPELLENT.add_equipment_to_player_level_1(state.player, Equipment.OPOSSUM_REPELLENT)
                            state.player.money -= cost

                    elif self.selected_item_index == 2:
                        cost = 500
                        if state.player.money - cost < 800 or Magic.REVEAL.value in state.player.magicinventory:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            state.player.magicinventory.append(Magic.REVEAL.value)
                            state.player.money -= cost

                    elif self.selected_item_index == 3:
                        cost = 1000
                        if state.player.money < cost or Events.LEVEL_1_BOSS_KEY.value in state.player.level_one_npc_state or state.player.perception != 1 or state.player.body != 1 or state.player.spirit != 1:
                            self.cant_buy_sound.play()
                        else:
                            state.player.quest_items.append(Events.LEVEL_1_BOSS_KEY.value)

                            self.buy_sound.play()
                            Events.add_level_one_event_to_player(state.player, Events.LEVEL_1_BOSS_KEY)
                            state.player.money -= cost





                # else:
                #     print("dsjfl;dsjlafj;jflsajf;j;fja;fkjsda;fjls;ajfl;sjafl;sjal;fjasl;jf;asjf;ls")
                #     self.cant_buy_sound.play()  # Play the sound effect once

                # else:
                    #     print("dsjfl;dsjlafj;jflsajf;j;fja;fkjsda;fjls;ajfl;sjafl;sjal;fjasl;jf;asjf;ls")
                    #     self.cant_buy_sound.play()  # Play the sound effect once





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
            if self.state == "talking":

                if self.selected_item_index == 0 and Equipment.BLACK_JACK_HAT.value not in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Protects from busts in Black Jack.", True,
                                                        (255, 255, 255)), (70, 460))
                    state.DISPLAY.blit(self.font.render(f"A stylish hat that brings luck to card games.", True,
                                                        (255, 255, 255)), (70, 510))
                if self.selected_item_index == 0 and Equipment.BLACK_JACK_HAT.value in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Black Hat is Sold out!", True,
                                                        (255, 255, 255)), (70, 460))



                if self.selected_item_index == 1 and Equipment.OPOSSUM_REPELLENT.value not in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"More spirit = more damage reduction", True,
                                                        (255, 255, 255)), (70, 460))


                    state.DISPLAY.blit(self.font.render(f"Keeps those pesky opossums at bay.", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 1 and Equipment.OPOSSUM_REPELLENT.value in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Opossum Repellent is sold out!", True,
                                                        (255, 255, 255)), (70, 460))



                if self.selected_item_index == 2 and Magic.REVEAL.value not in state.player.magicinventory:
                    state.DISPLAY.blit(self.font.render(f"Shows how many points enemy has in card games.", True,
                                                        (255, 255, 255)), (70, 460))


                    state.DISPLAY.blit(self.font.render(f"A magical spell that reveals hidden information.", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 2 and Magic.REVEAL.value in state.player.magicinventory:
                    state.DISPLAY.blit(self.font.render(f"Reveal spell is sold out!", True,
                                                        (255, 255, 255)), (70, 460))

                if self.selected_item_index == 3 and Events.LEVEL_1_BOSS_KEY.value not in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Requires perception=1, body=1, spirit=1", True,
                                                        (255, 255, 255)), (70, 460))
                    state.DISPLAY.blit(self.font.render(f"A key that unlocks the path to the boss.", True,
                                                        (255, 255, 255)), (70, 510))
                elif self.selected_item_index == 3 and Events.LEVEL_1_BOSS_KEY.value in state.player.level_one_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Boss key is sold out!", True,
                                                        (255, 255, 255)), (70, 460))



                if self.stat_point_increase == True:
                    # Draw a box on the far right end of the screen, 260 pixels wide and 260 pixels high
                    box_width = 260
                    box_height = 260
                    border_width = 5
                    start_x = state.DISPLAY.get_width() - box_width - 25  # Far right of the screen
                    start_y = state.DISPLAY.get_height() // 2 - box_height // 2 + 10  # Centered vertically

                    # Create the black box
                    black_box = pygame.Surface((box_width, box_height))
                    black_box.fill((0, 0, 0))

                    # Create a white border
                    white_border = pygame.Surface(
                        (box_width + 2 * border_width, box_height + 2 * border_width)
                    )
                    white_border.fill((255, 255, 255))
                    white_border.blit(black_box, (border_width, border_width))

                    # Draw the box on the far right
                    state.DISPLAY.blit(white_border, (start_x - border_width, start_y - border_width))

                    # Draw the label for maximum stat value
                    state.DISPLAY.blit(self.font.render("Max Value 2:", True, (255, 255, 255)), (start_x + 10, start_y + 20))

                    # Define the list of stats and the vertical position for each
                    stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
                    stat_values = [
                        state.player.body,
                        state.player.mind,
                        state.player.spirit,
                        state.player.perception - 1 if Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items else state.player.perception,
                        state.player.luck - 1 if state.player.enhanced_luck else state.player.luck,
                    ]

                    # Display the stats names
                    for idx, stat in enumerate(stats):
                        y_position = start_y + 60 + idx * 40  # Adjust vertical spacing
                        state.DISPLAY.blit(self.font.render(stat, True, (255, 255, 255)), (start_x + 60, y_position))

                    # Display the player's current stat values 30 pixels to the right of the stat names
                    for idx, stat_value in enumerate(stat_values):
                        y_position = start_y + 60 + idx * 40  # Adjust vertical spacing
                        state.DISPLAY.blit(self.font.render(str(stat_value), True, (255, 255, 255)), (start_x + 200, y_position))

                    # Draw the arrow next to the currently selected stat based on stat_point_increase_index
                    arrow_y_positions = [60, 100, 140, 180, 220]  # Y positions for the arrow, matching the stats' Y positions
                    arrow_x = start_x + 20  # X position for the arrow
                    arrow_y = start_y + arrow_y_positions[self.stat_point_increase_index]

                    # Draw the arrow ('->') at the current stat's position
                    state.DISPLAY.blit(self.font.render("->", True, (255, 255, 255)), (arrow_x, arrow_y))
