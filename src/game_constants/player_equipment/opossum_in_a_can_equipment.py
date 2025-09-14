import random
from game_constants.equipment import Equipment

class OpossumInACanEquipment:
    def __init__(self, state):
        self.state = state
        self.player = state.player
        self.POISION_RESIST = self.player.spirit * 10





