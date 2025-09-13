import random



class BlackJackMagic:
    def __init__(self, state):
        """
        Magic effects specific to Black Jack.
        Stores state so it has direct access to player and game data.
        """
        self.state = state
        self.player = state.player

        # duration scales with player's mind
        self.REVEAL_DURATION = 7 + self.player.mind
        self.REVEAL_MP_COST = 40

        self.REDRAW_DURATION = 7
        self.REDRAW_MP_COST = 40

    def force_enemy_redraw_faceup(self, enemy_hand: list, deck) -> bool:
        """
        Attempt to replace the enemy's face-up card (index 1) this turn.
        Returns True on success (card replaced), False on failure.
        NOTE: Caller is responsible for consuming per-turn flags (e.g., redraw_counter).
        """
        faceup_index = 1
        if len(enemy_hand) <= faceup_index:
            return False

        # Roll gating (your logic, using self.state / self.player)
        lucky_roll = random.randint(1, 100)
        min_roll_for_success = (self.state.player.current_stage * 5) + 50
        adjusted_roll = self.state.player.mind * 10
        player_roll = lucky_roll + adjusted_roll

        if player_roll >= min_roll_for_success:
            print("busting makes me feel good")
            new_card = deck.enemy_draw_hand(1)[0]
            enemy_hand[faceup_index] = new_card
            return True

        print("busting makes me feel sic")
        return False




