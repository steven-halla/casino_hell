import pygame

from constants import DISPLAY
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.gui.textbox.text_box import TextBox
from screen.examples.screen import Screen
from deck import Deck
from entity.gui.textbox.bordered_box import BorderedBox

# if a player has 3 cards, then an ace value is equal to one
# ace should be set that if a value is less than 10, then at least one of them should be
# set to 11
# need to set up test cases for many up to having 4 aces in hand

# betting is also broken, a black jack should net X 2 winnings

class BlackJackThomasScreen(Screen):
    def __init__(self):
        Screen.__init__(self, " Black Jack Game")

        self.deck = Deck()
        self.font = pygame.font.Font(None, 36)
        self.black_ace = False  # this is our boss level when talk to NPC set to true set false if game is set to quit
        self.ace_up_sleeve_jack = False
        self.ace_up_sleeve_jack_cheat_mode = False
        self.first_message_display = ""
        self.second_message_display = ""
        self.third_message_display = ""
        self.game_state = "welcome_screen"
        self.bet = 10
        self.cheater_bob_money = 1000
        self.sir_leopold_ace_attack = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/startloadaccept.wav")  # Adjust the path as needed
        self.sir_leopold_ace_attack.set_volume(0.6)
        self.player_score = 0
        self.enemy_score = 0
        # self.player_cards_list = []
        # self.enemy_cards_list = []
        self.player_hand = []
        self.enemy_hand = []
        self.choices = ["Ready", "Draw", "Redraw"]
        self.current_index = 0
        self.welcome_screen_choices = ["Play", "Magic", "Quit"]
        self.welcome_screen_index = 0
        self.magic_menu_selector = ["Reveal", "Back"]
        self.magic_menu_index = 0
        self.ace_value = 1
        self.bust_protection = False
        self.avatar_of_luck_card_redraw_counter = 3
        self.spell_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)

        self.player_black_jack_win = False
        self.enemy_black_jack_win = False
        self.black_jack_draw = False

        self.current_speaker = ""
        self.npc_speaking = False
        self.hero_speaking = False
        self.music_loop = True

        self.despair = False
        # self.despair = True
        self.black_jack_thomas_defeated = False

        self.hero_losing_text_state = False
        self.hero_winning_text_state = False
        self.player_status = ""
        self.enemy_status = ""

        self.black_jack_bluff_counter = 0
        self.reveal_hand = 11
        self.magic_lock = False
        self.luck_of_jack = 7
        self.avatar_of_luck = False
        self.redraw_lock = False
        self.next_draw_time = pygame.time.get_ticks() + 2000  # Set initial delay for first draw


        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/black_jack_screen.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.music_on = True


        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)
        self.flip_timer = pygame.time.get_ticks() + 2000
        self.pause_timer = 0


        # maybe include a self.turn_counter = 0 that can be +1 in our welcome screen in conjection with our reveal spell
        # incldue a double bet spell that is CHR based that player gets for free maybe4

        self.locked_text = self.font.render("Locked", True, (255, 255, 255))

        self.messages = {
            "welcome_screen": ["Thomas: Press T key for all commands.",

                               "You look pretty fresh to me.","" ],
            "hero_intro_text": [
                "am I in trouble?",

                "I can press up and down to select. Play to start, quit to leave, or magic for an advantage", ""],

            "bet_intro_text": [
                "Thomas: Min Bet is 10 and Max Bet is 100. The more you bet the more your  stamina is drained."],

            "hero_losing_text": [
                "Hero: This isn't good, I'll need to get serious if I want to make a comeback.",
                "Maybe I should lower my bet until I get the hang of my enemy.",
                ""],
            "enemy_winning_text": [
                "Cheater Bob: HA HA HA! You really stepped in it now!",
                "Do you know what happens when people lose all of their coins?",
                "I bet you have no idea what this place really is.", ""],
            "hero_losing_confused_text": [
                "Hero: Doesn't matter to me much what kind of place this is. I always go where there is gambling.",
                "This guy really means business....I need to focus, and regain my composure.",
                "Why doesn't he hit on 16??? It's like he's afraid to bust for some reason.",
                ""],

            "enemy_losing_text": [
                "Cheater Bob: How is this possible? I'm....Cheater Bob...I'm not supposed to lose.",
                "Your Cheating! There is no way I'd lose to an amateur like you!",
                ""],
            "hero_winning_text": [
                "Hero: I never cheat Cheater Bob. I'm just that good. Why are you sweating so much for?",
                "Care to tell me why your so worried? It's not like their going to kill you or anything.",
                "I can now use my bluff attack.",
                "If I use it I won't be able to use any other magic till this match is over.",
                "Should I use it now or wait a little bit till I'm closer to dealing a final blow?",
                ""],
            "enemy_losing_confused_text": [
                "Cheater Bob: There are some fates worse than death, 'hero'.",
                ".......",
                "If you take all my coins, and if the boss doesn't give me replacement coins..........",
                "NO!!! I won't end up like the others....I won't have you make a fool out of me.....",
                ""],

            "final_strike_text": [
                "Hero: You don't have a lot of coins left. I'll bet you the rest that my next hand will be a black jack.",
                "Of course, if you happen to win you'll be back in the game, sounds pretty nice of me right?",
                "",
                ],
            "enemy_bluffed_text": [
                "Cheater Bob: Do you Realize the odds of that happening?",
                " Why would you take such a bet for?",
                "It doesn't make any sense.",
                ""],

            "hero_bluffing_text": [
                "Hero: Well it's simple really, based on the card positions, and the way you shuffled. ",
                "I can pretty easily tell where each card landed in the deck.",
                "Simply put, I'm not doing a random bet, or a bluff, when you deal out the cards, I will get a black jack. It's all about my intellect and high perception.",
                ""],
            "enemy_falling_for_bluff_text": [
                "Cheater Bob: That's bull crap, there's no way you have that much perception.  ",
                "I'll take your bet, and then I'll tell everyone how much of a fool you are.",
                "I'll teach you to underestimate me!", ""],

            "enemy_crying_text": ["Cheater Bob: Impossible...how did you????",
                                  ""],
            "hero_reveal_text": [
                "Hero: To be honest, it was all a bluff, you were right all along.",
                "However, I never bet against myself, and because of that lady luck is always on my side.",
                "You lost,not because I cheated, but  because you didnt' believe in yourself and gave in to despair.",
                ""],

            "bluff_magic_explain": [
                "Casts Bluff on the enemy. When the enemy seems desperate this will be unlocked. Enemy less likely to hit due to fear of a bust. Magic Lock Permanent .25MP"],
            "reveal_magic_explain": [
                "Based on muscle twitches of enemy plus the way they shuffle cards, you can tell what score they have.Protects you from busts. Magic lock 10 turns.25MP"],
            "avatar_magic_explain": [
                "Your faith is so strong that lady luck herself blesses you. Allows up to 3 redraws per turn.Deck is not reshuffled and cards are burned.Magic lock 5 turns 25MP"],
            "back_magic_explain": ["Back to previous gui"],

        }

        self.welcome_screen_text_box = TextBox(self.messages["welcome_screen"],
                                               (50, 450, 50, 45), 30, 500)
        self.welcome_screen_text_box_hero = TextBox(
            self.messages["hero_intro_text"], (50, 450, 50, 45), 30, 500)

        self.bet_screen_text = TextBox(self.messages["bet_intro_text"],
                                       (50, 450, 50, 45), 30, 500)
        self.hero_losing_money_text = TextBox(self.messages["hero_losing_text"],
                                              (50, 450, 50, 45), 30, 500)
        self.enemy_losing_money_text = TextBox(
            self.messages["enemy_losing_text"], (50, 450, 50, 45), 30, 500)

        self.enemy_winning_money_text = TextBox(
            self.messages["enemy_winning_text"], (50, 450, 50, 45), 30, 500)
        self.hero_winning_money_text = TextBox(
            self.messages["hero_winning_text"], (50, 450, 50, 45), 30, 500)

        self.hero_losing_confused_money_text = TextBox(
            self.messages["hero_losing_confused_text"], (50, 450, 50, 45), 30,
            500)
        self.enemy_losing_confused_money_text = TextBox(
            self.messages["enemy_losing_confused_text"], (50, 450, 50, 45), 30,
            500)

        self.final_strike_text_component = TextBox(
            self.messages["final_strike_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_bluffed_text_component = TextBox(
            self.messages["enemy_bluffed_text"], (50, 450, 50, 45), 30, 500)

        self.hero_bluffing_text_component = TextBox(
            self.messages["hero_bluffing_text"], (50, 450, 50, 45), 30, 500)
        self.enemy_falling_for_bluff_text_component = TextBox(
            self.messages["enemy_falling_for_bluff_text"], (50, 450, 50, 45),
            30, 500)

        self.enemy_crying_text_component = TextBox(
            self.messages["enemy_crying_text"], (50, 450, 50, 45), 30, 500)
        self.hero_reveal_text_component = TextBox(
            self.messages["hero_reveal_text"], (50, 450, 50, 45), 30, 500)

        self.bluff_magic_explain_component = TextBox(
            self.messages["bluff_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.reveal_magic_explain_component = TextBox(
            self.messages["reveal_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.avatar_magic_explain_component = TextBox(
            self.messages["avatar_magic_explain"], (50, 450, 50, 45), 30, 500)
        self.back_magic_explain_component = TextBox(
            self.messages["back_magic_explain"], (50, 450, 50, 45), 30, 500)

        # self.bordered_text_box = BorderedTextBox(self.messages["list2"], (230, 200, 250, 45), 30, 500)
        self.main_bordered_box = BorderedBox((25, 425, 745, 150))

        self.defeated_textbox = NpcTextBox(
            [
                "Guy:Looks like you defeated me.....back to eating chili for days and day and days....",

                "pro tip,for some reason the boss is scared of BUST, those demons sure do lick those chops when his cards get high",
            ""],
            (50, 450, 50, 45), 30, 500)

        self.reveal_debuff = False
        self.reveal_debuff_counter = 0




    pygame.init()
    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)

    def place_bet(self, state: "GameState"):
        if state.controller.isUpPressed:
            self.bet += 10
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(100)
            state.controller.isUpPressed = False

        elif state.controller.isDownPressed:
            self.bet -= 10
            self.menu_movement_sound.play()  # Play the sound effect once

            pygame.time.delay(100)
            state.controller.isDownPressed = False

        if self.bet < 10:
            self.bet = 10

        if self.bet > 100:
            self.bet = 100

        if self.bet > self.cheater_bob_money:
            self.bet = self.cheater_bob_money

    def update(self, state: "GameState"):
        if self.music_on == True:
            self.stop_music()
            self.initialize_music()
            self.music_on = False
        state.player.canMove = False


        controller = state.controller
        controller.update()
        state.player.update(state)

        if self.cheater_bob_money < 10:
            self.black_jack_thomas_defeated = True
            self.game_state = "defeated"

        if self.game_state == "defeated":
            print("enemy defeated")
            self.defeated_textbox.update(state)



        if self.game_state == "welcome_screen":

            if state.player.stamina_points < 1:
                print("time to leave")
            if self.cheater_bob_money < 10:
                print("time to be gone wit you")
                self.black_jack_thomas_defeated = True
                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)

            self.welcome_screen_text_box.update(state)

            self.npc_speaking = True
            self.hero_speaking = False


            self.redraw_lock = False
            self.ace_up_sleeve_jack_cheat_mode = False
            self.bust_protection = False
            self.avatar_of_luck_card_redraw_counter = 3
            self.current_index = 0
            self.enemy_score = 0



            if self.welcome_screen_text_box.message_index == 2:

                print("naw naw naw")
                self.npc_speaking = False
                self.hero_speaking = True
                # self.welcome_screen_text_box_hero.update(state)

                # if self.welcome_screen_text_box_hero.is_finished():

                if controller.isUpPressed:
                    self.menu_movement_sound.play()  # Play the sound effect once

                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) - 1
                    else:
                        self.welcome_screen_index -= 1
                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isUpPressed = False

                elif controller.isDownPressed:
                    self.menu_movement_sound.play()
                    if not hasattr(self, "welcome_screen_index"):
                        self.welcome_screen_index = len(
                            self.welcome_screen_choices) + 1
                    else:
                        self.welcome_screen_index += 1

                    self.welcome_screen_index %= len(
                        self.welcome_screen_choices)
                    controller.isDownPressed = False

        elif self.game_state == "hero_is_desperate_state":
            self.npc_speaking = False
            self.hero_speaking = True
            self.hero_losing_money_text.update(state)

            self.hero_losing_text_state = True

            if self.hero_losing_money_text.is_finished():
                self.npc_speaking = True
                self.hero_speaking = False
                self.enemy_winning_money_text.update(state)
                if self.enemy_winning_money_text.is_finished():
                    self.npc_speaking = False
                    self.hero_speaking = True
                    self.hero_losing_confused_money_text.update(state)
                    if self.hero_losing_confused_money_text.is_finished():
                        self.game_state = "welcome_screen"

        elif self.game_state == "enemy_is_desperate_state":
            self.npc_speaking = True
            self.hero_speaking = False
            self.enemy_losing_money_text.update(state)

            self.hero_winning_text_state = True

            if self.enemy_losing_money_text.is_finished():
                self.npc_speaking = False
                self.hero_speaking = True
                self.hero_winning_money_text.update(state)
                if self.hero_winning_money_text.is_finished():
                    self.npc_speaking = True
                    self.hero_speaking = False
                    self.enemy_losing_confused_money_text.update(state)
                    if self.enemy_losing_confused_money_text.is_finished():
                        self.game_state = "welcome_screen"

        elif self.game_state == "bet_phase":

            self.bet_screen_text.update(state)

            self.npc_speaking = True
            self.hero_speaking = False

            self.third_message_display = " "
            self.place_bet(state)
            if self.bet_screen_text.current_message_finished():
                print("done")

                if controller.isTPressed:
                    if self.bet > 70:
                        state.player.stamina_points -= 3
                        print("-3")
                    elif self.bet < 30:

                        state.player.stamina_points -= 1

                        print("-1")
                    elif self.bet < 70 or self.bet > 20:
                        state.player.stamina_points -= 2
                        print("-2")

                    pygame.time.wait(300)
                    self.game_state = "draw_phase"
                    controller.isTPressed = False

        elif self.game_state == "draw_phase":
            self.first_message_display = ""
            self.second_message_display = ""
            self.thrid_message_display = ""
            self.black_jack_counter = 0
            self.player_black_jack_win = False
            self.enemy_black_jack_win = False
            self.black_jack_draw = False
            self.player_hand = self.deck.player_draw_hand(2)
            print("Player hand is" + str(self.player_hand))
            self.player_score = self.deck.compute_hand_value(self.player_hand)
            print("Player score is: " + str(self.player_score))

            # Check if the player has an ACE in their hand
            if self.black_jack_counter > 0:
                print("Player black jack win set to true and it might be true?")
                self.player_black_jack_win = True
                self.black_jack_bluff_counter += 1
            else:
                self.player_black_jack_win = False

            aces_to_remove = [
                ('Ace', 'Hearts', 11),
                ('Ace', 'Spades', 11),
                ('Ace', 'Diamonds', 11),
                ('Ace', 'Clubs', 11),
                ('Ace', 'Hearts', 1),
                ('Ace', 'Spades', 1),
                ('Ace', 'Diamonds', 1),
                ('Ace', 'Clubs', 1),
            ]

            self.enemy_hand = self.deck.enemy_draw_hand(2)
            print("Enemy hand is" + str(self.enemy_hand))
            self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
            print("enemy score is: " + str(self.enemy_score))
            while self.enemy_score > 17:
                print("Redrawing hand, score too high: " + str(self.enemy_score))
                # Empty the enemy_hand array
                self.enemy_hand = []
                # Draw a new hand
                self.enemy_hand = self.deck.enemy_draw_hand(2)
                print("New enemy hand is: " + str(self.enemy_hand))
                # Compute the score of the new hand
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                print("New enemy score is: " + str(self.enemy_score))
            if "sir leopold's paw" in state.player.items:

                for card in self.enemy_hand:
                    if card in aces_to_remove:
                        self.enemy_hand.remove(card)
                        print(f"jdsajf;lsjlafjsafjsa;flj Hedgehog swiped an Ace! Removed card: {card}")
                        self.sir_leopold_ace_attack.play()  # Play the sound effect once

                        self.enemy_hand += self.deck.enemy_draw_hand(1)

                        break

            if self.black_jack_counter > 0:
                print(
                    "Enemy black jack win set to true and the code is right here")
                self.enemy_black_jack_win = True
            elif self.black_jack_counter == 0:
                self.enemy_black_jack_win = False

            print(self.player_black_jack_win)

            if self.black_ace == True:
                if self.enemy_score < 7:
                    self.enemy_hand = self.deck.enemy_draw_hand(2)
                    print("Enemy hand is" + str(self.enemy_hand))
                    print("You get the sense the enemy is somewhat lucky")
                    self.enemy_score = self.deck.compute_hand_value(
                        self.enemy_hand)
                    print("enemy score is: " + str(self.enemy_score))
                    if self.black_jack_counter > 0:
                        print("Enemy black jack win set to true")

                        self.enemy_black_jack_win = True
                    elif self.black_jack_counter == 0:
                        self.enemy_black_jack_win = False

                    print(self.player_black_jack_win)

            if self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.black_jack_draw = True
                self.thrid_message_display = "Its a draw"
                print("Its a draw")
                self.game_state = "results_screen"
            elif self.player_black_jack_win == True and self.enemy_black_jack_win == False:

                print("its time for you to have double winnings")
                # state.player.money += self.bet
                # state.player.money += self.bet
                # self.cheater_bob_money -= self.bet
                # self.cheater_bob_money -= self.bet
                self.game_state = "results_screen"
            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                print("THE ENEMY HAS A BLAK Jack SORRRYYYYYY")
                # state.player.money -= self.bet
                # state.player.money -= self.bet
                # self.cheater_bob_money += self.bet
                # self.cheater_bob_money += self.bet

                self.game_state = "results_screen"

            else:
                self.game_state = "menu_screen"



        elif self.game_state == "player_draw_one_card":
            self.player_hand += self.deck.player_draw_hand(1)
            self.deck.compute_hand_value(self.player_hand)
            self.player_score = self.deck.compute_hand_value(self.player_hand)

            if self.player_score > 10:
                print("hi greater than 10")
                self.deck.rank_values["Ace"] = 1

            print("Player hand is now" + str(self.player_hand))
            print("Player score is now" + str(self.player_score))
            if self.player_score > 21:
                state.player.money -= self.bet
                self.cheater_bob_money += self.bet

                if state.player.level == 1:
                    state.player.exp += 5
                    self.first_message_display = f"You gain 5 exp and lose {self.bet} gold "
                elif state.player.level == 2:
                    state.player.exp += 2
                    self.first_message_display = f"You gain 2 exp and lose {self.bet} gold "
                self.second_message_display = "player bust you lose"
                self.game_state = "results_screen"

            elif self.player_score > 21 and self.reveal_hand < 11:
                print("you almost busted")
                print(self.player_hand)
                self.player_hand.pop()
                self.deck.compute_hand_value(self.player_hand)
                self.player_score = self.deck.compute_hand_value(
                    self.player_hand)
                print("here is your new hand")
                print(self.player_hand)
                self.reveal_hand -= 2
                self.bust_protection = True

            if self.bust_protection == True:
                self.game_state = "results_screen"
            else:
                self.game_state = "menu_screen"

        elif self.game_state == "enemy_draw_one_card":
            print("this is the start of enemy draw one card")
            current_time = pygame.time.get_ticks()

            while self.enemy_score < 13:  # this is 15 in order to make game a little easier
                print("thi sis our while loop")



                self.enemy_hand += self.deck.enemy_draw_hand(1)
                self.deck.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"

                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.money += self.bet
                    self.cheater_bob_money -= self.bet
                    print("enemy bust")
                    if state.player.level == 1:
                        state.player.exp += 12
                        self.first_message_display = f"You gain 12 exp and lose {self.bet} gold "
                    elif state.player.level == 2:
                        state.player.exp += 6
                        self.first_message_display = f"You gain 6 exp and lose {self.bet} gold "
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 12 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"

        elif self.game_state == "enemy_despair_draw_one_card":
            print("enemy is in despair")
            while self.enemy_score < 14:  # this is 15 in order to make game a little easier
                print("this is our despair loop")

                self.enemy_hand += self.deck.enemy_draw_hand(1)
                self.deck.compute_hand_value(self.enemy_hand)
                self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
                print("enemy hand is now" + str(self.enemy_hand))
                print("enemy score is now" + str(self.enemy_score))
                self.game_state = "results_screen"

                if self.enemy_score > 21:
                    print("if the enemy is going to bust")
                    state.player.money += self.bet
                    self.cheater_bob_money -= self.bet
                    print("enemy bust")
                    self.second_message_display = "enemy bust player wins"
                    self.game_state = "results_screen"

            if self.enemy_score > 14 and self.enemy_score < 22:
                print("stay here")
                self.game_state = "results_screen"




        elif self.game_state == "menu_screen":

            if self.player_score > 21:
                self.message_display = "You bust and lose."
                # state.player.money -= self.bet
                # self.cheater_bob_money += self.bet
                self.game_state = "results_screen"

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) - 1
                else:
                    self.current_index -= 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isUpPressed = False

            if controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "current_index"):
                    self.current_index = len(self.choices) + 1
                else:
                    self.current_index += 1
                self.current_index %= len(self.choices)
                print(self.choices[self.current_index])
                controller.isDownPressed = False

            if self.current_index == 2 and state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                print("Redrawing your hand")
                self.player_hand = self.deck.player_draw_hand(
                    2)  # no need to call self.player_hand.clear() befoe this, as we are already overriding it here
                print("Player hand is" + str(self.player_hand))
                print("Enemy hand is" + str(self.enemy_hand))
                print("player card list is " + str(self.player_hand))
                print("enemy card list is " + str(self.enemy_hand))
                self.player_score = self.deck.compute_hand_value(
                    self.player_hand)
                self.avatar_of_luck_card_redraw_counter -= 1

                if self.avatar_of_luck_card_redraw_counter < 1:
                    self.redraw_lock = True

                self.game_state = "menu_screen"
                state.controller.isTPressed = False

                # 534534543535353525532535353354

        elif self.game_state == "magic_menu":

            self.message_display = "Pick a magic spell and wreck havic. Press K to cast"

            if controller.isUpPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) - 1
                else:
                    self.magic_menu_index -= 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isUpPressed = False

            elif controller.isDownPressed:
                self.menu_movement_sound.play()  # Play the sound effect once

                # channel3 = pygame.mixer.Channel(3)
                # sound3 = pygame.mixer.Sound("audio/Fotstep_Carpet_Right_3.mp3")
                # channel3.play(sound3)
                if not hasattr(self, "magic_menu_index"):
                    self.magic_menu_index = len(self.magic_menu_selector) + 1
                else:
                    self.magic_menu_index += 1
                self.magic_menu_index %= len(self.magic_menu_selector)
                controller.isDownPressed = False


            if self.magic_menu_index == 0:
                self.reveal_magic_explain_component.update(state)

                if controller.isTPressed:
                    # channel3 = pygame.mixer.Channel(3)
                    # sound3 = pygame.mixer.Sound("audio/SynthChime5.mp3")
                    # channel3.play(sound3)
                    if state.player.focus_points >= 10:

                        state.player.focus_points -= 10
                        self.spell_sound.play()  # Play the sound effect once


                        self.reveal_hand = 10
                        self.reveal_debuff = True
                        self.reveal_debuff_counter = 10
                        self.magic_lock = True
                        self.player_status = "Focus"
                        self.enemy_status = "Reveal"
                        self.isTPressed = False

                        print("You cast reveal")
                        self.game_state = "welcome_screen"


                    elif state.player.focus_points < 10:
                        self.third_message_display = "Sorry but you dont have enough focus points to cast"


            elif self.magic_menu_index == 1:
                self.back_magic_explain_component.update(state)

                if controller.isTPressed:
                    print(str(controller.isTPressed))
                    controller.isTPressed = False
                    print(str(controller.isTPressed))


                    self.game_state = "welcome_screen"
                    self.isTPressed = False
                    print(str(controller.isTPressed))



        elif self.game_state == "results_screen":

            if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                self.second_message_display = "You win with a black jack press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and {self.bet * 2} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and {self.bet * 2} gold "


            elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                self.second_message_display = "It's a draw press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and 0 gold "


            elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                self.second_message_display = "Enemy gets blackjack you lose "
                if state.player.level == 1:
                    self.first_message_display = f"You gain 100 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 50 exp and 0 gold "



            elif self.player_score > self.enemy_score and self.player_score < 22:
                self.second_message_display = "You win player press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 25 exp and {self.bet} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 12 exp and {self.bet} gold "




            elif self.player_score < self.enemy_score and self.enemy_score < 22:
                self.second_message_display = "You lose player press T when ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 50 exp and lose {self.bet} gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 25 exp and lose {self.bet} gold "




            elif self.player_score == self.enemy_score:
                self.second_message_display = "It's a draw nobody wins press T when Ready"
                if state.player.level == 1:
                    self.first_message_display = f"You gain 25 exp and 0 gold "
                elif state.player.level == 2:
                    self.first_message_display = f"You gain 12 exp and 0 gold "

            if controller.isTPressed:



                if self.player_black_jack_win == True and self.enemy_black_jack_win == False:
                    state.player.money += self.bet * 2
                    self.cheater_bob_money -= self.bet * 2
                    if state.player.level == 1:
                        state.player.exp += 50

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and {self.bet * 2} gold "

                        state.player.exp += 25


                elif self.player_black_jack_win == True and self.enemy_black_jack_win == True:
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 50 exp and 0 gold "

                        state.player.exp += 75
                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 25 exp and 0 gold "

                        state.player.exp += 33


                elif self.player_black_jack_win == False and self.enemy_black_jack_win == True:
                    state.player.money -= self.bet * 2
                    self.cheater_bob_money += self.bet * 2
                    if state.player.level == 1:
                        state.player.exp += 100

                    elif state.player.level == 2:
                        state.player.exp += 50



                elif self.player_score > self.enemy_score and self.player_score < 22:
                    self.second_message_display = "You win player press T when ready"

                    state.player.money += self.bet
                    self.cheater_bob_money -= self.bet
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 25 exp and {self.bet} gold "

                        state.player.exp += 25

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and {self.bet} gold "

                        state.player.exp += 12


                elif self.player_score < self.enemy_score and self.enemy_score < 22:
                    self.second_message_display = "You lose player press T when ready"
                    state.player.money -= self.bet
                    self.cheater_bob_money += self.bet
                    if state.player.level == 1:
                        self.first_message_display = f"You gain 50 exp and lose {self.bet} gold "

                        state.player.exp += 50
                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 25 exp and lose {self.bet} gold "

                        state.player.exp += 25



                elif self.player_score == self.enemy_score:
                    self.second_message_display = "It's a draw nobody wins press T when Ready"

                    if state.player.level == 1:
                        self.first_message_display = f"You gain 25 exp and 0 gold "

                        state.player.exp += 25

                    elif state.player.level == 2:
                        self.first_message_display = f"You gain 12 exp and 0 gold "

                        state.player.exp += 12

                if self.reveal_hand < 11:
                    self.reveal_hand -= 1

                if self.reveal_hand == 0:
                    print("Magic time")
                    self.reveal_hand = 11
                    self.magic_lock = False

                if self.luck_of_jack < 7:
                    self.luck_of_jack -= 1

                if self.luck_of_jack == 0:
                    print("Magic time")
                    self.luck_of_jack = 6
                    self.avatar_of_luck = False
                    self.magic_lock = False

                pygame.time.wait(300)
                print("Hey there going to the welcome_screen")

                self.game_state = "welcome_screen"
                controller.isTPressed = False

    def hand_to_str(self, hand) -> str:
        msg = ""
        i = 0
        for card in hand:
            if i > 0:
                msg += ", "
            msg += card[0] + " " + card[1]
            i += 1
        return msg

    def draw(self, state: "GameState"):
        # change to dealer image
        # character_image = pygame.image.load("images/128by128.png")
        # hero_image = pygame.image.load("images/hero.png")

        state.DISPLAY.fill((0, 0, 51))

        black_box = pygame.Surface((200 - 10, 180 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 235))

        black_box = pygame.Surface((200 - 10, 45 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 45 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 195))

        state.DISPLAY.blit(self.font.render(f"Money: {state.player.money}", True,
                                      (255, 255, 255)), (37, 250))
        state.DISPLAY.blit(
            self.font.render(f"HP: {state.player.stamina_points}", True,
                             (255, 255, 255)), (37, 290))

        state.DISPLAY.blit(self.font.render(f"MP: {state.player.focus_points}", True,
                                      (255, 255, 255)), (37, 330))
        state.DISPLAY.blit(
            self.font.render(f"Bet: {self.bet}", True, (255, 255, 255)),
            (37, 370))

        state.DISPLAY.blit(self.font.render(f"Hero", True, (255, 255, 255)),
                     (37, 205))

        black_box = pygame.Surface((200 - 10, 110 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 110 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 20))

        black_box = pygame.Surface((200 - 10, 130 - 10))
        black_box.fill((0, 0, 0))
        border_width = 5
        white_border = pygame.Surface(
            (200 - 10 + 2 * border_width, 130 - 10 + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(black_box, (border_width, border_width))
        state.DISPLAY.blit(white_border, (25, 60))

        state.DISPLAY.blit(self.font.render(f"Money: {self.cheater_bob_money}", True,
                                      (255, 255, 255)), (37, 70))
        state.DISPLAY.blit(self.font.render(f"Status: {self.enemy_status}", True,
                                      (255, 255, 255)), (37, 110))

        if self.reveal_hand < 11:
            state.DISPLAY.blit(self.font.render(f"Score: {self.enemy_score}", True,
                                          (255, 255, 255)),
                         (37, 150))
        elif self.reveal_hand > 10:
            state.DISPLAY.blit(self.font.render(f"Score:", True, (255, 255, 255)),
                         (37, 150))

        state.DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)),
                     (37, 30))

        self.main_bordered_box.draw(state)
        # state.DISPLAY.blit(character_image, (633, 15))
        state.DISPLAY.blit(self.font.render(f"Cheater Bob", True, (255, 255, 255)),
                     (625, 145))

        # self.face_down_card((0,0))

        if self.game_state == "welcome_screen":
            #
            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill((0, 0, 0))
            border_width = 5
            white_border = pygame.Surface(
                (160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))
            state.DISPLAY.blit(white_border, (620, 235))

            state.DISPLAY.blit(
                self.font.render(f"{self.welcome_screen_choices[0]}", True,
                                 (255, 255, 255)),
                (687, 260))

            if self.magic_lock == False:

                state.DISPLAY.blit(
                    self.font.render(f"{self.welcome_screen_choices[1]}", True,
                                     (255, 255, 255)),
                    (687, 310))
            elif self.magic_lock == True:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)),
                             (680, 315))

            state.DISPLAY.blit(
                self.font.render(f"{self.welcome_screen_choices[2]}", True,
                                 (255, 255, 255)),
                (687, 360))

            if self.welcome_screen_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 255))

                if state.controller.isTPressed and self.welcome_screen_text_box.is_finished():
                    self.deck.shuffle()

                    self.game_state = "bet_phase"
                    state.controller.isTPressed = False



            elif self.welcome_screen_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 305))
                if state.controller.isTPressed and self.magic_lock == False:
                    pygame.time.wait(300)
                    self.game_state = "magic_menu"
                    self.isTPressed = False



            elif self.welcome_screen_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 355))
                if state.controller.isTPressed:
                    print("Quit")
                    state.player.canMove = True
                    self.music_on = True

                    state.currentScreen = state.gamblingAreaScreen
                    state.gamblingAreaScreen.start(state)
                    state.controller.isTPressed = False

            self.welcome_screen_text_box.draw(state)
            # self.welcome_screen_text_box_hero.draw(state)
            # self.bordered_text_box.draw(state)

        elif self.game_state == "defeated":
            print("enemy defeated")
            self.defeated_textbox.draw(state)
            if self.defeated_textbox.message_index == 2:
                print("moogles")
                state.player.canMove = True

                state.currentScreen = state.gamblingAreaScreen
                state.gamblingAreaScreen.start(state)

        elif self.game_state == "hero_is_desperate_state":
            self.hero_losing_money_text.draw(state)
            self.enemy_winning_money_text.draw(state)
            self.hero_losing_confused_money_text.draw(state)


        elif self.game_state == "enemy_is_desperate_state":
            self.enemy_losing_money_text.draw(state)
            self.hero_winning_money_text.draw(state)
            self.enemy_losing_confused_money_text.draw(state)


        elif self.game_state == "bet_phase":
            self.bet_screen_text.draw(state)

            # self.current_speaker = "cheater bob"

            # state.DISPLAY.blit(character_image, (23, 245))
            # state.DISPLAY.blit(self.font.render(f"{self.current_speaker}", True, (255, 255, 255)), (155, 350))

            state.DISPLAY.blit(self.font.render(f"Your Current bet:{self.bet}", True,
                                          (255, 255, 255)), (50, 530))
            state.DISPLAY.blit(self.font.render(f"v", True, (255, 255, 255)),
                         (260, 550))
            state.DISPLAY.blit(self.font.render(f"^", True, (255, 255, 255)),
                         (257, 510))


        elif self.game_state == "menu_screen":
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15

            for i, card in enumerate(self.player_hand):
                if i > 3:
                    player_card_y = 305
                    player_card_x = 235
                self.deck.draw_card_face_up(card[1], card[0], (player_card_x, player_card_y), DISPLAY)

                player_card_x += 75

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(self.enemy_hand):
                if index == 0:
                    self.deck.draw_card_face_down((enemy_card_x, enemy_card_y), state.DISPLAY)
                else:
                    self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), state.DISPLAY)
                enemy_card_x += 75

            black_box = pygame.Surface((160 - 10, 180 - 10))
            black_box.fill((0, 0, 0))
            border_width = 5
            white_border = pygame.Surface(
                (160 - 10 + 2 * border_width, 180 - 10 + 2 * border_width))
            white_border.fill((255, 255, 255))
            white_border.blit(black_box, (border_width, border_width))
            state.DISPLAY.blit(white_border, (620, 235))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[0]}", True, (255, 255, 255)),
                (687, 260))

            state.DISPLAY.blit(
                self.font.render(f"{self.choices[1]}", True, (255, 255, 255)),
                (687, 310))

            if self.avatar_of_luck == True and self.redraw_lock == False:
                state.DISPLAY.blit(self.font.render("Redraw", True, (255, 255, 255)),
                             (687, 360))

            elif self.avatar_of_luck == False or self.redraw_lock == True:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)),
                             (687, 360))
            else:
                state.DISPLAY.blit(self.font.render("Locked", True, (255, 255, 255)),
                             (687, 360))

            if self.current_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 255))
                if state.controller.isTPressed:
                    pygame.time.wait(300)

                    print("code is broke right here")
                    if self.despair == False:
                        self.game_state = "enemy_draw_one_card"
                    elif self.despair == True:
                        self.game_state = "enemy_despair_draw_one_card"
                    state.controller.isTPressed = False


            elif self.current_index == 1:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 305))
                if state.controller.isTPressed:
                    pygame.time.wait(300)
                    print("Time to draw a card")
                    self.game_state = "player_draw_one_card"
                    self.isTPressed = False



            elif self.current_index == 2:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (637, 355))

                if state.controller.isTPressed and self.avatar_of_luck == True and self.redraw_lock == False:
                    pygame.display.update()
                    self.game_state = "menu_screen"



        elif self.game_state == "magic_menu":

            black_box = pygame.Surface((255, 215))
            black_box.fill((0, 0, 0))
            # Create the white border
            border_width = 5
            white_border = pygame.Surface(
                (170 + 2 * border_width, 215 + 2 * border_width))
            white_border.fill((255, 255, 255))
            black_box = pygame.Surface((170, 215))
            black_box.fill((0, 0, 0))
            white_border.blit(black_box, (border_width, border_width))
            state.DISPLAY.blit(white_border, (620 - 20, 190))
            if self.magic_menu_index == 0:
                state.DISPLAY.blit(
                    self.font.render(f"->", True, (255, 255, 255)),
                    (640, 200))
                # state.DISPLAY.blit(
                #     self.font.render("Bluff status. When enemy ", True, (255, 255, 255)),
                #     (40, 445))
                self.reveal_magic_explain_component.draw(state)




            elif self.magic_menu_index == 1:

                state.DISPLAY.blit(

                    self.font.render(f"->", True, (255, 255, 255)),

                    (640, 250))

                self.back_magic_explain_component.draw(state)



            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[0]}", True,
                                 (255, 255, 255)),
                (680, 205))

            state.DISPLAY.blit(
                self.font.render(f"{self.magic_menu_selector[1]}", True,
                                 (255, 255, 255)),
                (680, 255))








        elif self.game_state == "results_screen":
            player_card_x = 235
            player_card_y = 195
            enemy_card_x = 235
            enemy_card_y = 15

            for i, card in enumerate(self.player_hand):
                if i > 3:
                    player_card_y = 305
                    player_card_x = 235
                self.deck.draw_card_face_up(card[1], card[0], (player_card_x, player_card_y), DISPLAY)

                player_card_x += 75

                # pygame.display.update()

            # pygame.display.update()

            for index, card in enumerate(self.enemy_hand):
                self.deck.draw_card_face_up(card[1], card[0], (enemy_card_x, enemy_card_y), DISPLAY)

                enemy_card_x += 75

            state.DISPLAY.blit(self.font.render(f"{self.current_speaker}", True,
                                          (255, 255, 255)), (155, 350))

            state.DISPLAY.blit(
                self.font.render(f"{self.second_message_display}", True,
                                 (255, 255, 255)), (45, 450))
            state.DISPLAY.blit(self.font.render(f"{self.first_message_display}", True,
                                          (255, 255, 255)), (45, 500))
        pygame.display.flip()
