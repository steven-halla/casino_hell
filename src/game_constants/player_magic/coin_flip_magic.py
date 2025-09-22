import random


class CoinFlipMagic:
    def __init__(self, state):
        self.player = state.player
        self.state = state
        self.shield_duration = 3
        self.shield_cost = 10
        self.HEADS_FORCE_COST = 10
        self.HEADS_FORCE_SUCCESS_CHANCE = state.player.mind * 10
        self.HEADS_FORCE_ENEMY_DEFENSE = random.randint(1, 100) + (state.player.current_stage * 5)




    def cast_shield(self):
        self.state.player.focus_points -= self.shield_cost
        return self.shield_duration

    def shield_outcome(self, coin_landed: str, player_choice: str, shield_debuff: int, magic_bonus: int) -> str:
        if coin_landed != player_choice and shield_debuff > 0:
            shield_roll = random.randint(1, 100)
            min_roll_for_success = (self.state.player.current_stage * 5) + 50

            adjusted_roll = magic_bonus
            total_roll = shield_roll + adjusted_roll

            print("SHIELD ROLL IS:", total_roll)

            if total_roll > min_roll_for_success:
                return "PLAYER_DRAW_SCREEN"
            return "PLAYER_LOSE_SCREEN"

        return "PLAYER_LOSE_SCREEN"
