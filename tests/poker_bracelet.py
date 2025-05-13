from deck import Deck
from game_constants.equipment import Equipment


def run_test(name, setup_func, expect_fail=False):
    print(f"Running {name}...")
    try:
        setup_func()
        print(f"{name}: ✅ Passed")
    except AssertionError as e:
        if expect_fail:
            print(f"{name}: ✅ Expected failure - {e}")
        else:
            print(f"{name}: ❌ Failed - {e}")


# 1. Player has Poker Bracelet, deck filled with 2s only, should never draw
def test_no_twos_with_bracelet_all_twos():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Spades", 2)] * 20 + [("Ace", "Hearts", 14)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] != "2", f"Expected no '2', got {hand}"


# 2. Player does NOT have Poker Bracelet, 2s are allowed
def test_twos_allowed_without_bracelet():
    class DummyState:
        class DummyPlayer:
            equipped_items = []
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2)]
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] == "2", f"Expected '2', got {hand}"


# 3. Player has Poker Bracelet, mixed deck, 2s skipped
def test_bracelet_skips_twos_in_mixed_deck():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Clubs", 2), ("Ace", "Diamonds", 14), ("2", "Spades", 2)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] == "Ace", f"Expected 'Ace', got {hand}"


# 4. Bracelet works with multiple cards
def test_bracelet_skips_multiple_twos():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Clubs", 2), ("2", "Diamonds", 2), ("Jack", "Hearts", 11), ("Queen", "Spades", 12)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(2, DummyState())
    for card in hand:
        assert card[0] != "2", f"Expected no '2', got {card}"


# 5. No bracelet and mixed deck
def test_no_bracelet_mixed_deck_allows_twos():
    class DummyState:
        class DummyPlayer:
            equipped_items = []
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2), ("Ace", "Spades", 14)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(2, DummyState())
    assert any(card[0] == "2" for card in hand), "Expected a '2' in hand"


# 6. Bracelet, only 2s in deck, fallback card at end
def test_only_fallback_card_drawn():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2)] * 5 + [("King", "Diamonds", 13)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] == "King", f"Expected 'King', got {hand}"


# 7. Draw 0 cards still returns empty list
def test_draw_zero_cards():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2), ("Ace", "Clubs", 14)]
    hand = deck.poker_player_draw_hand(0, DummyState())
    assert hand == [], f"Expected empty hand, got {hand}"


# 8. Drawing more cards than available
def test_draw_more_than_available():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("3", "Spades", 3), ("4", "Spades", 4)]
    try:
        hand = deck.poker_player_draw_hand(5, DummyState())
        assert len(hand) <= 2, f"Expected short hand, got {hand}"
    except IndexError:
        print("Expected IndexError due to insufficient cards.")


# 9. Redraw loops for each 2
def test_multiple_redraw_loops():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2), ("2", "Spades", 2), ("5", "Diamonds", 5)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] == "5", f"Expected '5', got {hand}"


# 10. Check if the function uses state.player.equipped_items correctly
def test_equipped_items_check_logic():
    class DummyState:
        class DummyPlayer:
            equipped_items = [Equipment.POKER_BRACELET.value]
        player = DummyPlayer()

    deck = Deck(load_sprites=False)
    deck.poker_cards = [("2", "Hearts", 2), ("3", "Hearts", 3)]
    deck.poker_cards.reverse()
    hand = deck.poker_player_draw_hand(1, DummyState())
    assert hand[0][0] == "3", f"Expected '3', got {hand}"


# Run all
if __name__ == "__main__":
    run_test("Test 1", test_no_twos_with_bracelet_all_twos)
    run_test("Test 2", test_twos_allowed_without_bracelet)
    run_test("Test 3", test_bracelet_skips_twos_in_mixed_deck)
    run_test("Test 4", test_bracelet_skips_multiple_twos)
    run_test("Test 5", test_no_bracelet_mixed_deck_allows_twos)
    run_test("Test 6", test_only_fallback_card_drawn)
    run_test("Test 7", test_draw_zero_cards)
    run_test("Test 8", test_draw_more_than_available)
    run_test("Test 9", test_multiple_redraw_loops)
    run_test("Test 10", test_equipped_items_check_logic)
