class MoneyBalancer:
    def __init__(self, money: int) -> None:
        self.money = money

    def balance_money(self, state: "GameState", initial_enemy_money: int) -> None:
        if self.money < 0:
            amount_needed = initial_enemy_money  # Amount of gold the enemy had before it fell below zero
            state.player.money += amount_needed  # Add this amount to the player's money
            self.money = 0
