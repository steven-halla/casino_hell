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
        if not self.has_black_jack_hat():
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

    def should_steal_ace(self, enemy_hand: list, ace_effect_triggered: bool, level_4_percentage_chance: int) -> bool:
        """
        Check if Sir Leopold's Amulet should steal an ace from the enemy.
        Returns True if an ace should be stolen, False otherwise.
        """
        if not self.has_sir_leopold_amulet():
            return False

        # Get spirit bonus from player
        spirit_bonus = self.player.spirit * 10
        sir_leopold_steal_roll = random.randint(1, 100) + spirit_bonus

        if sir_leopold_steal_roll > level_4_percentage_chance:
            if len(enemy_hand) > 1 and enemy_hand[1][0] == "Ace" and not ace_effect_triggered:
                return True

        return False
