import unittest
from models import Deck, Card


class HandEvaluations(unittest.TestCase):

    @unittest.skip
    def test_print_cards(self):
        Deck().print()
        self.assertTrue(True)

    @unittest.skip
    def test_remove_cards(self):
        deck = Deck(custom_suits={"𓆏": "GREEN", "𓃰": "GREY"})
        deck.double_cards()
        deck.remove_cards(lambda x: x.rank != "A")

        self.assertTrue(len(deck.cards) == 48)

    @unittest.skip
    def test_doesnt_have_pairs(self):
        deck = Deck(
            custom_ranks={"2": 2, "3": 3, "4": 4, "5": 5},
            custom_suits={"𓆏": "GREEN"}
        )

        self.assertTrue(deck.evaluator.has_pairs(1) is False)

    @unittest.skip
    def test_has_pairs(self):
        deck = Deck(
            custom_ranks={"2": 2, "3": 3, "4": 4, "5": 5},
            custom_suits={"𓆏": "GREEN"}
        )

        deck.add_cards([Card(rank="3", rank_value=3, suit="𓆏", color="RED")])

        self.assertTrue(deck.evaluator.has_pairs(1))

    @unittest.skip
    def test_has_flush(self):
        deck = Deck(
            custom_cards=[
                Card(rank="3", rank_value=3, suit="𓆏", color="GREEN"),
                Card(rank="3", rank_value=3, suit="𓆏", color="BLACK"),
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="4", rank_value=4, suit="𓃰", color="GREEN"),
                Card(rank="K", rank_value=13, suit="𓃰", color="GREEN"),
                Card(rank="Q", rank_value=12, suit="𓆏", color="GREEN")
            ]
        )

        self.assertTrue(deck.evaluator.has_flush(4))

    @unittest.skip
    def test_doesnt_have_flush(self):
        deck = Deck(
            custom_cards=[
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="4", rank_value=4, suit="𓃰", color="BLACK"),
                Card(rank="K", rank_value=13, suit="𓃰", color="BLACK"),
                Card(rank="Q", rank_value=12, suit="𓃰", color="BLACK")
            ]
        )

        self.assertTrue(deck.evaluator.has_flush(4) is False)

    @unittest.skip
    def test_has_three_pairs(self):
        deck = Deck(
            custom_cards=[
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="5", rank_value=5, suit="𓃰", color="BLACK"),
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="4", rank_value=4, suit="𓆏", color="RED"),
                Card(rank="4", rank_value=4, suit="𓃰", color="BLACK"),
                Card(rank="5", rank_value=5, suit="𓃰", color="BLACK"),
                Card(rank="6", rank_value=6, suit="𓃰", color="BLACK")
            ]
        )

        self.assertTrue(deck.evaluator.has_n_pairs(3))

    @unittest.skip
    def test_has_6_card_straight(self):
        deck = Deck(
            custom_cards=[
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="5", rank_value=5, suit="𓃰", color="BLACK"),
                Card(rank="6", rank_value=6, suit="𓆏", color="RED"),
                Card(rank="7", rank_value=7, suit="𓆏", color="RED"),
                Card(rank="8", rank_value=8, suit="𓃰", color="BLACK"),
                Card(rank="9", rank_value=9, suit="𓃰", color="BLACK"),
                Card(rank="10", rank_value=10, suit="𓃰", color="BLACK")
            ]
        )

        self.assertTrue(deck.evaluator.has_straight(6))

    @unittest.skip
    def test_has_7_card_straight(self):
        deck = Deck(
            custom_cards=[
                Card(rank="3", rank_value=3, suit="𓆏", color="RED"),
                Card(rank="5", rank_value=5, suit="𓃰", color="BLACK"),
                Card(rank="6", rank_value=6, suit="𓆏", color="RED"),
                Card(rank="7", rank_value=7, suit="𓆏", color="RED"),
                Card(rank="7", rank_value=7, suit="𓃰", color="BLACK"),
                Card(rank="8", rank_value=8, suit="𓃰", color="BLACK"),
                Card(rank="9", rank_value=9, suit="𓃰", color="BLACK"),
                Card(rank="10", rank_value=10, suit="𓃰", color="BLACK"),
                Card(rank="J", rank_value=11, suit="𓆏", color="RED"),
            ]
        )

        self.assertTrue(deck.evaluator.has_straight(7))

    @staticmethod
    @unittest.skip
    def test_get_foak_probability():

        foak_count = 0
        iterations = 100000

        for i in range(0, iterations):
            deck = Deck(custom_suits={"𓆏": "GREEN", "𓃰": "GREY"})

            deck.double_cards()
            deck.shuffle()
            deck.remove_cards(lambda_statement=lambda x: x.rank != "A", index=13)

            if deck.evaluator.has_four_of_a_kind():
                foak_count += 1

        print(
            "The probability of having a four-of-a-kind given this custom deck is around {} %.".format(
                foak_count / iterations * 100
            )
        )

    @staticmethod
    @unittest.skip
    def test_get_straights_probability():

        for i in range(3, 9):
            straight_count = 0
            straight_length = i
            iterations = 50000

            for j in range(0, iterations):
                deck = Deck(custom_suits={"𓆏": "GREEN", "𓃰": "GREY"})

                deck.double_cards()
                deck.shuffle()
                deck.remove_cards(lambda_statement=lambda x: x.rank != "A", index=13)

                if deck.evaluator.has_straight(straight_length):
                    straight_count += 1

            print(
                "The probability of this deck containing a {}-card straight is around {} %.".format(
                    straight_length,
                    straight_count / iterations * 100
                )
            )

    @staticmethod
    def test_get_diminishing_straights_probabibilty():
        """
        Given a custom deck, calculate the probability of the deck having a 3-card straight.
        Then remove the lowest cards, one by one, and calculate the probabilities again, etc.
        """

        straight_length = 3
        max_iterations = 50000

        straight_count_frequencies = dict()

        for i in range(3, 13):
            straight_count_frequencies[i] = 0

        for i in range(max_iterations):

            deck = Deck(custom_suits={"𓆏": "GREEN", "𓃰": "GREY"})

            deck.double_cards()
            deck.shuffle()
            deck.remove_cards(lambda_statement=lambda x: x.rank != "A", index=13)

            hand = deck.get_sample_hand(12)

            while len(hand.cards) >= straight_length:
                if hand.evaluator.has_straight(straight_length):
                    straight_count_frequencies[len(hand.cards)] += 1

                hand.remove_lowest_ranked_card()

        for i in sorted(straight_count_frequencies.keys()):
            print(
                "The probability of a hand containing a {}-card straight given its {} highest cards is around {} %.".format(
                        straight_length,
                        i,
                        straight_count_frequencies[i] / max_iterations * 100
                    )
                )
