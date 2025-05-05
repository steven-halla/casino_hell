def test_poker_score_tracker():
    class DummyDeck:
        rank_order_poker = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14
        }

    class DummyPokerDarnel:
        def __init__(self):
            self.deck = DummyDeck()
            self.player_hand: list[tuple[str, str, int]] = []
            self.enemy_hand: list[tuple[str, str, int]] = []

        def get_hand_score(self, hand_type: str) -> int:
            hand_scores = {
                "royal_straight_flush": 10,
                "straight_flush": 9,
                "four_of_a_kind": 8,
                "full_house": 7,
                "flush": 6,
                "straight": 5,
                "three_of_a_kind": 4,
                "two_pair": 3,
                "one_pair": 2,
                "no_hand": 1,
            }
            return hand_scores.get(hand_type, 1)

        def get_bonus_score_if_tied(self, hand_type: str, hand: list[tuple[str, str, int]]) -> int:
            bonus_rank_values = {
                "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                "7": 7, "8": 8, "9": 9, "10": 10,
                "Jack": 11, "Queen": 12, "King": 13, "Ace": 14,
            }

            bonus_score = 0
            rank_counts = {}
            for rank, _, _ in hand:
                rank_counts.setdefault(rank, 0)
                rank_counts[rank] += 1

            if hand_type == "one_pair":
                for rank, count in rank_counts.items():
                    if count == 2:
                        bonus_score += bonus_rank_values[rank]
            elif hand_type == "two_pair":
                for rank, count in rank_counts.items():
                    if count == 2:
                        bonus_score += bonus_rank_values[rank]
            elif hand_type == "three_of_a_kind":
                for rank, count in rank_counts.items():
                    if count == 3:
                        bonus_score += bonus_rank_values[rank]
            elif hand_type == "four_of_a_kind":
                for rank, count in rank_counts.items():
                    if count == 4:
                        bonus_score += bonus_rank_values[rank]
            elif hand_type in {"full_house", "flush", "straight", "straight_flush", "royal_straight_flush"}:
                for rank, _, _ in hand:
                    bonus_score += bonus_rank_values[rank]

            return bonus_score


        def poker_score_tracker(self) -> None:
            player_values = sorted(card[2] for card in self.player_hand)
            player_suits = sorted(card[1] for card in self.player_hand)
            enemy_values = sorted(card[2] for card in self.enemy_hand)
            enemy_suits = sorted(card[1] for card in self.enemy_hand)

            print("DEBUG player_values:", player_values)
            print("DEBUG enemy_values:", enemy_values)
            print("DEBUG player suit:", player_suits)
            print("DEBUG enemy suits:", enemy_suits)

            self.player_hand_type = ""
            self.enemy_hand_type = ""

            royal_values = {10, 11, 12, 13, 14}

            # ---- ROYAL FLUSH CHECK ----
            if not self.player_hand_type and set(card[2] for card in self.player_hand) == royal_values:
                suit = self.player_hand[0][1]
                if all(card[1] == suit for card in self.player_hand):
                    self.player_hand_type = "royal_straight_flush"
            if not self.enemy_hand_type and set(card[2] for card in self.enemy_hand) == royal_values:
                suit = self.enemy_hand[0][1]
                if all(card[1] == suit for card in self.enemy_hand):
                    self.enemy_hand_type = "royal_straight_flush"

            # ---- STRAIGHT FLUSH CHECK ----
            if not self.player_hand_type:
                player_suit_groups = {}
                for value, suit in ((card[2], card[1]) for card in self.player_hand):
                    player_suit_groups.setdefault(suit, []).append(value)
                for suit, values in player_suit_groups.items():
                    values = sorted(set(values))
                    consecutive = 1
                    for i in range(len(values) - 1):
                        if values[i + 1] == values[i] + 1:
                            consecutive += 1
                            if consecutive == 5:
                                self.player_hand_type = "straight_flush"
                                break
                        else:
                            consecutive = 1
                    if self.player_hand_type:
                        break

            if not self.enemy_hand_type:
                enemy_suit_groups = {}
                for value, suit in ((card[2], card[1]) for card in self.enemy_hand):
                    enemy_suit_groups.setdefault(suit, []).append(value)
                for suit, values in enemy_suit_groups.items():
                    values = sorted(set(values))
                    consecutive = 1
                    for i in range(len(values) - 1):
                        if values[i + 1] == values[i] + 1:
                            consecutive += 1
                            if consecutive == 5:
                                self.enemy_hand_type = "straight_flush"
                                break
                        else:
                            consecutive = 1
                    if self.enemy_hand_type:
                        break

            # ---- FOUR OF A KIND ----
            player_ranks = [card[0] for card in self.player_hand]
            player_rank_counts = {rank: player_ranks.count(rank) for rank in set(player_ranks)}
            if not self.player_hand_type and 4 in player_rank_counts.values():
                self.player_hand_type = "four_of_a_kind"

            enemy_ranks = [card[0] for card in self.enemy_hand]
            enemy_rank_counts = {rank: enemy_ranks.count(rank) for rank in set(enemy_ranks)}
            if not self.enemy_hand_type and 4 in enemy_rank_counts.values():
                self.enemy_hand_type = "four_of_a_kind"

            # ---- FULL HOUSE ----
            if not self.player_hand_type and 3 in player_rank_counts.values() and 2 in player_rank_counts.values():
                self.player_hand_type = "full_house"
            if not self.enemy_hand_type and 3 in enemy_rank_counts.values() and 2 in enemy_rank_counts.values():
                self.enemy_hand_type = "full_house"

            # ---- FLUSH ----
            if not self.player_hand_type and any(player_suits.count(suit) >= 5 for suit in set(player_suits)):
                self.player_hand_type = "flush"
            if not self.enemy_hand_type and any(enemy_suits.count(suit) >= 5 for suit in set(enemy_suits)):
                self.enemy_hand_type = "flush"

            # ---- STRAIGHT ----
            if not self.player_hand_type:
                consecutive = 1
                for i in range(len(player_values) - 1):
                    if player_values[i + 1] == player_values[i] + 1:
                        consecutive += 1
                        if consecutive == 5:
                            self.player_hand_type = "straight"
                            break
                    else:
                        consecutive = 1

            if not self.enemy_hand_type:
                consecutive = 1
                for i in range(len(enemy_values) - 1):
                    if enemy_values[i + 1] == enemy_values[i] + 1:
                        consecutive += 1
                        if consecutive == 5:
                            self.enemy_hand_type = "straight"
                            break
                    else:
                        consecutive = 1

            # ---- PAIR/TRIPS ----
            if not self.player_hand_type:
                if 3 in player_rank_counts.values():
                    self.player_hand_type = "three_of_a_kind"
                elif list(player_rank_counts.values()).count(2) == 2:
                    self.player_hand_type = "two_pair"
                elif 2 in player_rank_counts.values():
                    self.player_hand_type = "one_pair"

            if not self.enemy_hand_type:
                if 3 in enemy_rank_counts.values():
                    self.enemy_hand_type = "three_of_a_kind"
                elif list(enemy_rank_counts.values()).count(2) == 2:
                    self.enemy_hand_type = "two_pair"
                elif 2 in enemy_rank_counts.values():
                    self.enemy_hand_type = "one_pair"

            if not self.player_hand_type:
                self.player_hand_type = "no_hand"
            if not self.enemy_hand_type:
                self.enemy_hand_type = "no_hand"

            print(f"Player has: {self.player_hand_type.replace('_', ' ').title()}")
            print(f"Enemy has: {self.enemy_hand_type.replace('_', ' ').title()}")
            # player_score = self.get_hand_score(self.player_hand_type)
            # enemy_score = self.get_hand_score(self.enemy_hand_type)
            player_score = self.get_hand_score(self.player_hand_type)
            enemy_score = self.get_hand_score(self.enemy_hand_type)

            if self.player_hand_type == self.enemy_hand_type:
                player_score += self.get_bonus_score_if_tied(self.player_hand_type, self.player_hand)
                enemy_score += self.get_bonus_score_if_tied(self.enemy_hand_type, self.enemy_hand)
            print(f"Player score: {player_score}")
            print(f"Enemy score: {enemy_score}")



    # ---- TEST CASES ----
    print("=== Test 1.1: Player Wins with Higher Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("King", "Hearts", 10), ("King", "Spades", 10), ("3", "Clubs", 3), ("7", "Diamonds", 7), ("9", "Hearts", 9)]
    game.enemy_hand = [("Jack", "Hearts", 10), ("Jack", "Clubs", 10), ("5", "Spades", 5), ("6", "Diamonds", 6), ("8", "Clubs", 8)]
    game.poker_score_tracker()

    print("\n=== Test 1.2: Enemy Wins with Higher Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("8", "Spades", 8), ("2", "Diamonds", 2), ("4", "Clubs", 4), ("7", "Spades", 7)]
    game.enemy_hand = [("Queen", "Hearts", 10), ("Queen", "Diamonds", 10), ("3", "Clubs", 3), ("5", "Spades", 5), ("9", "Hearts", 9)]
    game.poker_score_tracker()

    print("\n=== Test 1.3: Draw with Same Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Hearts", 10), ("10", "Spades", 10), ("2", "Diamonds", 2), ("3", "Clubs", 3), ("4", "Spades", 4)]
    game.enemy_hand = [("10", "Diamonds", 10), ("10", "Clubs", 10), ("5", "Hearts", 5), ("6", "Spades", 6), ("7", "Hearts", 7)]
    game.poker_score_tracker()

    print("\n=== Test 1.4: Perfect Mirror Hand (Exact Same Cards) ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Hearts", 10), ("10", "Spades", 10), ("2", "Diamonds", 2), ("3", "Clubs", 3),
                        ("4", "Spades", 4)]
    game.enemy_hand = [("10", "Hearts", 10), ("10", "Spades", 10), ("2", "Diamonds", 2), ("3", "Clubs", 3),
                       ("4", "Spades", 4)]
    game.poker_score_tracker()

    print("\n=== Test 2.1: Player and Enemy Both Two Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("9", "Hearts", 9), ("9", "Clubs", 9), ("2", "Diamonds", 2), ("2", "Spades", 2), ("4", "Hearts", 4)]
    game.enemy_hand = [("8", "Spades", 8), ("8", "Diamonds", 8), ("3", "Clubs", 3), ("3", "Spades", 3), ("7", "Hearts", 7)]
    game.poker_score_tracker()

    print("\n=== Test 2.2: Player Two Pair vs Enemy One Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("8", "Clubs", 8), ("3", "Diamonds", 3), ("3", "Hearts", 3), ("5", "Spades", 5)]
    game.enemy_hand = [("Queen", "Hearts", 10), ("Queen", "Diamonds", 10), ("2", "Clubs", 2), ("4", "Spades", 4), ("6", "Diamonds", 6)]
    game.poker_score_tracker()

    print("\n=== Test 3.1: Player No Hand, Enemy Has Three of a Kind ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("4", "Spades", 4), ("6", "Clubs", 6), ("8", "Diamonds", 8), ("10", "Hearts", 10)]
    game.enemy_hand = [("Jack", "Spades", 10), ("Jack", "Diamonds", 10), ("Jack", "Hearts", 10), ("5", "Hearts", 5), ("7", "Clubs", 7)]
    game.poker_score_tracker()

    print("\n=== Test 4: No Pair for Either ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("4", "Spades", 4), ("6", "Clubs", 6), ("8", "Diamonds", 8), ("10", "Hearts", 10)]
    game.enemy_hand = [("3", "Clubs", 3), ("5", "Spades", 5), ("7", "Diamonds", 7), ("9", "Clubs", 9), ("Queen", "Hearts", 10)]
    game.poker_score_tracker()

    print("\n=== Test 5.1: Player has a Straight ===")
    game = DummyPokerDarnel()
    game.player_hand = [("3", "Hearts", 3), ("4", "Spades", 4), ("5", "Clubs", 5), ("6", "Diamonds", 6),
                        ("7", "Hearts", 7)]
    game.enemy_hand = [("King", "Spades", 13), ("King", "Hearts", 13), ("4", "Clubs", 4), ("8", "Diamonds", 8),
                       ("2", "Hearts", 2)]
    game.poker_score_tracker()

    print("\n=== Test 5.2: Enemy has a Straight ===")
    game = DummyPokerDarnel()
    game.player_hand = [("9", "Hearts", 9), ("9", "Clubs", 9), ("4", "Spades", 4), ("6", "Hearts", 6),
                        ("8", "Diamonds", 8)]
    game.enemy_hand = [("5", "Hearts", 5), ("6", "Spades", 6), ("7", "Clubs", 7), ("8", "Hearts", 8),
                       ("9", "Spades", 9)]
    game.poker_score_tracker()

    print("\n=== Test 5.3: Both Have Equal Straight (Draw) ===")
    game = DummyPokerDarnel()
    game.player_hand = [("4", "Clubs", 4), ("5", "Hearts", 5), ("6", "Diamonds", 6), ("7", "Spades", 7),
                        ("8", "Hearts", 8)]
    game.enemy_hand = [("4", "Spades", 4), ("5", "Diamonds", 5), ("6", "Clubs", 6), ("7", "Clubs", 7),
                       ("8", "Diamonds", 8)]
    game.poker_score_tracker()

    print("\n=== Test 5.4: Player Has Higher Straight ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("9", "Spades", 9), ("10", "Diamonds", 10), ("Jack", "Hearts", 11),
                        ("Queen", "Spades", 12)]
    game.enemy_hand = [("4", "Clubs", 4), ("5", "Hearts", 5), ("6", "Spades", 6), ("7", "Diamonds", 7),
                       ("8", "Clubs", 8)]
    game.poker_score_tracker()

    print("\n=== Test 5.5: Enemy Has Higher Straight ===")
    game = DummyPokerDarnel()
    game.player_hand = [("5", "Clubs", 5), ("6", "Hearts", 6), ("7", "Diamonds", 7), ("8", "Spades", 8),
                        ("9", "Clubs", 9)]
    game.enemy_hand = [("9", "Hearts", 9), ("10", "Clubs", 10), ("Jack", "Spades", 11), ("Queen", "Hearts", 12),
                       ("King", "Diamonds", 13)]
    game.poker_score_tracker()

    print("\n=== Test 6.1: Player has a Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("5", "Hearts", 5), ("7", "Hearts", 7), ("9", "Hearts", 9),
                        ("King", "Hearts", 13)]
    game.enemy_hand = [("3", "Clubs", 3), ("4", "Spades", 4), ("6", "Diamonds", 6), ("8", "Clubs", 8),
                       ("Jack", "Spades", 11)]
    game.poker_score_tracker()

    print("\n=== Test 6.2: Enemy has a Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("3", "Clubs", 3), ("5", "Diamonds", 5), ("7", "Spades", 7),
                        ("9", "Hearts", 9)]
    game.enemy_hand = [("3", "Clubs", 3), ("5", "Clubs", 5), ("7", "Clubs", 7), ("9", "Clubs", 9),
                       ("King", "Clubs", 13)]
    game.poker_score_tracker()

    print("\n=== Test 6.3: Both Have a Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Spades", 2), ("4", "Spades", 4), ("6", "Spades", 6), ("8", "Spades", 8),
                        ("10", "Spades", 10)]
    game.enemy_hand = [("3", "Clubs", 3), ("5", "Clubs", 5), ("7", "Clubs", 7), ("9", "Clubs", 9),
                       ("Queen", "Clubs", 12)]
    game.poker_score_tracker()

    print("\n=== Test 6.4: Player Flush vs Enemy Straight ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Diamonds", 2), ("4", "Diamonds", 4), ("6", "Diamonds", 6), ("8", "Diamonds", 8),
                        ("10", "Diamonds", 10)]
    game.enemy_hand = [("5", "Hearts", 5), ("6", "Spades", 6), ("7", "Clubs", 7), ("8", "Hearts", 8),
                       ("9", "Spades", 9)]
    game.poker_score_tracker()

    print("\n=== Test 6.5: Enemy Flush vs Player Three of a Kind ===")
    game = DummyPokerDarnel()
    game.player_hand = [("King", "Spades", 13), ("King", "Hearts", 13), ("King", "Diamonds", 13), ("7", "Clubs", 7),
                        ("3", "Hearts", 3)]
    game.enemy_hand = [("3", "Spades", 3), ("5", "Spades", 5), ("7", "Spades", 7), ("9", "Spades", 9),
                       ("Jack", "Spades", 11)]
    game.poker_score_tracker()

    print("\n=== Test 6.6: No Flush for Either ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("3", "Clubs", 3), ("4", "Diamonds", 4), ("5", "Spades", 5),
                        ("6", "Hearts", 6)]
    game.enemy_hand = [("7", "Clubs", 7), ("8", "Diamonds", 8), ("9", "Spades", 9), ("10", "Hearts", 10),
                       ("Jack", "Clubs", 11)]
    game.poker_score_tracker()

    print("\n=== Test 7.1: Player has Full House ===")
    game = DummyPokerDarnel()
    game.player_hand = [("King", "Hearts", 13), ("King", "Spades", 13), ("King", "Clubs", 13),
                        ("9", "Diamonds", 9), ("9", "Hearts", 9)]
    game.enemy_hand = [("3", "Hearts", 3), ("4", "Spades", 4), ("6", "Clubs", 6),
                       ("7", "Diamonds", 7), ("10", "Hearts", 10)]
    game.poker_score_tracker()

    print("\n=== Test 7.2: Enemy has Full House ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("4", "Spades", 4), ("6", "Clubs", 6),
                        ("8", "Diamonds", 8), ("10", "Hearts", 10)]
    game.enemy_hand = [("Queen", "Clubs", 12), ("Queen", "Diamonds", 12), ("Queen", "Spades", 12),
                       ("5", "Hearts", 5), ("5", "Spades", 5)]
    game.poker_score_tracker()

    print("\n=== Test 7.3: Both have Full House ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Hearts", 10), ("10", "Clubs", 10), ("10", "Diamonds", 10),
                        ("9", "Spades", 9), ("9", "Hearts", 9)]
    game.enemy_hand = [("Jack", "Hearts", 11), ("Jack", "Diamonds", 11), ("Jack", "Clubs", 11),
                       ("8", "Spades", 8), ("8", "Hearts", 8)]
    game.poker_score_tracker()

    print("\n=== Test 7.4: Player Full House, Enemy Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("8", "Spades", 8), ("8", "Clubs", 8),
                        ("2", "Diamonds", 2), ("2", "Clubs", 2)]
    game.enemy_hand = [("3", "Spades", 3), ("5", "Spades", 5), ("7", "Spades", 7),
                       ("9", "Spades", 9), ("King", "Spades", 13)]
    game.poker_score_tracker()

    print("\n=== Test 7.5: No Full House for Either ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("3", "Diamonds", 3), ("4", "Clubs", 4),
                        ("5", "Hearts", 5), ("6", "Spades", 6)]
    game.enemy_hand = [("7", "Clubs", 7), ("8", "Hearts", 8), ("9", "Diamonds", 9),
                       ("10", "Spades", 10), ("Jack", "Clubs", 11)]
    game.poker_score_tracker()

    print("\n=== Test 8.1: Player has Four of a Kind ===")
    game = DummyPokerDarnel()
    game.player_hand = [("9", "Hearts", 9), ("9", "Diamonds", 9), ("9", "Spades", 9), ("9", "Clubs", 9),
                        ("3", "Hearts", 3)]
    game.enemy_hand = [("4", "Spades", 4), ("5", "Hearts", 5), ("7", "Clubs", 7), ("10", "Diamonds", 10),
                       ("King", "Hearts", 13)]
    game.poker_score_tracker()

    print("\n=== Test 8.2: Enemy has Four of a Kind ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Clubs", 2), ("4", "Diamonds", 4), ("6", "Spades", 6), ("8", "Hearts", 8),
                        ("10", "Clubs", 10)]
    game.enemy_hand = [("Queen", "Clubs", 12), ("Queen", "Diamonds", 12), ("Queen", "Hearts", 12),
                       ("Queen", "Spades", 12), ("2", "Hearts", 2)]
    game.poker_score_tracker()

    print("\n=== Test 8.3: Both have Four of a Kind ===")
    game = DummyPokerDarnel()
    game.player_hand = [("6", "Hearts", 6), ("6", "Spades", 6), ("6", "Diamonds", 6), ("6", "Clubs", 6),
                        ("3", "Diamonds", 3)]
    game.enemy_hand = [("8", "Clubs", 8), ("8", "Hearts", 8), ("8", "Spades", 8), ("8", "Diamonds", 8),
                       ("4", "Hearts", 4)]
    game.poker_score_tracker()

    print("\n=== Test 8.4: Four of a Kind beats Full House ===")
    game = DummyPokerDarnel()
    game.player_hand = [("Jack", "Hearts", 11), ("Jack", "Spades", 11), ("Jack", "Diamonds", 11), ("Jack", "Clubs", 11),
                        ("2", "Hearts", 2)]
    game.enemy_hand = [("10", "Hearts", 10), ("10", "Spades", 10), ("3", "Clubs", 3), ("3", "Diamonds", 3),
                       ("3", "Spades", 3)]
    game.poker_score_tracker()

    print("\n=== Test 8.5: No Four of a Kind for Either ===")
    game = DummyPokerDarnel()
    game.player_hand = [("3", "Hearts", 3), ("3", "Spades", 3), ("3", "Diamonds", 3), ("7", "Clubs", 7),
                        ("9", "Hearts", 9)]
    game.enemy_hand = [("8", "Hearts", 8), ("8", "Spades", 8), ("8", "Clubs", 8), ("5", "Diamonds", 5),
                       ("King", "Hearts", 13)]
    game.poker_score_tracker()

    print("\n=== Test 9.1: Player has Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("5", "Hearts", 5), ("6", "Hearts", 6), ("7", "Hearts", 7), ("8", "Hearts", 8),
                        ("9", "Hearts", 9)]
    game.enemy_hand = [("2", "Clubs", 2), ("4", "Diamonds", 4), ("6", "Spades", 6), ("9", "Hearts", 9),
                       ("King", "Spades", 13)]
    game.poker_score_tracker()

    print("\n=== Test 9.2: Enemy has Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Clubs", 2), ("4", "Diamonds", 4), ("6", "Spades", 6), ("8", "Hearts", 8),
                        ("10", "Spades", 10)]
    game.enemy_hand = [("3", "Clubs", 3), ("4", "Clubs", 4), ("5", "Clubs", 5), ("6", "Clubs", 6), ("7", "Clubs", 7)]
    game.poker_score_tracker()

    print("\n=== Test 9.3: Both Have Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("5", "Spades", 5), ("6", "Spades", 6), ("7", "Spades", 7), ("8", "Spades", 8),
                        ("9", "Spades", 9)]
    game.enemy_hand = [("4", "Clubs", 4), ("5", "Clubs", 5), ("6", "Clubs", 6), ("7", "Clubs", 7), ("8", "Clubs", 8)]
    game.poker_score_tracker()

    print("\n=== Test 9.4: Straight but Not Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("5", "Spades", 5), ("6", "Hearts", 6), ("7", "Spades", 7), ("8", "Diamonds", 8),
                        ("9", "Clubs", 9)]
    game.enemy_hand = [("2", "Hearts", 2), ("5", "Hearts", 5), ("8", "Hearts", 8), ("10", "Hearts", 10),
                       ("King", "Hearts", 13)]
    game.poker_score_tracker()

    print("\n=== Test 10.1: Player has Royal Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Spades", 10), ("Jack", "Spades", 11), ("Queen", "Spades", 12), ("King", "Spades", 13),
                        ("Ace", "Spades", 14)]
    game.enemy_hand = [("3", "Clubs", 3), ("5", "Hearts", 5), ("7", "Spades", 7), ("9", "Diamonds", 9),
                       ("Jack", "Hearts", 11)]
    game.poker_score_tracker()

    print("\n=== Test 10.2: Enemy has Royal Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Clubs", 2), ("4", "Diamonds", 4), ("6", "Spades", 6), ("8", "Hearts", 8),
                        ("10", "Clubs", 10)]
    game.enemy_hand = [("10", "Hearts", 10), ("Jack", "Hearts", 11), ("Queen", "Hearts", 12), ("King", "Hearts", 13),
                       ("Ace", "Hearts", 14)]
    game.poker_score_tracker()

    print("\n=== Test 10.3: Both Have Royal Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Diamonds", 10), ("Jack", "Diamonds", 11), ("Queen", "Diamonds", 12),
                        ("King", "Diamonds", 13), ("Ace", "Diamonds", 14)]
    game.enemy_hand = [("10", "Hearts", 10), ("Jack", "Hearts", 11), ("Queen", "Hearts", 12), ("King", "Hearts", 13),
                       ("Ace", "Hearts", 14)]
    game.poker_score_tracker()

    print("\n=== Test 10.4: Royal Flush beats Straight Flush ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Clubs", 10), ("Jack", "Clubs", 11), ("Queen", "Clubs", 12), ("King", "Clubs", 13),
                        ("Ace", "Clubs", 14)]
    game.enemy_hand = [("5", "Spades", 5), ("6", "Spades", 6), ("7", "Spades", 7), ("8", "Spades", 8),
                       ("9", "Spades", 9)]
    game.poker_score_tracker()




