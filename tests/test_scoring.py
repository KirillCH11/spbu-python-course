import pytest
from project.Yatzy.scoring import calculate_score, Category


class TestScoring:
    def test_upper_section(self):
        dice = [1, 1, 2, 3, 4]
        assert calculate_score(dice, Category.ONES) == 2
        assert calculate_score(dice, Category.TWOS) == 2
        assert calculate_score(dice, Category.THREES) == 3
        assert calculate_score(dice, Category.FOURS) == 4

    def test_pair(self):
        assert calculate_score([1, 1, 2, 3, 4], Category.PAIR) == 2
        assert calculate_score([1, 1, 2, 2, 3], Category.PAIR) == 4  # Highest pair
        assert calculate_score([1, 2, 3, 4, 5], Category.PAIR) == 0

    def test_two_pairs(self):
        assert calculate_score([1, 1, 2, 2, 3], Category.TWO_PAIRS) == 6
        assert calculate_score([1, 1, 2, 3, 4], Category.TWO_PAIRS) == 0

    def test_three_kind(self):
        assert calculate_score([1, 1, 1, 2, 3], Category.THREE_KIND) == 3
        assert calculate_score([1, 2, 3, 4, 5], Category.THREE_KIND) == 0

    def test_four_kind(self):
        assert calculate_score([1, 1, 1, 1, 2], Category.FOUR_KIND) == 4
        assert calculate_score([1, 1, 1, 2, 3], Category.FOUR_KIND) == 0

    def test_straights(self):
        assert calculate_score([1, 2, 3, 4, 5], Category.SMALL_STRAIGHT) == 15
        assert calculate_score([2, 3, 4, 5, 6], Category.LARGE_STRAIGHT) == 20
        assert calculate_score([1, 2, 3, 4, 6], Category.SMALL_STRAIGHT) == 0

    def test_full_house(self):
        assert calculate_score([1, 1, 2, 2, 2], Category.FULL_HOUSE) == 8
        assert calculate_score([1, 1, 1, 2, 2], Category.FULL_HOUSE) == 7
        assert calculate_score([1, 1, 1, 1, 2], Category.FULL_HOUSE) == 0

    def test_chance(self):
        assert calculate_score([1, 2, 3, 4, 5], Category.CHANCE) == 15

    def test_yatzy(self):
        assert calculate_score([1, 1, 1, 1, 1], Category.YATZY) == 50
        assert calculate_score([1, 1, 1, 1, 2], Category.YATZY) == 0
