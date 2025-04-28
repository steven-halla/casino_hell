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
            player_ranks = [player_card[0] for player_card in self.player_hand]
            player_rank_counts = {player_rank: player_ranks.count(player_rank) for player_rank in set(player_ranks)}
            enemy_ranks = [enemy_card[0] for enemy_card in self.enemy_hand]
            enemy_rank_counts = {enemy_rank: enemy_ranks.count(enemy_rank) for enemy_rank in set(enemy_ranks)}

            def determine_pair_type(rank_counts):
                if list(rank_counts.values()).count(2) == 2:
                    return "two_pair"
                elif 2 in rank_counts.values():
                    return "one_pair"
                else:
                    return "no_pair"

            player_hand_type = determine_pair_type(player_rank_counts)
            enemy_hand_type = determine_pair_type(enemy_rank_counts)

            print(f"Player has: {player_hand_type.replace('_', ' ').title()}")
            print(f"Enemy has: {enemy_hand_type.replace('_', ' ').title()}")

            if player_hand_type == "two_pair" and enemy_hand_type != "two_pair":
                print("Player wins with Two Pair!")
            elif enemy_hand_type == "two_pair" and player_hand_type != "two_pair":
                print("Enemy wins with Two Pair!")
            elif player_hand_type == "one_pair" and enemy_hand_type == "one_pair":
                player_pair_rank = None
                enemy_pair_rank = None
                for rank, count in player_rank_counts.items():
                    if count == 2:
                        player_pair_rank = rank
                        break
                for rank, count in enemy_rank_counts.items():
                    if count == 2:
                        enemy_pair_rank = rank
                        break

                if self.deck.rank_order_poker[player_pair_rank] > self.deck.rank_order_poker[enemy_pair_rank]:
                    print("Player wins with higher pair!")
                elif self.deck.rank_order_poker[player_pair_rank] < self.deck.rank_order_poker[enemy_pair_rank]:
                    print("Enemy wins with higher pair!")
                else:
                    print("Both players have the same pair! It's a draw!")
            elif player_hand_type == "two_pair" and enemy_hand_type == "two_pair":
                print("Both players have Two Pair! (Future: compare highest pairs)")
            else:
                print("No winning hand detected.")

    # ---- TEST CASES ----
    print("=== Test 1: Player Wins with Higher Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("King", "Hearts", 10), ("King", "Spades", 10), ("3", "Clubs", 3), ("7", "Diamonds", 7), ("9", "Hearts", 9)]
    game.enemy_hand = [("Jack", "Hearts", 10), ("Jack", "Clubs", 10), ("5", "Spades", 5), ("6", "Diamonds", 6), ("8", "Clubs", 8)]
    game.poker_score_tracker()

    print("\n=== Test 2: Enemy Wins with Higher Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("8", "Spades", 8), ("2", "Diamonds", 2), ("4", "Clubs", 4), ("7", "Spades", 7)]
    game.enemy_hand = [("Queen", "Hearts", 10), ("Queen", "Diamonds", 10), ("3", "Clubs", 3), ("5", "Spades", 5), ("9", "Hearts", 9)]
    game.poker_score_tracker()

    print("\n=== Test 3: Draw with Same Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("10", "Hearts", 10), ("10", "Spades", 10), ("2", "Diamonds", 2), ("3", "Clubs", 3), ("4", "Spades", 4)]
    game.enemy_hand = [("10", "Diamonds", 10), ("10", "Clubs", 10), ("5", "Hearts", 5), ("6", "Spades", 6), ("7", "Hearts", 7)]
    game.poker_score_tracker()

    print("\n=== Test 4: Player and Enemy Both Two Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("9", "Hearts", 9), ("9", "Clubs", 9), ("2", "Diamonds", 2), ("2", "Spades", 2), ("4", "Hearts", 4)]
    game.enemy_hand = [("8", "Spades", 8), ("8", "Diamonds", 8), ("3", "Clubs", 3), ("3", "Spades", 3), ("7", "Hearts", 7)]
    game.poker_score_tracker()

    print("\n=== Test 5: Player Two Pair vs Enemy One Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("8", "Hearts", 8), ("8", "Clubs", 8), ("3", "Diamonds", 3), ("3", "Hearts", 3), ("5", "Spades", 5)]
    game.enemy_hand = [("Queen", "Hearts", 10), ("Queen", "Diamonds", 10), ("2", "Clubs", 2), ("4", "Spades", 4), ("6", "Diamonds", 6)]
    game.poker_score_tracker()

    print("\n=== Test 6: No Pair for Player, Enemy Has One Pair ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("4", "Spades", 4), ("6", "Clubs", 6), ("8", "Diamonds", 8), ("10", "Hearts", 10)]
    game.enemy_hand = [("Jack", "Spades", 10), ("Jack", "Diamonds", 10), ("3", "Clubs", 3), ("5", "Hearts", 5), ("7", "Clubs", 7)]
    game.poker_score_tracker()

    print("\n=== Test 7: No Pair for Either ===")
    game = DummyPokerDarnel()
    game.player_hand = [("2", "Hearts", 2), ("4", "Spades", 4), ("6", "Clubs", 6), ("8", "Diamonds", 8), ("10", "Hearts", 10)]
    game.enemy_hand = [("3", "Clubs", 3), ("5", "Spades", 5), ("7", "Diamonds", 7), ("9", "Clubs", 9), ("Queen", "Hearts", 10)]
    game.poker_score_tracker()