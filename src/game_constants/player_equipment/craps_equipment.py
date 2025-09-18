import random


class CrapsEquipment:
    def __init__(self, state):
        self.state = state
        self.player = state.player
        self.CHICKEN_NUGGER_SUCCESS_BONUS = (random.randint(1, 100)) + state.player.spirit * 5
        self.PLAYER_LOSE_ROLL = (self.state.player.current_stage * 5) + 50


    # def chicken_nugger_amulet(self, state):
    #     lucky_roll = random.randint(1, 100)
    #     # Get spirit bonus from player
    #
    #     # Hat chance decreases as floors increase
    #     min_roll_for_success = (self.state.player.current_stage * 5) + 50
    #     adjusted_roll = (self.state.player.spirit * 10)
    #     player_roll = lucky_roll + adjusted_roll
    #
    #     if player_roll >= min_roll_for_success:
    #         pass
