
class ExpGain:
    def __init__(self) -> None:
        pass

    def gain_exp(self, state: "GameState", exp: int) -> None:
        # print("Your exp before: " + str(state.player.exp))
        state.player.exp += exp
        # print("Your exp after: " + str(state.player.exp))



