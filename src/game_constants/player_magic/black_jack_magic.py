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


