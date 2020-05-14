import unittest
from models import HandEvaluator, Deck, Card


class HandEvaluations(unittest.TestCase):

    hand_evaluator = HandEvaluator()

    @unittest.skip
    def test_print_cards(self):
        self.hand_evaluator.deck.print()
        self.assertTrue(True)

    @unittest.skip
    def test_remove_cards(self):
        hand_evaluator = HandEvaluator(custom_card_suit_colors={"𓆏": "FROG", "𓃰": "ELEPHANT"})
        hand_evaluator.deck.double_cards()
        hand_evaluator.deck.remove_cards(lambda x: x.rank != "A")

        self.assertTrue(len(hand_evaluator.deck.cards) == 48)

    @unittest.skip
    def test_doesnt_have_pairs(self):
        hand_evaluator = HandEvaluator(
            custom_card_ranks={"2", "3", "4", "5"},
            custom_card_suit_colors={"𓆏": "FROG"}
        )

        self.assertTrue(hand_evaluator.deck.has_pairs(1) is False)

    @unittest.skip
    def test_has_pairs(self):
        hand_evaluator = HandEvaluator(
            custom_card_ranks={"2", "3", "4", "5"},
            custom_card_suit_colors={"𓆏": "FROG"}
        )

        hand_evaluator.deck.add_cards([Card(rank="3", suit="𓆏", color="GIRAFFE")])

        self.assertTrue(hand_evaluator.deck.has_pairs(1))

    @unittest.skip
    def test_has_flush(self):
        hand_evaluator = HandEvaluator(
            custom_deck=Deck(cards=[
                Card(rank="3", suit="𓆏", color="GREEN"),
                Card(rank="3", suit="𓆏", color="BLACK"),
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="4", suit="𓃰", color="GREEN"),
                Card(rank="K", suit="𓃰", color="GREEN"),
                Card(rank="Q", suit="𓆏", color="GREEN")
            ])
        )

        self.assertTrue(hand_evaluator.deck.has_flush(4))

    @unittest.skip
    def test_doesnt_have_flush(self):
        hand_evaluator = HandEvaluator(
            custom_deck=Deck(cards=[
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="4", suit="𓃰", color="BLACK"),
                Card(rank="K", suit="𓃰", color="BLACK"),
                Card(rank="Q", suit="𓃰", color="BLACK")
            ])
        )

        self.assertTrue(hand_evaluator.deck.has_flush(4) is False)

    @unittest.skip
    def test_has_three_pairs(self):
        hand_evaluator = HandEvaluator(
            custom_deck=Deck(cards=[
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="5", suit="𓃰", color="BLACK"),
                Card(rank="3", suit="𓆏", color="RED"),
                Card(rank="4", suit="𓆏", color="RED"),
                Card(rank="4", suit="𓃰", color="BLACK"),
                Card(rank="5", suit="𓃰", color="BLACK"),
                Card(rank="6", suit="𓃰", color="BLACK")
            ])
        )

        self.assertTrue(hand_evaluator.deck.has_n_pairs(3))

    def test_custom_test(self):

        foak_count = 0
        iterations = 100000

        for i in range(0, iterations):
            hand_evaluator = HandEvaluator(
                custom_card_suit_colors={"𓆏": "FROG", "𓃰": "ELEPHANT"}
            )

            hand_evaluator.deck.double_cards()
            hand_evaluator.deck.shuffle()
            hand_evaluator.deck.remove_cards(lambda_statement=lambda x: x.rank != "A", index=13)

            if hand_evaluator.deck.has_four_of_a_kinds(1):
                foak_count += 1

        print(
            "The probability of having a four-of-a-kind given this custom deck is around {} %.".format(
                foak_count / iterations * 100
            )
        )

    def test_custom_test2(self):

        straight_count = 0
        iterations = 100000

        for i in range(0, iterations):
            hand_evaluator = HandEvaluator(
                custom_card_suit_colors={"𓆏": "FROG", "𓃰": "ELEPHANT"}
            )

            hand_evaluator.deck.double_cards()
            hand_evaluator.deck.shuffle()
            hand_evaluator.deck.remove_cards(lambda_statement=lambda x: x.rank != "A", index=13)

            if hand_evaluator.deck.has_straight(4):
                straight_count += 1

        print(
            "The probability of having a four-card straight given this custom deck is around {} %.".format(
                straight_count / iterations * 100
            )
        )
