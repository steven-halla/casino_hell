import random


class CrapsMagic:
    def __init__(self, state):
        self.state = state
        self.player = state.player
        self.LUCKY_7_MP_COSTS = 25
        self.LUCKY_7_DURATION = state.player.mind + 5

    @staticmethod
    def apply_lucky_seven_buff(
            lucky_seven_buff_counter: int,
            dice_roll_1: int,
            dice_roll_2: int,
            come_out_roll_total: int,
    ) -> tuple[int, int]:
        point_roll_total = dice_roll_1 + dice_roll_2
        print(f"[Lucky 7] Starting → dice1={dice_roll_1}, dice2={dice_roll_2}, total={point_roll_total}")

        if lucky_seven_buff_counter > 0 and point_roll_total != come_out_roll_total and point_roll_total != 7:
            dice_roll_3 = random.randint(1, 6)
            print(f"[Lucky 7] Rerolled dice3={dice_roll_3}")

            original_dice = dice_roll_2
            dice_roll_2 = dice_roll_3
            point_roll_total = dice_roll_1 + dice_roll_2
            print(f"[Lucky 7] After reroll → dice1={dice_roll_1}, dice2={dice_roll_2}, total={point_roll_total}")

            if point_roll_total == 7:
                dice_roll_2 = original_dice
                point_roll_total = dice_roll_1 + dice_roll_2
                print(f"[Lucky 7] Reverted to original dice2={dice_roll_2}, total={point_roll_total}")

        return dice_roll_2, point_roll_total
