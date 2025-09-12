import random
from game_constants.equipment import Equipment

class BlackJackEquipment:
    def __init__(self, state):
        """
        Equipment effects specific to Black Jack.
        Stores state so it has direct access to player and game data.
        """
        self.state = state
        self.player = state.player

    def has_black_jack_hat(self) -> bool:
        """Check if the player has the Black Jack Hat equipped."""
        return Equipment.BLACK_JACK_HAT.value in self.player.equipped_items

    def has_sir_leopold_amulet(self) -> bool:
        """Check if the player has Sir Leopold's Amulet equipped."""
        return Equipment.SIR_LEOPOLD_AMULET.value in self.player.equipped_items

    def handle_bust_protection(self, player_hand: list, player_score: int) -> bool:
        """
        Handle bust protection with Black Jack Hat.
        Returns True if the player is protected from busting, False otherwise.
        """
        if Equipment.BLACK_JACK_HAT.value not in self.player.equipped_items:
            return False

        # Generate lucky roll internally
        lucky_roll = random.randint(1, 100)
        # Get spirit bonus from player

        # Hat chance decreases as floors increase
        min_roll_for_success = (self.state.player.current_stage * 5) + 50
        adjusted_roll = (self.state.player.spirit * 10)
        player_roll = lucky_roll + adjusted_roll

        if player_roll >= min_roll_for_success:
            print("no bust line 35 black jack equpiment")

            # Bust prevented
            return True

        print("yes bust line 40 black jack equpiment")
        return False


    def should_steal_ace(self, enemy_hand: list, deck, ace_effect_triggered: bool) -> bool:
        """
        Sir Leopold's Amulet: If roll succeeds and enemy_hand[1] is an Ace and
        effect hasn't triggered, pop it and replace with a new card.
        Mutates enemy_hand. Returns True iff effect applied.
        """
        if Equipment.SIR_LEOPOLD_AMULET.value not in self.player.equipped_items:
            return False
        if ace_effect_triggered:
            return False

        # roll logic
        lucky_roll = random.randint(1, 100)
        min_roll_for_success = (self.state.player.current_stage * 5) + 50
        adjusted_roll = self.state.player.spirit * 10
        player_roll = lucky_roll + adjusted_roll

        if player_roll >= min_roll_for_success and len(enemy_hand) > 1 and enemy_hand[1][0] == "Ace":
            # POP/INSERT on the PARAM, not self
            enemy_hand.pop(1)
            new_card = deck.enemy_draw_hand(1)[0]
            enemy_hand.insert(1, new_card)
            print("Hell yeah you got that ace bro")
            return True

        print("no ace for you home slice")
        return False
