

import math

import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic
from game_constants.treasure import Treasure


# there should be 3 quest
# first 500 COINS
#  + 10 HP
#  THRID GOURMAND HAT


# quest marker npc items 2 we can store quest state there as well as talking state of quest whether we talked to npc already or 1st time
# need to add quest marker state

class MCNugg(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.npc_messages = {

            "level_6_quest": NpcTextBox(
                [
                    "MC Nugg: Yo, What up, nugg brothers.",
                    "Sir Leopold: Wow, his voice is so deep, and smooth.",
                    "MC Nugg: Back in my Day I was known as the king of soul. Now I'm known as the king of nuggets. Want me to squeeze you out a 6 piece?",
                    "Hero: No thanks on that. I'm here to gamble.",
                    "Mc Nugg: Well in that case you've come to the wrong place. But I'll tell you what Nugg brother.",
                    "If you can get the special rib demon item from the slots dealer I'll reward you with something special."


                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_1_finish": NpcTextBox(
                [
                    "MC Nugg: I knew you were a pure hearted soul nugg brother, have this reward from the king of nuggets. ",
                    "Hero: Thank you for the cool shades, what do they do?",
                    "Mc Nugg: These glasses will raise your perception. You can use it to find the secret sauce that the demons hid.",
                    "Sir leopold: What is it with all the saucy business? Isn't there anyting of better value.",
                    "Mc Nugg: No little nugglet, down on this floor sauce is boss."

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_start": NpcTextBox(
                [
                    "MC Nugg: listen up nugg brother, equip those shades and go find that sauce for me.",
                    "Hero: i'll check around ",
                    "Mc Nugg: And don't forget, with a perception of 3 you can equip more items."

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_finish": NpcTextBox(
                [
                    "MC Nugg: Good on you here is your reward of 500 coins, don't spend em all in 1 place.",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_3_start": NpcTextBox(
                [
                    "MC Nugg: ok now its time for your final nugg Quest, defeat that black jack dealing fool for me.",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_3_finish": NpcTextBox(
                [
                    "MC Nugg: You were the first to defeat Mack, such a nuggulous feat deserves the best reward.",
                    "I'll teach you this new spell, it's full of soul, you wont have to pay money for slots.",
                    "Sir Leopold: It's just a coin on a string...",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "final_message": NpcTextBox(
                [
                    "MC Nugg: Are you sure I can't serve you some chicken nuggets, I can lay you a fresh batch, extra greasy.",

                ],
                (50, 450, 50, 45), 30, 500
            ),

        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/chicken_sprites.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):

        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

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

                current_message = self.npc_messages["level_6_quest"]

                if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                        and Equipment.SOCKS_OF_PERCEPTION.value not in state.player.items:
                    current_message = self.npc_messages["quest_1_finish"]
                elif Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                        and Treasure.BBQ_SAUCE.value not in state.player.quest_items:

                    print("Yippy")
                    current_message = self.npc_messages["quest_2_start"]
                elif Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                        and Equipment.NUGG_QUEST_TWO_MONEY.value not in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_2_finish"]
                elif Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state \
                        and Equipment.NUGG_QUEST_TWO_MONEY.value in state.player.level_two_npc_state \
                        and Events.BLACK_JACK_BLACK_MACK_DEFEATED.value not in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_3_start"]
                elif Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                        and Magic.SLOTS_HACK.value not in state.player.magicinventory:
                    current_message = self.npc_messages["quest_3_finish"]
                elif Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["final_message"]

                current_message.reset()

    def update_talking(self, state: "GameState"):
        # this method casues it to skip to end of message this method is only temp



        current_message = self.npc_messages["level_6_quest"]

        if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                and Equipment.SOCKS_OF_PERCEPTION.value not in state.player.items:
            current_message = self.npc_messages["quest_1_finish"]
        elif Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                and Treasure.BBQ_SAUCE.value not in state.player.quest_items:

            print("Yippy")
            current_message = self.npc_messages["quest_2_start"]
        elif Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                and Equipment.NUGG_QUEST_TWO_MONEY.value not in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_2_finish"]
        elif Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state \
                and Equipment.NUGG_QUEST_TWO_MONEY.value in state.player.level_two_npc_state \
                and Events.BLACK_JACK_BLACK_MACK_DEFEATED.value not in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_3_start"]
        elif Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                and Magic.SLOTS_HACK.value not in state.player.magicinventory:
            current_message = self.npc_messages["quest_3_finish"]
        elif Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["final_message"]

        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            state.controller.isTPressed = False

            if (Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state and
                Events.MC_NUGGET_QUEST_2_REWARD.value not in state.player.level_two_npc_state) and \
                Equipment.SOCKS_OF_PERCEPTION.value in state.player.items:
                state.player.level_two_npc_state.append(Equipment.NUGG_QUEST_TWO_MONEY.value)
                state.player.money += 500
                state.player.level_two_npc_state.append(Events.MC_NUGGET_QUEST_2_REWARD.value)

            elif (Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state

                    and Magic.SLOTS_HACK.value not in state.player.magicinventory and \
                    Equipment.SOCKS_OF_PERCEPTION.value in state.player.items and \
                    Equipment.NUGG_QUEST_TWO_MONEY.value in state.player.level_two_npc_state):
                state.player.level_two_npc_state.append(Events.MC_NUGGET_QUEST_3_REWARD.value)

                state.player.magicinventory.append(Magic.SLOTS_HACK.value)


            elif (Events.MC_NUGGET_QUEST_1_REWARD.value in state.player.level_two_npc_state and
                    Equipment.SOCKS_OF_PERCEPTION.value not in state.player.items):
                print("niggles")
                state.player.items.append(Equipment.SOCKS_OF_PERCEPTION.value)
                Events.add_event_to_player(state.player, Events.MC_NUGGET_BETA_QUEST_COMPLETE)

                state.player.level_two_npc_state.append(Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value)


            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        # sprite_rect = pygame.Rect(15, 88, 30, 30)
        sprite_rect = pygame.Rect(55, 171, 44, 44)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        # scaled_sprite = pygame.transform.scale(sprite, (55, 55))
        scaled_sprite = pygame.transform.scale(sprite, (66, 66))

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":

            current_message = self.npc_messages["level_6_quest"]

            if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                    and Equipment.SOCKS_OF_PERCEPTION.value not in state.player.items:
                current_message = self.npc_messages["quest_1_finish"]
            elif Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                    and Treasure.BBQ_SAUCE.value not in state.player.quest_items:

                print("Yippy")
                current_message = self.npc_messages["quest_2_start"]
            elif Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                    and Equipment.NUGG_QUEST_TWO_MONEY.value not in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_2_finish"]
            elif Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state \
                    and Equipment.NUGG_QUEST_TWO_MONEY.value in state.player.level_two_npc_state \
                    and Events.BLACK_JACK_BLACK_MACK_DEFEATED.value not in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_3_start"]
            elif Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state \
                    and Magic.SLOTS_HACK.value not in state.player.magicinventory:
                current_message = self.npc_messages["quest_3_finish"]
            elif Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["final_message"]

            current_message.draw(state)

