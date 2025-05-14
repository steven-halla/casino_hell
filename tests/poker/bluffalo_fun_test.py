import random

class BluffTest:
    def __init__(self, enemy_score, enemy_pressure, player_bet, card_length):
        self.enemy_score = enemy_score
        self.enemy_pressure = enemy_pressure
        self.player_bet = player_bet
        self.enemy_hand = [("Dummy", "Suit", 0)] * card_length
        self.PLAYER_WINS = "PLAYER_WINS"
        self.ACTION_SCREEN = "ACTION_SCREEN"
        self.game_state = "BLUFFALO_SCREEN"

    def run_bluff_logic(self):
        card_modifier = len(self.enemy_hand) * 3

        if self.player_bet < 150:
            bet_modifier = 5
        elif self.player_bet < 250:
            bet_modifier = 15
        elif self.player_bet < 350:
            bet_modifier = 20
        else:
            bet_modifier = 30

        if self.enemy_pressure < 100:
            rand_range = 50 if self.enemy_score == 3 else 55
        else:
            rand_range = 60 if self.enemy_score == 3 else 65

        fold_chance = random.randint(1, rand_range) + bet_modifier + card_modifier

        print(f"Score={self.enemy_score}, Pressure={self.enemy_pressure}, Bet={self.player_bet}, Cards={len(self.enemy_hand)}, FoldChance={fold_chance}")

        if self.enemy_score > 4:
            self.game_state = self.ACTION_SCREEN
        elif fold_chance > 80:
            self.game_state = self.PLAYER_WINS
        else:
            self.enemy_pressure -= 10 if self.enemy_score == 3 else 15
            self.game_state = self.ACTION_SCREEN

        return self.game_state

# Example usage:
if __name__ == "__main__":
    tests = [
        (1, 30, 50, 3),
        (1, 110, 75, 3),
        (2, 50, 100, 4),
        (2, 130, 120, 3),
        (2, 90, 180, 5),
        (2, 140, 200, 4),
        (3, 40, 150, 3),
        (3, 95, 250, 5),
        (3, 110, 300, 4),
        (3, 80, 350, 5),
        (3, 60, 275, 4),
        (4, 90, 100, 3),
        (4, 120, 220, 3),
        (4, 100, 300, 4),
        (5, 80, 350, 3),
        (5, 100, 200, 5),
        (1, 85, 100, 4),
        (2, 70, 250, 5),
        (3, 95, 225, 4),
        (4, 60, 300, 3),
        (1, 99, 125, 3),
        (2, 101, 150, 4),
        (3, 89, 275, 5),
        (4, 110, 180, 3),
        (5, 115, 350, 5),
    ]

    for t in tests:
        test = BluffTest(*t)
        result = test.run_bluff_logic()
        print(f"-> Resulting state: {result}\n")
