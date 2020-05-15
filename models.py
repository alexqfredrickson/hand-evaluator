from random import shuffle
from copy import deepcopy


class Hand:
    def __init__(self, custom_cards=None, custom_suits=None, custom_ranks=None):
        """
        A hand of playing cards. By default, generates a normal 52 card deck. \
        If custom_cards is specified, these cards are used instead. \
        If both custom_suits and custom_ranks are specified, generates a deck with these ranks/suits. \
        If only one is specified, uses default ranks/suits (respective to what was unspecified)

        :type custom_cards: list[Card]
        :type custom_suits: dict[str, str]
        :type custom_ranks: dict[str, int]
        """

        default_card_ranks = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }

        default_card_suits = {
            "♠": "BLACK",
            "♣": "BLACK",
            "♡": "RED",
            "♢": "RED"
        }

        if custom_cards:
            self.cards = custom_cards

        elif custom_suits or custom_ranks:
            self.cards = [
                Card(
                    rank=rank,
                    rank_value=(custom_ranks if custom_ranks else default_card_ranks)[rank],
                    suit=suit,
                    color=(custom_suits if custom_suits else default_card_suits)[suit],
                )
                for rank in (custom_ranks if custom_ranks else default_card_ranks)
                for suit in (custom_suits if custom_suits else default_card_suits)
            ]

        else:
            self.cards = [
                Card(
                    rank=rank,
                    rank_value=default_card_ranks[rank],
                    suit=suit,
                    color=default_card_suits[suit],
                ) for rank in default_card_ranks for suit in default_card_suits
            ]

        self.evaluator = HandEvaluatorMixin(self.cards)

    def add_cards(self, cards):
        for c in cards:
            self.cards.append(c)

        # reinitialize hand evaluator
        self.evaluator = HandEvaluatorMixin(self.cards)

    def double_cards(self):
        """
        Creates a duplicate of each card in the deck.
        """

        self.cards += deepcopy(self.cards)

        # reinitialize hand evaluator
        self.evaluator = HandEvaluatorMixin(self.cards)

    def remove_cards(self, lambda_statement=None, index=None):
        """
        Filters self.cards according to the provided lambda statement or index.  If both are specified, filters first.
        """

        if lambda_statement:
            self.cards = list(filter(lambda_statement, self.cards))

        if index:
            self.cards = self.cards[0:index]

        # reinitialize hand evaluator
        self.evaluator = HandEvaluatorMixin(self.cards)

    def remove_lowest_ranked_card(self):
        if len(self.cards) != 0:
            self.cards.remove(min(self.cards, key=lambda x: x.rank))

            # reinitialize hand evaluator
            self.evaluator = HandEvaluatorMixin(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def print(self):
        for c in self.cards:
            print(c.rank + c.suit, end=" ")

        print("")


class Deck(Hand):
    """
    Kind of like a hand, if you think about it.
    """

    def __init__(self, custom_cards=None, custom_suits=None, custom_ranks=None):
        super().__init__(custom_cards, custom_suits, custom_ranks)

    def get_sample_hand(self, count):
        return Hand(custom_cards=self.cards[0:count])


class HandEvaluatorMixin:
    def __init__(self, cards):
        self.cards = cards

        self.all_card_suits = self._enumerate_card_suits()
        self.all_card_ranks = self._enumerate_card_ranks()
        self.all_card_colors = self._enumerate_card_colors()
        self.all_card_rank_values = self._enumerate_card_rank_values()

        self.suits_histogram = self._enumerate_suits_histogram()
        self.rank_values_histogram = self._enumerate_rank_values_histogram()

    def _enumerate_card_suits(self):
        return {c.suit for c in self.cards}

    def _enumerate_card_ranks(self):
        return {c.rank for c in self.cards}

    def _enumerate_card_colors(self):
        return {c.color for c in self.cards}

    def _enumerate_card_rank_values(self):
        return {c.rank_value for c in self.cards}

    def _enumerate_suits_histogram(self):
        return {suit: len([c for c in self.cards if c.suit == suit]) for suit in self.all_card_suits}

    def _enumerate_rank_values_histogram(self):
        return {
            rank_value:
                len([c for c in self.cards if c.rank_value == rank_value]) for rank_value in self.all_card_rank_values
        }

    def has_flush(self, cards_count=5, suit=None):
        """
        :param cards_count: The amount of cards required to constitute a flush.
        :param suit: The suit that a flush is required to constitute (optional; default: None).
        """

        if suit:
            return self.suits_histogram[suit] > cards_count

        return any(c >= cards_count for c in self.suits_histogram.values())

    def has_straight(self, cards_count=5):

        sorted_rank_values = sorted(self.rank_values_histogram.keys())

        for i in range(0, len(sorted_rank_values) - cards_count + 1):
            if all(
                    sorted_rank_values[i + increment] ==
                    sorted_rank_values[i + increment + 1] - 1
                    for increment in range(0, cards_count - 1)
            ):
                return True

        return False

    def has_straight_flush(self):
        pass

    def has_four_of_a_kind(self):
        return self.has_m_many_n_of_a_kind(1, 4)

    def has_three_of_a_kind(self):
        return self.has_m_many_n_of_a_kind(1, 3)

    def has_pair(self):
        return self.has_m_many_n_of_a_kind(1, 2)

    def has_two_pairs(self):
        return self.has_m_many_n_of_a_kind(2, 2)

    def has_m_many_n_of_a_kind(self, matching_sets_count, cards_count):
        """
        Returns whether or not the hand contains m-or-more n-of-a-kinds, where n is the number of cards necessary to
        comprise a set (i.e. the 'pair' in two-pair) - and m is the total amount of matching sets (e.g. the
        'two' in two-pair).
        """

        rank_counts = list(filter(lambda s: s >= cards_count, self.rank_values_histogram.values()))

        return len(rank_counts) >= matching_sets_count

    def has_cards(self):
        return len(self.cards) > 0


class Card:
    def __init__(self, rank, rank_value, suit, color):
        """
        A playing card.

        :param rank: A card's rank (e.g. "Ace").
        :type rank: str
        :param rank_value: A rank's value (e.g. 14).
        :type rank_value: int
        :param suit: A card's suit.
        :type suit: str
        :param color: A card's color.
        :type color: str
        """

        self.rank = rank
        self.rank_value = rank_value
        self.suit = suit
        self.color = color
