


from entity.gui.textbox.text_box import TextBox

class GameOver:
    def __init__(self):
        pass

    def player_dead(self, state: "GameState"):
        if state.player.money <= 0:
            state.game_over_message = TextBox(
                ["You are out of money. Game over!"],
                (65, 460, 700, 130),
                36,
                500
            )
            print("You are out of money")

        if state.player.stamina_points <= 0:
            state.game_over_message = TextBox(
                ["You are out of stamina. Game over!"],
                (65, 460, 700, 130),
                36,
                500
            )
            print("You are out of stamina")
