
class SlotsMagic:
    def __init__(self, state):
        self.state = state
        self.player = state.player
        self.SLOTS_MP_COST = 100

        self.SLOTS_HACK_DURATION = state.player.mind + 5
