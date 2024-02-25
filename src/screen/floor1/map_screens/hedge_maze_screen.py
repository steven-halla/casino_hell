import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon1 import Demon1
from entity.demon.demon7 import Demon7
from entity.demon.demon2 import Demon2
from entity.demon.demon3 import Demon3
from entity.demon.demon4 import Demon4
from entity.npc.hedge_maze_screen.evilcat import EvilCat
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from entity.treasurechests.blueflower import BlueFlower
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class HedgeMazeScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/hedgemaze1.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        self.blue_flower = False
        move_player_down_flag = False
        self.hog4_replaced_with_demon = False  # Set a flag to prevent repeated additions
        self.add_demon = False
        self.clock = pygame.time.Clock()  # Initialize the clock


    def start(self, state: "GameState"):
        super().start(state)

        if state.chili_area_to_maze_area_entry_point == True:
            player_start_x = 16 * 45  # Desired X coordinate
            player_start_y = 16 * 176  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.chili_area_to_maze_area_entry_point = False



        state.treasurechests = [

            BlueFlower(16 * 72, 14 * 122),

        ]

        state.npcs = [
            HedgeHog4(16 * 3, 14 * 6),
            EvilCat(16 * 82, 14 * 35),
            HedgeHog2(16 * 10, 14 * 160),
            HedgeHog3(16 * 63, 14 * 118),
            HedgeHog1(16 * 79, 14 * 184), # this position is set for our 1st hoggy hog hog hog bottom right of screen
            ]

        state.demons = [
            Demon1(16 * 53, 14 * 180),#THIS POSITION IS SET TO 1ST ENEMY
            Demon1(16 * 26, 14 * 2), # THIS POSITION IS BOTTOM LEFT CORNER OF SCREEN
            Demon1(16 * 52, 14 * 154), #this position is set to 2nd enemy
            Demon1(16 * 37, 14 * 178), #this position is set to 2nd enemy
            # Demon2(16 * 20, 14 * 79),
            # Demon3(16 * 20, 14 * 85),
            # Demon4(16 * 20, 14 * 10),
            # Demon3(16 * 20, 14 * 76),
            # Demon2(16 * 55, 16 * 13),
            # Demon3(16 * 55, 16 * 23),
            # Demon4(16 * 55, 16 * 33),
        ]

    def update(self, state: "GameState"):
        # i dont think npc and demons getting updated
        # print(state.quest_giver_janet.find_hog)
        # print(state.quest_giver_janet.quest2counter)

        self.clock.tick(60)



        if "blue flower" in state.player.items:
            state.demons.clear()

            state.maze_area_to_chili_area_entry_point = True

            state.currentScreen = state.chilliScreen
            state.chilliScreen.start(state)

        if "blue flower" in state.player.items:
            # Loop through the demons to find Demon7 by its position or a unique identifier
            for demon in list(state.demons):  # Make a copy of the list to modify it while iterating
                if isinstance(demon, Demon7):
                    state.demons.remove(demon)
                    break  # Exit the loop once the Demon7 instance is found and removed

        hedgehog4_present = any(isinstance(npc, HedgeHog4) for npc in state.npcs)
        if not hedgehog4_present and self.hog4_replaced_with_demon == False:
            print("no hoggy")
            new_demon = Demon7(16 * 18, 16 * 17)  # You can set the position as needed
            state.demons.append(new_demon)
            self.hog4_replaced_with_demon = True  # Set a flag to prevent repeated additions

            # Ensure not to append Demon1 repeatedly after HedgeHog4 is deleted
            # You can use a flag or condition to make sure this happens only once

        if self.add_demon == True:
            new_demon = Demon4(16 * 80, 16 * 1)  # You can set the position as needed
            # Add the new demon to the state.demons list
            state.demons.append(new_demon)
            self.add_demon = False
            state.npcs = [npc for npc in state.npcs if not isinstance(npc, EvilCat)]





        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()


        # Assuming you have your hedgehog instances named like HedgeHog1, HedgeHog2, etc.
        # hedgehogs = [HedgeHog1(), HedgeHog2(), HedgeHog3(), HedgeHog4()]


        ### i can use this to append NPC if i need to , just state.npcs.append(npc)
        for npc in state.npcs:
            npc.update(state)
            # Check if the npc is any of the hedgehogs
            if isinstance(npc, (HedgeHog1, HedgeHog2, HedgeHog3, HedgeHog4)) and npc.to_be_deleted:
                self.hedge_hog_counter += 1
                print(self.hedge_hog_counter)
                state.npcs.remove(npc)

        # Game Update Loop
        for chest in state.treasurechests:
            chest.update(state)

        for demon in state.demons:
            demon.update(state)
            if demon.move_player_down:
                state.player.collision.y += 100  # Move player down by 100 pixels
                demon.move_player_down = False

        if controller.isExitPressed is True:
            state.isRunning = False


        player.update(state)

        # check map for collision
        if self.tiled_map.layers:
            tile_rect = Rectangle(0, 0, 16, 16)
            collision_layer = self.tiled_map.get_layer_by_name("collision")

            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()
                for demon in state.demons:
                    if demon.collision.isOverlap(tile_rect):
                        demon.undoLastMove()


        state.camera.x = PLAYER_OFFSET[0] - state.player.collision.x
        state.camera.y = PLAYER_OFFSET[1] - state.player.collision.y



    def draw(self, state: "GameState"):
        state.DISPLAY.fill(BLUEBLACK)
        # state.DISPLAY.blit(state.FONT.render(
        #     f"player money: {state.player.money}",
        #     True, (255, 255, 255)), (333, 333))
        # state.DISPLAY.blit(state.FONT.render(
        #     f"player stamina points: {state.player.stamina_points}",
        #     True, (255, 255, 255)), (333, 388))

        if self.tiled_map.layers:
            tile_width = self.tiled_map.tilewidth
            tile_height = self.tiled_map.tileheight

            # Get the background layer
            bg_layer = self.tiled_map.get_layer_by_name("bg")
            # Iterate over the tiles in the background layer
            for x, y, image in bg_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

            # Get the collision layer
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            for x, y, image in collision_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))



        for npc in state.npcs:
            npc.draw(state)

        # for npc in state.npcs:
        #     if isinstance(npc, ShopKeeper):
        #         npc.textbox.draw(state)

        for demon in state.demons:
            demon.draw(state)

        for treasurechests in state.treasurechests:
            treasurechests.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
