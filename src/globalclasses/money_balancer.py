class MoneyBalancer:
    def __init__(self, money: int) -> None:
        self.money = money

    def balance_money(self, state: "GameState", initial_enemy_money: int) -> None:
        if self.money < 0:
            print("money is at 0")
            amount_needed = initial_enemy_money
            state.player.money += amount_needed
            self.money = 0
