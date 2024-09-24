

import math
import pygame


from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


# in order to get this quest to work:
# if you win 500 coins get a coin
# if you win 500 coins from two games those coins become mega coin.
# if you rest at the innn, the lower coins vanish , but an inn stay wont eras the mega coin
class Alex(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Alex: I have  a simple quest for you: win 500 coins from the coin flip and oppossum in a can game in ONE SITTING",
                    "Hero: So no saving/resting of ANY sort in between?",
                    "Alex: Thats right ,so no cheating on this task, go big or go home....I really want to go home...I dont remember what my children look like",

                ],
                (50, 450, 50, 45), 30, 500
            ),
                "quest_1_complete": NpcTextBox(
                [
                    "Alex: I see you did as I asked I'll give you this new magic spell heads force , its great for a last push",
                    "Hero: Thank you for this friend. ", ""


                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_1_complete_after_message": NpcTextBox(
                [
                    "Alex: I heard somewhere there is an opposum in a can spell. You should go find it.",

                ],
                (50, 450, 50, 45), 30, 500
            ),

        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Ellens Parents.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):



        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.npc_messages["default_message"]

            if Events.QUEST_1_COMPLETE.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_1_complete"]
                if self.npc_messages["quest_1_complete"].message_index == 2:
                    state.currentScreen = state.hungryStarvingHippos
                    state.hungryStarvingHippos.start(state)

            if Magic.HEADS_FORCE.value in state.player.magicinventory:
                current_message = self.npc_messages["quest_1_complete_after_message"]



            if current_message.message_index == 1:
                if state.controller.isAPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"


                elif state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            self.update_talking(state, current_message)

    def update_waiting(self, state: "GameState"):
        player = state.player
        min_distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

            if distance < 40 and state.player.menu_paused == False:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.npc_messages["default_message"]

                if Events.QUEST_1_COMPLETE.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_1_complete"]

                if Magic.HEADS_FORCE.value in state.player.magicinventory:
                    current_message = self.npc_messages["quest_1_complete_after_message"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            if Events.QUEST_1_COMPLETE.value in state.player.level_two_npc_state and Magic.HEADS_FORCE.value not in state.player.magicinventory:
                state.player.magicinventory.append(Magic.HEADS_FORCE.value)

            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(108, 5, 22, 26)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = self.npc_messages["default_message"]

            if Events.QUEST_1_COMPLETE.value in state.player.level_two_npc_state:
                print("Hi")
                current_message = self.npc_messages["quest_1_complete"]

            if Magic.HEADS_FORCE.value in state.player.magicinventory:
                current_message = self.npc_messages["quest_1_complete_after_message"]

            current_message.draw(state)





