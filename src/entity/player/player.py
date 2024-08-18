import json
from typing import Tuple

import pygame

from constants import TILE_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT, BLUEBLACK
from entity.entity import Entity
from game_constants.treasure import Treasure


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)

        self.color: Tuple[int, int, int] = RED
        self.walk_speed = 3.5
        self.money = 1000
        self.current_frame_index = 0
        self.exp = 0
        self.inn_badge = False
        self.level = 1
        self.body = 0
        self.mind = 0
        self.spirit = 0
        self.luck = 0
        self.food = 0
        self.perception = 2
        self.stamina_points = 160
        self.stamina_increase = self.body * 1 * self.level
        self.stamina_guard = False
        self.max_stamina_points = 160 + self.stamina_increase
        self.focus_points = 55
        self.max_focus_points = 10
        self.items = ["sir leopold's paw"]

        self.equipped_items = []

        self.npc_items = []
        self.magicinventory = ["shield",  "shake" ]
        self.companions = []
        self.canMove = True
        self.level3janetreward = False
        self.hasRabies = False
        self.rabies1time = False
        self.rabiesImmunity = False
        self.level2checker = False
        self.level3checker = False
        self.level4checker = False
        self.level5checker = False
        self.level6checker = False
        self.close_status_screen = False
        self.days = 0
        self.isBossWorthy = False
        self.realBarKeep = False
        self.shop_keep_potion = False
        self.shop_keep_save_coin = False
        self.current_frame_index = 0  # Current index in the sprite list
        # Timer for sprite animation
        self.sprite_animation_timer = 0
        self.sprite_animation_interval = 500  # 500 milliseconds (0.5 seconds) per frame
        self.left_animation_frames = []  # Holds frames for left movement animation
        # Initialize pygame's clock to manage the animation timer
        self.clock = pygame.time.Clock()
        # TODO refrence the images with relative paths
        self.sir_leopold_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/DS DSi - The World Ends With You - Hedge Hado Coa (1).png").convert_alpha()

        self.up_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.down_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.left_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.left_frames = [(28, 146, 18, 26), (46, 146, 18, 26), (63, 146, 17.9, 26)]
        self.down_frames = [(28, 120, 18, 26), (45, 120, 18, 26), (63, 120, 17.9, 26)]
        self.up_frames = [(29, 172, 18, 26), (47, 172, 18, 26), (64, 172, 17.9, 26)]
        # Set the initial direction and frame index.
        self.current_direction = 'down'  # Default direction
        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/levelup.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.level_two_npc_state = []
        self.leveling_up = False

        self.stamina_increase_from_level = 0
        self.focus_increase_from_level = 0
        self.stat_point_increase = False
        self.menu_index = 0
        self.menu_paused = False
        self.player_status = "Normal"

        self.current_screen = "main_menu_screen"
        self.item_index = 0

        self.items_equipped = []
        self.items_equipped_index = 0

        self.equipment_paused = False
        self.looking_at_items = False

        self.index_setter = 0
        self.quest_items = []

        self.magic_inventory_index = 0

        self.quest_items_index = 0

        self.exp_to_next_level = {
            1: 100,
            2: 300,
            3: 600,
            4: 1200,
            5: 2000,
            6: 3500,  # Continue adding levels as needed
            # Add more levels as needed
        }

    def to_dict(self, state: "GameState") -> dict:
        return {
            "level": self.level,
            "exp": self.exp,
            "stamina_points": self.stamina_points,
            "max_stamina_points": self.max_stamina_points,
            "focus_points": self.focus_points,
            "max_focus_points": self.max_focus_points,
            "companions": self.companions,
            "items": self.items,
            "equipped_items": self.equipped_items,
            "npcitems": self.npc_items,
            "magicinventory": self.magicinventory,
            "body": self.body,
            "mind": self.mind,
            "spirit": self.spirit,
            "perception": self.perception,
            "luck": self.luck,
            "money": self.money,
            "rabies": self.hasRabies,
            "immunity": self.rabiesImmunity,
            "quest_items": self.quest_items,
            "level3reward": self.level3janetreward,
            "food": self.food,
            "days": self.days,
            "leveltwonpcstate": self.level_two_npc_state,

            "cutscene1": state.restScreen.barscene1,
            "cutscene2": state.restScreen.barscene2,

            "quest1complete": state.gamblingAreaScreen.five_hundred_opossums,

            "coinfliptedmoney": state.coinFlipTedScreen.coinFlipTedMoney,
            "coinflipfredmoney": state.coinFlipFredScreen.coinFlipFredMoney,

            "opossumnellymoney": state.opossumInACanNellyScreen.nellyOpossumMoney,
            "opossumsallymoney": state.opossumInACanSallyScreen.sallyOpossumMoney,

            "blackjackthomasmoney": state.blackJackThomasScreen.cheater_bob_money,
            "blackjackrumblebillmoney": state.blackJackRumbleBillScreen.cheater_bob_money,

            "shopkeeperpotion": self.shop_keep_potion,
            "shopkeepersavecoin": self.shop_keep_save_coin,


            # level 2
            "slotsrippasnappamoney": state.slotsRippaSnappaScreen.money,

            # Add more stats as needed
        }


    def update(self, state: "GameState"):
        if state.controller.isAPressed:

            print("Your nPc inventory issss:::   " + str(state.player.npc_items))
            print("Your level 2 NPC state  issss:::   " + str(state.player.level_two_npc_state))



        controller = state.controller
        controller.update()


        if self.exp >= 100 and self.level2checker == False:
            print("grats you leveld up to level 2")
            self.level = 2

            if self.spirit < 1:
                self.max_stamina_points += 10 + (self.stamina_increase)
                self.max_focus_points += 10
                self.spirit += 1
            self.level2checker = True
            self.leveling_up = True
            return

        if self.exp >= 300 and self.level3checker == False:
            print("grats you leveld up to level 3")
            # if "shield" not in self.magicinventory:
            if "shield" not in state.player.magicinventory:
                self.magicinventory.append("shield")
                self.max_stamina_points += 10
                self.max_focus_points += 10
            self.level3checker = True
            self.leveling_up = True

            self.level = 3

            return

        if self.exp >= 600 and self.level4checker == False:
            print("grats you leveld up to level 4")
            if "level 4 token" not in state.player.npc_items:
            # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                self.max_stamina_points += 20
                self.max_focus_points += 20
            self.level4checker = True
            self.level = 4
            self.leveling_up = True


            return

        if self.exp >= 1200 and self.level5checker == False:
            print("grats you leveld up to level 5")
            if "level 5 token" not in state.player.npc_items:
                # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                stamina_increase = 20
                self.max_stamina_points += stamina_increase
                self.stamina_increase_from_level = stamina_increase

                focus_increase = 20
                self.max_focus_points += focus_increase
                self.focus_increase_from_level = focus_increase
                self.stat_point_increase = True


            self.level5checker = True
            self.level = 5
            self.leveling_up = True


            return

        if self.exp >= 2000 and self.level6checker == False:
            print("grats you leveld up to level 6")
            if "level 6 token" not in state.player.npc_items:
                # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                self.max_stamina_points += 20
                self.max_focus_points += 20
            self.level6checker = True
            self.level = 6
            self.leveling_up = True


            return


        # Define canMove before the for loop
        for npc in state.npcs:
            if npc.isSpeaking:
                self.canMove = False
                break

        if self.canMove:
            if controller.isLeftPressed:
                self.velocity.x = -self.walk_speed
                self.current_direction = 'left'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.left_frames)

            elif controller.isRightPressed:
                self.velocity.x = self.walk_speed
                self.current_direction = 'right'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.left_frames)

            else:
                # hard stop
                # self.velocity.x = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.x *= 0.65  # gradually slow the x velocity down
                if abs(self.velocity.x) < 0.15:  # if x velocity is close to zero, just set to zero
                    self.velocity.x = 0

            if controller.isUpPressed:
                self.velocity.y = -self.walk_speed
                self.current_direction = 'up'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.up_frames)


            elif controller.isDownPressed:
                self.velocity.y = self.walk_speed
                self.current_direction = 'down'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.down_frames)

            else:
                # hard stop
                # self.velocity.y = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.y *= 0.65  # gradually slow the y velocity down
                if abs(self.velocity.y) < 0.15:  # if y velocity is close to zero, just set to zero
                    self.velocity.y = 0

        else:  # if can not move, set velocity to zero
            self.velocity.x = 0
            self.velocity.y = 0

        # move player by velocity
        # note that if we have any collisions later we will undo the movements.
        # TODO test collision BEFORE moving
        self.setPosition(self.position.x + self.velocity.x,
                         self.position.y + self.velocity.y)



        if self.isOverlap(state.obstacle):
            self.undoLastMove()




        for npc in state.npcs:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(npc.collision) :



                # print("collide with npc: " + str(npc.collision.toTuple()))
                # print("moogle pants")

                self.undoLastMove()
                break

        for treasurechests in state.treasurechests:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(treasurechests.collision) :
                print("collide with chests: " + str(treasurechests.collision.toTuple()))
                self.undoLastMove()
                break

        for demon in state.demons:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(
                    demon.collision) :
                # print("collide with npc: " + str(demon.collision.toTuple()))
                self.undoLastMove()
                break


    def draw(self, state):
        sprite = None  # Initialize sprite to None

        if self.current_direction == 'up':
            # Define the rectangle for the up sprite
            frame_rect = self.up_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.up_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.up_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))
        elif self.current_direction == 'down':
            frame_rect = self.down_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.down_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.left_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))
            # Define the rectangle for the down sprite
            # sprite_rect = pygame.Rect(22, 120, 24, 26)  # Your provided values for the 'down' sprite
            # sprite = self.down_sprite.subsurface(sprite_rect)

        if self.current_direction == 'left':
            # Get the current frame rectangle based on self.current_frame_index
            frame_rect = self.left_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.left_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.left_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))

        elif self.current_direction == 'right':
            frame_rect = self.left_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.left_sprite.subsurface(sprite_rect)
            current_frame_sprite = pygame.transform.flip(current_frame_sprite, True, False)

            # Scale the selected sprite
            scaled_sprite = pygame.transform.scale(current_frame_sprite, (50, 50))

            # Assign the scaled sprite to the sprite variable
            sprite = scaled_sprite

            # Calculate the position to draw the sprite, adjusting for the camera
            sprite_x = self.collision.x + state.camera.x - 10
            sprite_y = self.collision.y + state.camera.y - 10

            # Draw the sprite on the screen
            # state.DISPLAY.blit(sprite, (sprite_x, sprite_y))

            # Scale the selected sprite
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))

        # Calculate the position to draw the sprite, adjusting for the camera
        sprite_x = self.collision.x + state.camera.x - 10
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the sprite on the screen
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

    def draw_player_stats(self, state):

        self.menu_paused = True


        if self.current_screen == "main_menu_screen":

            # Get the dimensions of the display
            screen_width = state.DISPLAY.get_width()
            screen_height = state.DISPLAY.get_height()

            # 1. Black Background
            state.DISPLAY.fill((0, 0, 0))  # Fill the entire screen with black

            # 2. Main Box (Covering most of the screen)
            main_box_width = screen_width - 20  # 10 pixels padding on both sides
            main_box_height = screen_height - 20  # 10 pixels padding on top and bottom

            # Define the gradient colors (top to bottom)
            top_color = (0, 0, 139)  # Dark blue
            bottom_color = (135, 206, 250)  # Light blue

            # Pre-calculate the gradient colors for each pixel row of the main box
            gradient_colors = []
            for y in range(main_box_height):
                color = (
                    bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                    bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                    bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
                )
                gradient_colors.append(color)

            # Create the main box surface with the gradient applied
            main_box = pygame.Surface((main_box_width, main_box_height))
            for y in range(main_box_height):
                pygame.draw.line(main_box, gradient_colors[y], (0, y), (main_box_width, y))

            # Draw the main box centered on the screen
            state.DISPLAY.blit(main_box, (10, 10))

            border_thickness = 3
            pygame.draw.line(state.DISPLAY, (255, 255, 255), (10, 12), (10 + main_box_width - 5, 12), border_thickness)  # Top
            pygame.draw.line(state.DISPLAY, (255, 255, 255), (10, 10), (10, 10 + main_box_height), border_thickness)  # Left
            # Draw the bottom border line, ensuring it's straight
            pygame.draw.line(state.DISPLAY, (255, 255, 255), (10, 10 + main_box_height - 2), (10 + main_box_width - 220, 10 + main_box_height - 2), border_thickness)  # Bottom

            # Add a white border around the main box
            # border_thickness = 3
            # pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(10, 10, main_box_width, main_box_height), border_thickness, border_radius=20)

            # 3. Third Box (Top right box)
            third_box_width = 220
            third_box_height = 400
            third_box_y = 10  # 10 pixels padding from the top
            third_box_x = screen_width - third_box_width - 10  # 10 pixels padding from the right

            # Create the third box surface with the gradient applied
            third_box = pygame.Surface((third_box_width, third_box_height), pygame.SRCALPHA)
            for y in range(third_box_height):
                pygame.draw.line(third_box, gradient_colors[y], (0, y), (third_box_width, y))

            # Draw the third box on the right side of the screen
            state.DISPLAY.blit(third_box, (third_box_x, third_box_y))

            # Add a white border around the third box
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(third_box_x, third_box_y, third_box_width, third_box_height), border_thickness, border_radius=7)

            # 4. Fourth Box (Bottom right box)
            fourth_box_width = 220
            fourth_box_height = 170
            fourth_box_y = third_box_y + third_box_height + 10  # 10 pixels padding below the third box
            fourth_box_x = screen_width - fourth_box_width - 10  # 10 pixels padding from the right

            # Create the fourth box surface with the gradient applied
            fourth_box = pygame.Surface((fourth_box_width, fourth_box_height), pygame.SRCALPHA)
            for y in range(fourth_box_height):
                pygame.draw.line(fourth_box, gradient_colors[y + third_box_height + 10], (0, y), (fourth_box_width, y))

            # Draw the fourth box below the third box
            state.DISPLAY.blit(fourth_box, (fourth_box_x, fourth_box_y))

            # Add a white border around the fourth box
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(fourth_box_x, fourth_box_y, fourth_box_width, fourth_box_height), border_thickness, border_radius=7)

            # Render the menu items and arrow in the third box

            # Set the font for the menu items
            font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

            # Define the menu items - note this needs 3 more to fill the screen proper
            # config, load,
            menu_items = ["Equipment", "Quest Items", "Magic", "Status"]








            ##########

            ###### DO NOT DELETE THE BELOW______________----------------------------------------
            # menu_items = ["Equipment", "Quest Items", "Magic", "Status", "Companions", "Config", "Load", "Quit"]

            # Starting y position for the first item
            item_y = 30  # Adjust this as needed to center vertically within the box

            # Draw each menu item in the box with 20 pixels between each
            for item in menu_items:
                text_surface = font.render(item, True, (255, 255, 255))  # White color for text
                third_box.blit(text_surface, (50, item_y))  # Adjust x-position as needed
                item_y += text_surface.get_height() + 20  # Move to the next line with 20 pixels spacing

            # Define the arrow symbol

            arrow = "->"

            # Render the arrow
            arrow_surface = font.render(arrow, True, (255, 255, 255))  # White color for the arrow

            # Calculate the y position of the arrow based on the menu index
            arrow_y = 28 + self.menu_index * (text_surface.get_height() + 20)

            # Draw the arrow in the top box, aligned with the menu item
            third_box.blit(arrow_surface, (10, arrow_y))  # Positioned 20 pixels from the left edge

            # Set the font for the text in the fourth box
            font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

            # Create the text to display in the fourth box
            gold_text = f"GP"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(gold_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (30, 30))  # 30 pixels from the left edge and top

            money_text = f"{self.money}"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(money_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (75, 60))  # 30 pixels from the left edge and top

            status_text = f"Status"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(status_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (30, 100))  # 30 pixels from the left edge and top

            status_text = f"{self.player_status}"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(status_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (75, 130))  # 30 pixels from the left edge and top



            #######

            status_text = f"Time"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(status_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (30, 170))  # 30 pixels from the left edge and top

            status_text = f"00:00"

            # Set the x and y positions, similar to the top box
            text_surface = font.render(status_text, True, (255, 255, 255))  # White color for text
            fourth_box.blit(text_surface, (75, 200))  # 30 pixels from the left edge and top






            # Display everything on the screen
            state.DISPLAY.blit(third_box, (third_box_x, third_box_y))
            state.DISPLAY.blit(fourth_box, (fourth_box_x, fourth_box_y))

            # Draw the borders around each box with rounded corners
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(third_box_x, third_box_y, third_box_width, third_box_height), border_thickness, border_radius=7)
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(fourth_box_x, fourth_box_y, fourth_box_width, fourth_box_height), border_thickness, border_radius=7)

            ######

            if  "sir leopold" in state.player.companions:


                # Get the subsurface for the area you want
                sprite_rect = pygame.Rect(5, 6, 56, 35)

                # Get the subsurface for the area you want
                sprite = self.sir_leopold_image.subsurface(sprite_rect)

                # Scale the subsurface to make it two times bigger
                scaled_sprite = pygame.transform.scale(sprite, (70, 70))  # 44*2 = 88

                # Define the position where you want to draw the sprite
                sir_leopold_sprite_x = 43
                sir_leopold_sprite_y = 180

                # Draw the scaled sprite portion on the display
                state.DISPLAY.blit(scaled_sprite, (sir_leopold_sprite_x, sir_leopold_sprite_y))
                sir_leopold_name = font.render(f"Sir Leopold", True, color)
                sir_leoplold_name_x = 140
                sir_leoplold_name_y = 205
                state.DISPLAY.blit(sir_leopold_name, (sir_leoplold_name_x, sir_leoplold_name_y))

            hero_name = font.render(f"Hero", True, color)

            hero__name_x = 170
            hero__name_y = 50
            state.DISPLAY.blit(hero_name, (hero__name_x, hero__name_y))

            # Load the down-facing sprite of the hero
            down_facing_hero_sprite = self.down_sprite.subsurface(pygame.Rect(*self.down_frames[0]))

            # Scale the sprite if needed (optional)
            scaled_hero_sprite = pygame.transform.scale(down_facing_hero_sprite, (64, 64))

            # Calculate the position to place the hero's sprite on the screen
            hero_sprite_x = 40  # Adjust this value to position more towards the top left
            hero_sprite_y = 70  # Adjust this value to position more towards the top left

            # Draw the hero's sprite on the screen
            state.DISPLAY.blit(scaled_hero_sprite, (hero_sprite_x, hero_sprite_y))

            # Define the font and color for the HP display
            font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
            color = (255, 255, 255)  # White color for text

            # Render the HP text into a Surface object
            hp_display_surface = font.render(f"HP: {self.stamina_points} /", True, color)
            hp_max_display_surface = font.render(f"{self.max_stamina_points}", True, color)

            # Calculate the position to place the hero's HP text on the screen
            hero_hp_x = 130  # Adjust this value to position more towards the top left
            hero_hp_sprite_y = 80  # Adjust this value to position more towards the top left
            max_hero_hp_x = 240  # Adjust this value to position more towards the top left
            max_hero_hp_sprite_y = 80  # Adjust this value to position more towards the top left

            # Blit the HP text surfaces onto the screen
            state.DISPLAY.blit(hp_display_surface, (hero_hp_x, hero_hp_sprite_y))
            state.DISPLAY.blit(hp_max_display_surface, (max_hero_hp_x, max_hero_hp_sprite_y))

            hero_mp_x = 130  # Adjust this value to position more towards the top left
            hero_mp_sprite_y = 110  # Adjust this value to position more towards the top left
            max_hero_mp_x = 240  # Adjust this value to position more towards the top left
            max_hero_mp_sprite_y = 110  # Adjust this value to position more towards the top left

            mp_display_surface = font.render(f"MP: {self.focus_points} /", True, color)
            mp_max_display_surface = font.render(f"{self.max_focus_points}", True, color)
            # Blit the HP text surfaces onto the screen
            state.DISPLAY.blit(mp_display_surface, (hero_mp_x, hero_mp_sprite_y))
            state.DISPLAY.blit(mp_max_display_surface, (max_hero_mp_x, max_hero_mp_sprite_y))

            if state.controller.isTPressed:
                if self.menu_index == 0:
                    state.controller.isTPressed = False
                    self.current_screen = "equipment_screen"
                elif self.menu_index == 1:
                    state.controller.isTPressed = False
                    self.current_screen = "quest_items_screen"
                elif self.menu_index == 2:
                    state.controller.isTPressed = False
                    self.current_screen = "magic_inventory_screen"
                elif self.menu_index == 3:
                    state.controller.isTPressed = False
                    self.current_screen = "status_screen"


            # Handle menu navigation with up/down arrow keys
            if self.menu_paused:
                if state.controller.isUpPressed:
                    self.menu_index = (self.menu_index - 1) % len(menu_items)
                    state.controller.isUpPressed = False

                elif state.controller.isDownPressed:
                    self.menu_index = (self.menu_index + 1) % len(menu_items)
                    state.controller.isDownPressed = False


        if self.current_screen == "equipment_screen":
            # Ensure that self.item_index is initialized outside of this method (e.g., in the __init__ method of your class)

            # Set the number of menu items
            menu_items = self.items  # Assuming self.items is the list you want to navigate through

            # Display the equipment screen
            self.equipment_screen(state)

            # Handle up/down navigation
            if self.looking_at_items == True:

                # Equip the selected item if T is pressed
                if state.controller.isTPressed:
                    state.controller.isTPressed = False
                    self.equipped_items[self.items_equipped_index] = self.items[self.item_index]
                    print(f"Equipped item: {self.items[self.item_index]} at slot {self.items_equipped_index}")
                    self.looking_at_items = False

                if state.controller.isBPressed:
                    state.controller.isBPressed = False
                    self.looking_at_items = False
                # Handle up/down navigation for items
                if state.controller.isUpPressed:
                    self.item_index = (self.item_index - 1) % len(self.items)
                    state.controller.isUpPressed = False
                    print(self.items[self.item_index])  # Print the item at the current index
                    self.show_item_description(state)

                elif state.controller.isDownPressed:
                    self.item_index = (self.item_index + 1) % len(self.items)
                    state.controller.isDownPressed = False
                    print(self.items[self.item_index])  # Print the item at the current index
                    self.show_item_description(state)

                # Update the description for the selected item
                self.show_item_description(state)

            elif self.looking_at_items == False:

                if state.controller.isBPressed:
                    state.controller.isBPressed = False
                    self.current_screen = "main_menu_screen"
                if state.controller.isTPressed:
                    state.controller.isTPressed = False
                    self.looking_at_items = True
                # Determine the maximum index based on perception level
                if self.perception < 3:
                    max_index = 2  # Can only access up to the 2nd slot (index 0 and 1)
                elif self.perception == 3 or self.perception == 4:
                    max_index = 3  # Can access up to the 3rd slot (index 0, 1, 2)
                elif self.perception >= 5:
                    max_index = 4  # Can access all slots (index 0, 1, 2, 3, 4)

                # Handle up/down navigation for equipped items based on max_index
                if state.controller.isUpPressed:
                    self.items_equipped_index = (self.items_equipped_index - 1) % (max_index + 1)
                    state.controller.isUpPressed = False
                    print(f"Selected equipped item slot: {self.items_equipped_index}")  # Print the currently selected equipped item slot

                elif state.controller.isDownPressed:
                    self.items_equipped_index = (self.items_equipped_index + 1) % (max_index + 1)
                    state.controller.isDownPressed = False
                    print(f"Selected equipped item slot: {self.items_equipped_index}")  # Print the currently selected equipped item slot

                # Print the currently selected equipped item or indicate if the slot is empty
                if self.items_equipped_index < len(self.equipped_items):
                    print(f"Currently selected equipped item: {self.equipped_items[self.items_equipped_index]}")
                else:
                    print(f"Selected slot {self.items_equipped_index} is empty.")

        elif self.current_screen == "quest_items_screen":
            if state.controller.isUpPressed:
                self.quest_items_index = (self.quest_items_index - 1) % len(self.quest_items)
                state.controller.isUpPressed = False
                print(self.quest_items[self.quest_items_index])  # Print the item at the current index

            elif state.controller.isDownPressed:
                self.quest_items_index = (self.quest_items_index + 1) % len(self.quest_items)
                state.controller.isDownPressed = False
                print(self.quest_items[self.quest_items_index])  # Print the item at the current index

            self.quest_item_screen(state)
            self.show_quest_items_description(state)

            if state.controller.isBPressed:
                state.controller.isBPressed = False
                self.current_screen = "main_menu_screen"

        elif self.current_screen == "magic_inventory_screen":

            # Handle Up/Down navigation for the magic inventory
            if state.controller.isUpPressed:
                self.magic_inventory_index = (self.magic_inventory_index - 1) % len(self.magicinventory)
                state.controller.isUpPressed = False
                print(self.magicinventory[self.magic_inventory_index])  # Print the item at the current index

            elif state.controller.isDownPressed:
                self.magic_inventory_index = (self.magic_inventory_index + 1) % len(self.magicinventory)
                state.controller.isDownPressed = False
                print(self.magicinventory[self.magic_inventory_index])  # Print the item at the current index

            # First, render the magic inventory screen
            self.magic_inventory_screen(state)

            # Then, display the description on top of the screen
            self.show_magic_description(state)

            # Handle back button press to return to the main menu
            if state.controller.isBPressed:
                state.controller.isBPressed = False
                self.current_screen = "main_menu_screen"

        elif self.current_screen == "status_screen":
            if state.controller.isBPressed:
                state.controller.isBPressed = False
                self.current_screen = "main_menu_screen"
            self.status_screen(state)

    def status_screen(self, state):
        screen_width = state.DISPLAY.get_width()
        screen_height = state.DISPLAY.get_height()

        # Fill the entire screen with black
        state.DISPLAY.fill((0, 0, 0))  # Black color

        # 1. Main Box with gradient and border
        main_box_width = screen_width - 20
        main_box_height = 530
        main_box_x = 10
        main_box_y = 60  # Positioned 60 pixels from the top

        # Define the gradient colors (top to bottom)
        top_color = (0, 0, 139)  # Dark blue
        bottom_color = (135, 206, 250)  # Light blue

        # Create the main box surface with its gradient
        main_box = pygame.Surface((main_box_width, main_box_height))
        for y in range(main_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
            )
            pygame.draw.line(main_box, color, (0, y), (main_box_width, y))

        # Add border to the main box
        border_thickness = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)

        # 2. Render Hero and Stats in Main Box
        font = pygame.font.Font(None, 36)  # Adjust the font size as needed
        text_color = (255, 255, 255)  # White color for the text

        # Render "Hero"
        hero_text = font.render("Hero", True, text_color)
        main_box.blit(hero_text, (50, 30))  # Positioning at (50, 50) inside the main box

        # Render HP and MP
        current_level_text = font.render(f"Level: {self.level}", True, text_color)
        hp_text = font.render(f"HP: {self.stamina_points} / {self.max_stamina_points}", True, text_color)
        mp_text = font.render(f"MP: {self.focus_points} / {self.max_focus_points}", True, text_color)
        exp_text = font.render(f"EXP: {self.exp} / {self.exp_to_next_level.get(self.level, 'Max Level')}", True, text_color)
        body_text = font.render(f"Body: {self.body}", True, text_color)
        mind_text = font.render(f"Mind: {self.mind}", True, text_color)
        spirit_text = font.render(f"Spirit: {self.spirit}", True, text_color)
        perception_text = font.render(f"Perception: {self.perception}", True, text_color)
        luck_text = font.render(f"Luck: {self.luck}", True, text_color)

        main_box.blit(current_level_text, (50, 80))  # Positioning MP display at (50, 150)

        main_box.blit(hp_text, (50, 130))  # Positioning HP display at (50, 100)
        main_box.blit(mp_text, (50, 180))  # Positioning MP display at (50, 150)
        main_box.blit(exp_text, (50, 230))  # Positioning MP display at (50, 150)

        main_box.blit(body_text, (50, 280))  # Positioning MP display at (50, 150)
        main_box.blit(mind_text, (50, 330))  # Positioning MP display at (50, 150)
        main_box.blit(spirit_text, (50, 380))  # Positioning MP display at (50, 150)
        main_box.blit(perception_text, (50, 430))  # Positioning MP display at (50, 150)
        main_box.blit(luck_text, (50, 480))  # Positioning MP display at (50, 150)

        # Draw the main box on the screen
        state.DISPLAY.blit(main_box, (main_box_x, main_box_y))

        # Draw the borders again to ensure visibility
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)

        # 4. Third Box (Small box overlapping top right corner) - Render Last to Overlay
        box3_width = 200
        box3_height = 70
        box3_x = screen_width - box3_width - 10  # Positioned at the right edge with padding
        box3_y = 30  # Positioned to overlap the top right corner of Box 2

        # Create Box 3's surface with its gradient
        box3_surface = pygame.Surface((box3_width, box3_height))
        for y in range(box3_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // box3_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // box3_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // box3_height,
            )
            pygame.draw.line(box3_surface, color, (0, y), (box3_width, y))

        # Draw Box 3 overlapping Box 2's top right corner
        state.DISPLAY.blit(box3_surface, (box3_x, box3_y))

        # Render the text "Status" inside Box 3
        text_surface = font.render("Status", True, (255, 255, 255))  # White color for the text
        text_x = box3_x + (box3_width - text_surface.get_width()) // 2
        text_y = box3_y + (box3_height - text_surface.get_height()) // 2
        state.DISPLAY.blit(text_surface, (text_x, text_y))

        # Add a white border around Box 3 with rounded corners
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(box3_x, box3_y, box3_width, box3_height), border_thickness, border_radius=7)

    def magic_inventory_screen(self, state):
        screen_width = state.DISPLAY.get_width()
        screen_height = state.DISPLAY.get_height()

        # Fill the entire screen with black
        state.DISPLAY.fill((0, 0, 0))  # Black color

        # 1. Main Box with gradient and border
        main_box_width = screen_width - 20
        main_box_height = 420
        main_box_x = 10
        main_box_y = 60  # Positioned 60 pixels from the top

        # Define the gradient colors (top to bottom)
        top_color = (0, 0, 139)  # Dark blue
        bottom_color = (135, 206, 250)  # Light blue

        # Create the main box surface with its gradient
        main_box = pygame.Surface((main_box_width, main_box_height))
        for y in range(main_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
            )
            pygame.draw.line(main_box, color, (0, y), (main_box_width, y))

        # Add border to the main box
        border_thickness = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)

        # 2. Render Magic Items in Main Box
        font = pygame.font.Font(None, 36)  # Adjust the font size as needed
        quest_item_y = 30  # Start position from the top of the box
        quest_item_x = 80  # Start position from the left of the box
        spacing = 10  # Spacing between items
        inventory_color = (155, 23, 155)  # Example color, you can change this to any RGB value

        for magic in state.player.magicinventory:
            text_surface = font.render(magic, True, inventory_color)  # Render the text in the specified color
            main_box.blit(text_surface, (quest_item_x, quest_item_y))  # Blit the text onto the main box
            quest_item_y += text_surface.get_height() + spacing  # Move down for the next item

        # Calculate the y-position for the arrow based on the current magic_inventory_index
        arrow_y_position = 30 + self.magic_inventory_index * (font.get_height() + spacing)

        # Render the arrow in the main box at the position of the selected magic item
        arrow_surface = font.render("->", True, inventory_color)
        main_box.blit(arrow_surface, (quest_item_x - 40, arrow_y_position))

        # Draw the main box on the screen
        state.DISPLAY.blit(main_box, (main_box_x, main_box_y))

        # 3. Text Box with gradient and border
        text_box_width = screen_width - 20
        text_box_height = 100
        text_box_x = 10
        text_box_y = 490  # Positioned 560 pixels from the top

        # Create the text box surface with its gradient
        text_box = pygame.Surface((text_box_width, text_box_height))
        for y in range(text_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // text_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // text_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // text_box_height,
            )
            pygame.draw.line(text_box, color, (0, y), (text_box_width, y))

        # Add border to the text box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height), border_thickness, border_radius=7)

        # Draw the text box on the screen
        state.DISPLAY.blit(text_box, (text_box_x, text_box_y))

        # Draw the borders again to ensure visibility
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height), border_thickness, border_radius=7)

        # 4. Third Box (Small box overlapping top right corner) - Render Last to Overlay
        box3_width = 200
        box3_height = 70
        box3_x = screen_width - box3_width - 10  # Positioned at the right edge with padding
        box3_y = 30  # Positioned to overlap the top right corner of Box 2

        # Create Box 3's surface with its gradient
        box3_surface = pygame.Surface((box3_width, box3_height))
        for y in range(box3_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // box3_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // box3_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // box3_height,
            )
            pygame.draw.line(box3_surface, color, (0, y), (box3_width, y))

        # Draw Box 3 overlapping Box 2's top right corner
        state.DISPLAY.blit(box3_surface, (box3_x, box3_y))

        # Render the text "Magic" inside Box 3
        text_surface = font.render("Magic", True, (255, 255, 255))  # White color for the text
        text_x = box3_x + (box3_width - text_surface.get_width()) // 2
        text_y = box3_y + (box3_height - text_surface.get_height()) // 2
        state.DISPLAY.blit(text_surface, (text_x, text_y))

        # Add a white border around Box 3 with rounded corners
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(box3_x, box3_y, box3_width, box3_height), border_thickness, border_radius=7)

    def quest_item_screen(self, state):
        screen_width = state.DISPLAY.get_width()
        screen_height = state.DISPLAY.get_height()

        # Fill the entire screen with black
        state.DISPLAY.fill((0, 0, 0))  # Black color

        # 1. Main Box with gradient and border
        main_box_width = screen_width - 20
        main_box_height = 420
        main_box_x = 10
        main_box_y = 60  # Positioned 60 pixels from the top

        # Define the gradient colors (top to bottom)
        top_color = (0, 0, 139)  # Dark blue
        bottom_color = (135, 206, 250)  # Light blue

        # Create the main box surface with its gradient
        main_box = pygame.Surface((main_box_width, main_box_height))
        for y in range(main_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
            )
            pygame.draw.line(main_box, color, (0, y), (main_box_width, y))

        # Add border to the main box
        border_thickness = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)

        # 2. Render Quest Items in Main Box
        font = pygame.font.Font(None, 36)  # Adjust the font size as needed
        quest_item_y = 30  # Start position from the top of the box
        quest_item_x = 80  # Start position from the left of the box
        spacing = 10  # Spacing between items
        inventory_color = (155, 23, 155)  # Example color, you can change this to any RGB value

        for index, item in enumerate(state.player.quest_items):
            text_surface = font.render(item, True, inventory_color)  # Render the text in the specified color
            main_box.blit(text_surface, (quest_item_x, quest_item_y))  # Blit the text onto the main box

            # Check if this item is the currently selected one
            if index == self.quest_items_index:  # Assuming quest_item_index is tracking the selected index
                arrow_surface = font.render("->", True, (255, 255, 255))  # White color for the arrow
                main_box.blit(arrow_surface, (quest_item_x - 50, quest_item_y))  # Position the arrow 50 pixels to the left of the text

            quest_item_y += text_surface.get_height() + spacing  # Move down for the next item

        # Draw the main box on the screen
        state.DISPLAY.blit(main_box, (main_box_x, main_box_y))

        # 3. Text Box with gradient and border
        text_box_width = screen_width - 20
        text_box_height = 100
        text_box_x = 10
        text_box_y = 490  # Positioned 560 pixels from the top

        # Create the text box surface with its gradient
        text_box = pygame.Surface((text_box_width, text_box_height))
        for y in range(text_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // text_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // text_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // text_box_height,
            )
            pygame.draw.line(text_box, color, (0, y), (text_box_width, y))

        # Add border to the text box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height), border_thickness, border_radius=7)

        # Draw the text box on the screen
        state.DISPLAY.blit(text_box, (text_box_x, text_box_y))

        # Draw the borders again to ensure visibility
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height), border_thickness, border_radius=7)

        # 4. Third Box (Small box overlapping top right corner) - Render Last to Overlay
        box3_width = 200
        box3_height = 70
        box3_x = screen_width - box3_width - 10  # Positioned at the right edge with padding
        box3_y = 30  # Positioned to overlap the top right corner of Box 2

        # Create Box 3's surface with its gradient
        box3_surface = pygame.Surface((box3_width, box3_height))
        for y in range(box3_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // box3_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // box3_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // box3_height,
            )
            pygame.draw.line(box3_surface, color, (0, y), (box3_width, y))

        # Draw Box 3 overlapping Box 2's top right corner
        state.DISPLAY.blit(box3_surface, (box3_x, box3_y))

        # Render the text "Quest Items" inside Box 3
        text_surface = font.render("Quest Items", True, (255, 255, 255))  # White color for the text
        text_x = box3_x + (box3_width - text_surface.get_width()) // 2
        text_y = box3_y + (box3_height - text_surface.get_height()) // 2
        state.DISPLAY.blit(text_surface, (text_x, text_y))

        # Add a white border around Box 3 with rounded corners
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(box3_x, box3_y, box3_width, box3_height), border_thickness, border_radius=7)

    def equipment_screen(self, state):

            # Get the dimensions of the display
            screen_width = state.DISPLAY.get_width()
            screen_height = state.DISPLAY.get_height()

            # Fill the entire screen with black
            state.DISPLAY.fill((0, 0, 0))  # Black color

            # 2. Main Box with gradient and border
            main_box_width = screen_width - 20
            main_box_height = 220
            main_box_x = 10
            main_box_y = 60  # Lowered the position by 100 pixels

            # Define the gradient colors (top to bottom)
            top_color = (0, 0, 139)  # Dark blue
            bottom_color = (135, 206, 250)  # Light blue

            # Create the main box surface with its gradient
            main_box = pygame.Surface((main_box_width, main_box_height))
            for y in range(main_box_height):
                color = (
                    bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                    bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                    bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
                )
                pygame.draw.line(main_box, color, (0, y), (main_box_width, y))
            font = pygame.font.Font(None, 36)  # Adjust font size as needed
            item_color = (90, 244, 244)  # A unique blue color, easy on the eyes
            #########





            text_box_width = screen_width - 20
            text_box_height = 120
            text_box_x = 10
            text_box_y = 560  # Lowered the position by 100 pixels

            # Define the gradient colors (top to bottom)
            text_top_color = (0, 0, 139)  # Dark blue
            text_bottom_color = (135, 206, 250)  # Light blue

            # Create the main box surface with its gradient
            text_box = pygame.Surface((text_box_width, text_box_height))
            for y in range(text_box_height):
                color = (
                    bottom_color[0] + (top_color[0] - bottom_color[0]) * y // text_box_height,
                    bottom_color[1] + (top_color[1] - bottom_color[1]) * y // text_box_height,
                    bottom_color[2] + (top_color[2] - bottom_color[2]) * y // text_box_height,
                )
                pygame.draw.line(text_box, color, (0, y), (text_box_width, y))
            font = pygame.font.Font(None, 36)  # Adjust font size as needed


            # Draw the main and bottom boxes on the screen
            state.DISPLAY.blit(text_box, (text_box_x, text_box_y))







            ####
            # Get the dimensions of the display

            # Fill the entire screen with black

            # 2. Main Box with gradient and border
            bottom_box_width = screen_width - 20
            bottom_box_height = 240
            bottom_box_x = 10
            bottom_box_y = 300  # Lowered the position by 100 pixels

            # Define the gradient colors (top to bottom)
            top_color = (0, 0, 139)  # Dark blue
            bottom_color = (135, 206, 250)  # Light blue

            # Create the main box surface with its gradient
            bottom_box = pygame.Surface((bottom_box_width, bottom_box_height))
            for y in range(bottom_box_height):
                color = (
                    bottom_color[0] + (top_color[0] - bottom_color[0]) * y // bottom_box_height,
                    bottom_color[1] + (top_color[1] - bottom_color[1]) * y // bottom_box_height,
                    bottom_color[2] + (top_color[2] - bottom_color[2]) * y // bottom_box_height,
                )
                pygame.draw.line(bottom_box, color, (0, y), (bottom_box_width, y))
            font = pygame.font.Font(None, 36)  # Adjust font size as needed
            inventory_color = (155, 23, 155)  # A unique blue color, easy on the eyes

            # Print and display items in the bottom box
            item_y = 30  # Start 30 pixels from the top of the bottom box
            item_x = 80  # Start 30 pixels from the top of the bottom box
            spacing = 10  # Spacing between items

            for item in self.items:
                text_surface = font.render(item, True, inventory_color)  # Render the text in the specified color
                bottom_box.blit(text_surface, (item_x, item_y))  # 30 pixels margin from the left
                item_y += text_surface.get_height() + spacing  # Move down for the next item

            # Draw the main and bottom boxes on the screen
            state.DISPLAY.blit(main_box, (main_box_x, main_box_y))
            state.DISPLAY.blit(bottom_box, (bottom_box_x, bottom_box_y))

            # Print and display items in the bottom box
            # Print and display items in the bottom box
            # Display only the arrow next to the 0th item
            # Define the padding and spacing for the items
            # Define the padding and spacing for the items
            # Define the padding and spacing for the items
            inventory_arrow_padding = 50  # Padding from the left side of the box for the arrow in the inventory
            top_box_arrow_padding = 35  # Padding from the left side of the box for the arrow in the top box
            spacing = 10  # Spacing between items
            inventory_arrow_padding = 50  # Padding from the left side of the box for the arrow in the inventory
            top_box_arrow_padding = 35  # Padding from the left side of the box for the arrow in the top box
            spacing = 10  # Spacing between items

            if self.looking_at_items == True:
                # Arrow should point to an item in the inventory list
                item_y_start = 30  # The starting y-position for the items in the inventory

                # Calculate the y-position for the arrow based on the current item_index
                arrow_y_position = item_y_start + self.item_index * (font.get_height() + spacing)

                # Render the arrow and position it according to the current item_index
                arrow_surface = font.render("->", True, inventory_color)
                bottom_box.blit(arrow_surface, (item_x - inventory_arrow_padding, arrow_y_position))
            else:
                # Arrow should point to the currently selected equipped item
                item_y_start = 30  # The starting y-position for the equipped items in the top box

                # Define the items, including the level-based slots
                items = ["companion item", "item 1", "item 2", "LEVEL 3", "LEVEL 5"]

                # Starting y position for the first item (adjust as needed for vertical alignment)
                equipped_y_start = 30  # Start at the same y-position as the arrow, or any other position

                # Adjust the left margin for the equipped items
                equipped_item_margin = 300  # Adjust this to ensure there's enough space between the items and equipped items

                # Draw each item slot in Box 2 and display the equipped item next to it, if available
                item_y = equipped_y_start  # Start at the same y-position as the arrow
                for index, slot in enumerate(items):
                    # Render the item slot name
                    slot_surface = font.render(slot, True, item_color)  # Render the text in the specified color
                    main_box.blit(slot_surface, (50, item_y))  # Adjust x-position to center or align as needed

                    # Display the equipped item if it exists in this slot
                    if index < len(self.equipped_items) and self.equipped_items[index]:
                        equipped_item_surface = font.render(self.equipped_items[index], True, item_color)
                        main_box.blit(equipped_item_surface, (equipped_item_margin, item_y))  # 200 pixels to the right of the slot name

                    item_y += slot_surface.get_height() + 10  # Move down for the next item slot

                # Determine the maximum index based on perception level
                if self.perception < 3:
                    max_index = 2  # Can only access up to the 2nd index (index 0, 1, and 2)
                elif self.perception == 3 or self.perception == 4:
                    max_index = 3  # Can access up to the 3rd index (index 0, 1, 2, and 3)
                elif self.perception > 4:
                    max_index = 4  # Can access up to the 4th index (index 0, 1, 2, 3, and 4)

                # Ensure that the items_equipped_index does not exceed the max_index
                self.items_equipped_index = min(self.items_equipped_index, max_index)

                # Calculate the y-position for the arrow based on the current equipped item index
                arrow_y_position = item_y_start + self.items_equipped_index * (font.get_height() + spacing)

                # Render the arrow in the top box at the position of the selected equipped item
                arrow_surface = font.render("->", True, item_color)  # Assuming item_color is defined for the top box
                main_box.blit(arrow_surface, (50 - top_box_arrow_padding, arrow_y_position))

                # Print the currently selected equipped item, if it exists
                if self.items_equipped_index < len(items):
                    print(f"Currently selected equipped item: {items[self.items_equipped_index]}")
                else:
                    print(f"Selected slot {self.items_equipped_index} is empty or not yet equipped.")

            #######################

            # Define the items to display in Box 2
            items = ["companion item ", "item 1", "item 2", "LEVEL 3", "LEVEL 5"]

            # Starting y position for the first item (adjust as needed for vertical alignment)
            item_y_start = 30  # Start at the same y-position as the arrow, or any other position

            # Draw each item in Box 2
            item_y = item_y_start  # Start at the same y-position as the arrow
            for item in items:
                text_surface = font.render(item, True, item_color)  # Render the text in the specified color
                main_box.blit(text_surface, (50, item_y))  # Adjust x-position to center or align as needed
                item_y += text_surface.get_height() + spacing  # Move down for the next item

            state.DISPLAY.blit(main_box, (main_box_x, main_box_y))
            state.DISPLAY.blit(bottom_box, (bottom_box_x, bottom_box_y))

            # Add a white border around the main box
            border_thickness = 3


            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(main_box_x, main_box_y, main_box_width, main_box_height), border_thickness, border_radius=7)
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(bottom_box_x, bottom_box_y, bottom_box_width, bottom_box_height), border_thickness, border_radius=7)
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(text_box_x, text_box_y, text_box_width, text_box_height), border_thickness, border_radius=7)



            # 3. Third Box (Small box overlapping top right corner)
            box3_width = 200
            box3_height = 70
            # Calculate Box 3's position to overlap Box 2's top right corner
            box3_x = screen_width - box3_width - 10  # Positioned at the right edge with padding
            box3_y = 30  # Positioned to overlap the top right corner of Box 2

            # Create Box 3's surface with its gradient
            box3_surface = pygame.Surface((box3_width, box3_height))
            for y in range(box3_height):
                color = (
                    bottom_color[0] + (top_color[0] - bottom_color[0]) * y // box3_height,
                    bottom_color[1] + (top_color[1] - bottom_color[1]) * y // box3_height,
                    bottom_color[2] + (top_color[2] - bottom_color[2]) * y // box3_height,
                )
                pygame.draw.line(box3_surface, color, (0, y), (box3_width, y))



            # Draw Box 3 overlapping Box 2's top right corner
            state.DISPLAY.blit(box3_surface, (box3_x, box3_y))
            # Set the font for the text
            font = pygame.font.Font(None, 36)  # Adjust the font size as needed

            # Render the text "Equipment"
            text_surface = font.render("Equipment", True, (255, 255, 255))  # White color for the text

            # Calculate the position to center the text within Box 3
            text_x = box3_x + (box3_width - text_surface.get_width()) // 2
            text_y = box3_y + (box3_height - text_surface.get_height()) // 2

            # Draw the text inside Box 3
            state.DISPLAY.blit(text_surface, (text_x, text_y))

            # Optionally, add a white border around Box 3 with rounded corners
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(box3_x, box3_y, box3_width, box3_height), border_thickness, border_radius=7)

    def show_magic_description(self, state):
        # Define descriptions for each item
        descriptions = {
            "reveal": "its a good show.",
            "shield": "not a good show.",
            "shake": "an ok show"
        }

        # Get the item name based on the current index
        current_magic = self.magicinventory[self.magic_inventory_index]

        # Get the description for the current item
        description_text = descriptions.get(current_magic, "")

        # Render the description text
        font = pygame.font.Font(None, 36)  # Adjust font size as needed
        description_color = (255, 255, 255)  # White color for the text
        description_surface = font.render(description_text, True, description_color)

        # Assuming the text box position is already defined where you want the description to appear
        text_box_x = 10  # X position of the text box
        text_box_y = 490  # Y position of the text box

        # Position the text within the text box
        text_x = 20  # X position inside the text box
        text_y = 20  # Y position inside the text box

        # Blit the description text onto the existing text box
        state.DISPLAY.blit(description_surface, (text_box_x + text_x, text_box_y + text_y))

    def show_quest_items_description(self, state):
        # Define descriptions for each item
        descriptions = {
            "contract": "It's too bad you didnt' read it, not like anyone does",
            "BBQ_SAUCE": "ITS THE BOSS OF SAUCE."

        }

        # Get the item name based on the current index
        current_item = self.quest_items[self.quest_items_index]

        # Get the description for the current item
        description_text = descriptions.get(current_item, "")

        # Render the description text
        font = pygame.font.Font(None, 36)  # Adjust font size as needed
        description_color = (255, 255, 255)  # White color for the text
        description_surface = font.render(description_text, True, description_color)

        # Assuming the text box position is already defined where you want the description to appear
        text_box_x = 10  # X position of the text box
        text_box_y = 490  # Y position of the text box

        # Position the text within the text box
        text_x = 20  # X position inside the text box
        text_y = 20  # Y position inside the text box

        # Blit the description text onto the existing text box
        state.DISPLAY.blit(description_surface, (text_box_x + text_x, text_box_y + text_y))
    def show_item_description(self, state):
        # Define descriptions for each item
        descriptions = {
            "sir leopold's paw": "Sir Leopold can steal aces on initial draw.",
            "opossum repellent": "Keeps those pesky opossums at bay, 1/2 bite damage.",
            "coin flip glasses": "Get bonus money on wins + 10 per perception point."
        }

        # Get the item name based on the current index
        current_item = self.items[self.item_index]

        # Get the description for the current item
        description_text = descriptions.get(current_item, "")

        # Render the description text
        font = pygame.font.Font(None, 36)  # Adjust font size as needed
        description_color = (255, 255, 255)  # White color for the text
        description_surface = font.render(description_text, True, description_color)

        # Assuming the text box position is already defined where you want the description to appear
        text_box_x = 10  # X position of the text box
        text_box_y = 560  # Y position of the text box

        # Position the text within the text box
        text_x = 20  # X position inside the text box
        text_y = 20  # Y position inside the text box

        # Blit the description text onto the existing text box
        state.DISPLAY.blit(description_surface, (text_box_x + text_x, text_box_y + text_y))

    def load_game(self, state):

        # Define the file path
        file_path = '/Users/stevenhalla/code/casino_hell/assets/save_data.json'

        # Read the JSON string from the file
        try:
            with open(file_path, 'r') as file:
                player_data_json = file.read()

            # Convert JSON string to a dictionary
            player_data = json.loads(player_data_json)


            # Update player's stats with the loaded data
            state.player.level_two_npc_state = player_data['leveltwonpcstate']

            state.player.level = player_data['level']
            state.player.exp = player_data['exp']
            state.player.stamina_points = player_data['stamina_points']
            state.player.max_stamina_points = player_data['max_stamina_points']
            state.player.focus_points = player_data['focus_points']
            state.player.max_focus_points = player_data['max_focus_points']
            state.player.companions = player_data['companions']
            state.player.items = player_data['items']
            state.player.equipped_items = player_data['equipped_items']
            state.player.npc_items = player_data['npcitems']
            state.player.magicinventory = player_data['magicinventory']
            state.player.body = player_data['body']
            state.player.mind = player_data['mind']
            state.player.spirit = player_data['spirit']
            state.player.perception = player_data['perception']
            state.player.luck = player_data['luck']
            state.player.money = player_data['money']
            state.player.hasRabies = player_data['rabies']
            state.player.rabiesImmunity = player_data['immunity']
            state.player.quest_items = player_data['quest_items']
            state.player.level3janetreward = player_data['level3reward']
            state.player.food = player_data['food']
            state.player.days = player_data['days']
            state.restScreen.barscene1 = player_data['cutscene1']
            state.restScreen.barscene2 = player_data['cutscene2']
            state.gamblingAreaScreen.five_hundred_opossums = player_data['quest1complete']
            state.coinFlipTedScreen.coinFlipTedMoney = player_data['coinfliptedmoney']
            state.coinFlipFredScreen.coinFlipFredMoney = player_data['coinflipfredmoney']
            state.opossumInACanNellyScreen.nellyOpossumMoney = player_data['opossumnellymoney']
            state.opossumInACanSallyScreen.sallyOpossumMoney = player_data['opossumsallymoney']
            state.blackJackThomasScreen.cheater_bob_money = player_data['blackjackthomasmoney']
            state.blackJackRumbleBillScreen.cheater_bob_money = player_data['blackjackrumblebillmoney']

            state.player.shop_keep_potion = player_data['shopkeeperpotion']
            state.player.shop_keep_save_coin = player_data['shopkeepersavecoin']


            #level 2

            state.slotsRippaSnappaScreen.money = player_data['slotsrippasnappamoney']





            innkeeper_position_x = 16 * 22
            innkeeper_position_y = 16 * 11
            state.player.setPosition(innkeeper_position_x, innkeeper_position_y)

            # Switch to the restScreen
            # state.currentScreen = state.restScreen
            state.currentScreen = state.area2RestScreen


            state.area2RestScreen.start(state)
            # ... more stats as needed

            print("Game loaded successfully.")

        except Exception as e:
            print(f"Failed to load game: {e}")
