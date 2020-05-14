from random import shuffle
from copy import deepcopy


class HandEvaluator:
    def __init__(self, custom_deck=None, custom_card_ranks=None, custom_card_suit_colors=None):
        """
        Evaluates frequencies of different types of hands given a set of cards.

        :type custom_deck: Deck
        :type custom_card_ranks: set[str]
        :type custom_card_suit_colors: dict[str, str]
        """

        self.card_ranks = {
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
        }

        self.card_suit_colors = {
            "♠": "BLACK",
            "♣": "BLACK",
            "♡": "RED",
            "♢": "RED"
        }

        if custom_card_ranks:
            self.card_ranks = custom_card_ranks

        if custom_card_suit_colors:
            self.card_suit_colors = custom_card_suit_colors

        self.card_suits = set(self.card_suit_colors.keys())
        self.card_colors = set(self.card_suit_colors.values())

        self.deck = custom_deck if custom_deck else self._generate_starting_deck()

    def _generate_starting_deck(self):
        """
        Generates a starting deck with one card of each provided rank/suit.
        """

        return Deck(
            [Card(rank, suit, self.card_suit_colors[suit]) for rank in self.card_ranks for suit in self.card_suits]
        )


class Deck:
    def __init__(self, cards):
        """
        A deck of playing cards. By default, contains

        :type cards: list[Card]
        """

        self.cards = cards
        self._calculate_histograms()

    def _calculate_histograms(self):
        self.card_suits = {c.suit for c in self.cards}
        self.card_ranks = {c.rank for c in self.cards}
        self.card_colors = {c.color for c in self.cards}
        self.suits_histogram = {suit: len([c for c in self.cards if c.suit == suit]) for suit in self.card_suits}
        self.ranks_histogram = {rank: len([c for c in self.cards if c.rank == rank]) for rank in self.card_ranks}

    def add_cards(self, cards):
        for c in cards:
            self.cards.append(c)

        self._calculate_histograms()

    def double_cards(self):
        """
        Creates a duplicate of each card in the deck.
        """

        self.cards += deepcopy(self.cards)
        self._calculate_histograms()

    def remove_cards(self, lambda_statement=None, index=None):
        """
        Filters self.cards according to the provided lambda statement or index.  If both are specified, filters first.
        """

        if lambda_statement:
            self.cards = list(filter(lambda_statement, self.cards))

        if index:
            self.cards = self.cards[0:index]

        self._calculate_histograms()

    def has_flush(self, count=5, suit=None):
        """
        :param count: The amount of cards required to constitute a flush.
        :param suit: The suit that a flush is required to constitute (optional; default: None).
        """

        if suit:
            return self.suits_histogram[suit] > count

        return any(c >= count for c in self.suits_histogram.values())

    def has_four_of_a_kinds(self, four_of_a_kind_count=1):
        """
        :param four_of_a_kind_count: Some number of four-of-a-kinds.
        """

        rank_counts = list(filter(lambda s: s >= 4, self.ranks_histogram.values()))

        return len(rank_counts) >= four_of_a_kind_count

    def has_three_of_a_kinds(self, three_of_a_kind_count=1):
        """
        :param three_of_a_kind_count: Some number of three-of-a-kinds.
        """

        rank_counts = list(filter(lambda s: s >= 3, self.ranks_histogram.values()))

        return len(rank_counts) >= three_of_a_kind_count

    def has_pairs(self, pair_count=1):
        """
        :param pair_count: Some number of pairs.
        """

        rank_counts = list(filter(lambda s: s >= 2, self.ranks_histogram.values()))

        return len(rank_counts) >= pair_count

    def has_cards(self):
        return len(self.cards) > 0

    def shuffle(self):
        shuffle(self.cards)

    def print(self):
        for c in self.cards:
            print(c.rank + c.suit, end=" ")

        print("")


class Card:
    def __init__(self, rank, suit, color):
        """
        A playing card.

        :param rank: A card's rank.
        :type rank: str
        :param suit: A card's suit.
        :type suit: str
        :param color: A card's color.
        :type color: str
        """

        self.rank = rank
        self.suit = suit
        self.color = color
