import random
from typing import List, Tuple

import pygame

from entity.entity import Entity


class Deck:
    def __init__(self):
        self.ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        self.suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
        self.rank_strings = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                             8: "8",
                             9: "9", 10: "10", "Jack": "Jack", "Queen": "Queen",
                             "King": "King", "Ace": "Ace"}
        self.suit_strings = {"Spades": "Spades", "Diamonds": "Diamonds",
                             "Clubs": "Clubs", "Hearts": "Hearts"}
        self.rank_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
                            10: 10, "Jack": 10, "Queen": 10,
                            "King": 10, "Ace": 11}
        self.rank_values_high_low = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
                            10: 10, "Jack": 11, "Queen": 12,
                            "King": 13, "Ace": 20}
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit],
                       self.rank_values[rank]) for suit in self.suits
                      for rank in self.ranks]
        self.isBlackJack = False
        self.black_jack_counter = 0
        self.sprite_size = (67, 95)
        self.card_width = 68
        self.card_height = 98

        self.sprite_sheet = pygame.image.load("./assets/images/playingcards.png")

        self.suit_index = {
            "Clubs": 0,
            "Diamonds": 1,
            "Hearts": 2,
            "Spades": 3
        }
        self.value_index = {
            "2": 0,
            "3": 1,
            "4": 2,
            "5": 3,
            "6": 4,
            "7": 5,
            "8": 6,
            "9": 7,
            "10": 8,
            "Jack": 9,
            "Queen": 10,
            "King": 11,
            "Ace": 12
        }

        self.card_value = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "jack": 10,
            "queen": 10,
            "king": 10,
            "ace": 11
        }



        for suit in self.suits:
            if "Ace" in self.ranks:
                self.cards.append(("Ace", suit, 1))
                self.cards.append(("Ace", suit, 11))

        # self.cards.append(('Joker', 'red', 0))
        # self.cards.append(('Joker', 'black', 0))

    def compute_hand_value_high_low(self, hand: List[Tuple[str, str, int]]) -> int:
        total_value = 0
        for card in hand:
            rank = card[0]
            value = self.rank_values_high_low.get(rank, 0)
            total_value += value
        return total_value

    def compute_hand_value(self, hand: List[Tuple[str, str, int]]) -> int:
        # Initialize the point value of the hand to 0
        hand_value = 0
        # Initialize a counter to track the number of aces in the hand
        num_aces = 0
        # Iterate through the cards in the hand
        for card in hand:
            if card[0] == "Ace":
                num_aces += 1
                hand_value += 11
            else:
                hand_value += card[2]

        while num_aces > 0 and hand_value > 21:
            hand_value -= 10
            num_aces -= 1

        return hand_value

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def draw_card_face_down(self, position: tuple[int, int], display: pygame.Surface):
        top_card_position = (self.card_width * 13, 0)
        sprite = self.sprite_sheet.subsurface(pygame.Rect(top_card_position, (self.card_width, self.card_height)))
        sprite.set_colorkey((0, 190, 0))
        display.blit(sprite, position)

    def draw_card_face_up(self, suit: str, value: str, position: Tuple[int, int], display: pygame.Surface):
        x_offset = self.value_index[value]
        y_offset = self.suit_index[suit]
        card_position = (x_offset * self.card_width, y_offset * self.card_height)
        sprite = self.sprite_sheet.subsurface(pygame.Rect(card_position, (self.card_width, self.card_height)))
        sprite.set_colorkey((0, 190, 0))

        # Ensure 'display' is a valid pygame.Surface object
        display.blit(sprite, position)

    def get_next_card(self):
        card = self.cards.pop()
        # print("draw card: " + str(card))
        return card

    def shuffle(self):

        self.cards.clear()
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit],
                       self.rank_values[rank]) for suit in self.suits
                      for rank in self.ranks]

        random.shuffle(self.cards)
        return self.cards

    def player_draw_hand(self, num_cards):

        hand = []
        for i in range(num_cards):
            hand.append(self.get_next_card())
        return hand

    def enemy_draw_hand(self, num_cards):
        hand = []
        for i in range(num_cards):
            hand.append(self.get_next_card())
        return hand

    def add_rank(self, rank):
        self.ranks.append(rank)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for
                      suit in self.suits for rank in self.ranks]

    def add_suit(self, suit):
        self.suits.append(suit)
        self.cards = [(self.rank_strings[rank], self.suit_strings[suit]) for
                      suit in self.suits
                      for rank in self.ranks]

    def insert_cards_manually(self, cards_to_insert: List[Tuple[str, str, int]]) -> List[Tuple[str, str, int]]:
        """Inserts a list of cards (rank, suit, value) into the deck, reshuffles, and returns the inserted cards."""
        inserted_cards = []
        for card in cards_to_insert:
            rank, suit, value = card
            if rank in self.rank_strings and suit in self.suit_strings:
                self.cards.append((self.rank_strings[rank], self.suit_strings[suit], value))
                inserted_cards.append((self.rank_strings[rank], self.suit_strings[suit], value))
                print(f"Added {rank} of {suit} with value {value} to the deck.")
            else:
                print(f"Invalid card: {rank} of {suit}. Skipping...")

        # Reshuffle the deck
        random.shuffle(self.cards)

        # Return the inserted cards for use in the hand
        return inserted_cards

        #the below is how to make the fun call with the insert cards mannually method
        # cards_to_insert = [("Ace", "Spades", 11), ("King", "Hearts", 10)]
        #         cards_to_insert2 = [("Ace", "Diamonds", 11), ("King", "Spades", 10)]
        #         self.enemy_hand = self.deck.insert_cards_manually(cards_to_insert)
        #         self.player_hand = self.deck.insert_cards_manually(cards_to_insert2)
        #         self.enemy_score = self.deck.compute_hand_value(self.enemy_hand)
        #         # self.player_hand = self.deck.player_draw_hand(2)
        #         self.player_score = self.deck.compute_hand_value(self.player_hand)
