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

        def poker_score_tracker(self) -> None:

            player_values = sorted(card[2] for card in self.player_hand)
            player_suits = sorted(card[1] for card in self.player_hand)
            print("DEBUG player_values:", player_values)

            enemy_values = sorted(card[2] for card in self.enemy_hand)
            enemy_suits = sorted(card[1] for card in self.enemy_hand)
            print("DEBUG enemy_values:", enemy_values)
            print("DEBUG player suit:", player_suits)
            print("DEBUG enemy suits:", enemy_suits)

            player_hand_type = "no_hand"
            enemy_hand_type = "no_hand"

            # ---- FULL HOUSE CHECK FIRST ----
            player_ranks = [card[0] for card in self.player_hand]
            player_rank_counts = {rank: player_ranks.count(rank) for rank in set(player_ranks)}
            if 3 in player_rank_counts.values() and 2 in player_rank_counts.values():
                player_hand_type = "full_house"

            enemy_ranks = [card[0] for card in self.enemy_hand]
            enemy_rank_counts = {rank: enemy_ranks.count(rank) for rank in set(enemy_ranks)}
            if 3 in enemy_rank_counts.values() and 2 in enemy_rank_counts.values():
                enemy_hand_type = "full_house"

            # ---- FLUSH CHECK ----
            player_suits = [card[1] for card in self.player_hand]
            enemy_suits = [card[1] for card in self.enemy_hand]

            if player_hand_type == "no_hand" and any(player_suits.count(suit) >= 5 for suit in set(player_suits)):
                player_hand_type = "flush"
            if enemy_hand_type == "no_hand" and any(enemy_suits.count(suit) >= 5 for suit in set(enemy_suits)):
                enemy_hand_type = "flush"

            # ---- STRAIGHT CHECK ----
            consecutive_count = 1
            for i in range(len(player_values) - 1):
                if player_values[i + 1] == player_values[i] + 1:
                    consecutive_count += 1
                    if consecutive_count == 5:
                        if player_hand_type == "no_hand":
                            player_hand_type = "straight"
                        break
                else:
                    consecutive_count = 1

            consecutive_count = 1
            for i in range(len(enemy_values) - 1):
                if enemy_values[i + 1] == enemy_values[i] + 1:
                    consecutive_count += 1
                    if consecutive_count == 5:
                        if enemy_hand_type == "no_hand":
                            enemy_hand_type = "straight"
                        break
                else:
                    consecutive_count = 1

            # ---- FALLBACK: PAIRS AND TRIPS ----
            if player_hand_type == "no_hand":
                if 3 in player_rank_counts.values():
                    player_hand_type = "three_of_a_kind"
                elif list(player_rank_counts.values()).count(2) == 2:
                    player_hand_type = "two_pair"
                elif 2 in player_rank_counts.values():
                    player_hand_type = "one_pair"

            if enemy_hand_type == "no_hand":
                if 3 in enemy_rank_counts.values():
                    enemy_hand_type = "three_of_a_kind"
                elif list(enemy_rank_counts.values()).count(2) == 2:
                    enemy_hand_type = "two_pair"
                elif 2 in enemy_rank_counts.values():
                    enemy_hand_type = "one_pair"

            print(f"Player has: {player_hand_type.replace('_', ' ').title()}")
            print(f"Enemy has: {enemy_hand_type.replace('_', ' ').title()}")

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

