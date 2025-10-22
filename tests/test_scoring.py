import pytest
from project.Yatzy.scoring import calculate_score


class TestScoring:
    def test_upper_section(self):
        dice = [1, 1, 2, 3, 4]
        assert calculate_score(dice, "ones") == 2
        assert calculate_score(dice, "twos") == 2
        assert calculate_score(dice, "threes") == 3
        assert calculate_score(dice, "fours") == 4

    def test_pair(self):
        assert calculate_score([1, 1, 2, 3, 4], "pair") == 2
        assert calculate_score([1, 1, 2, 2, 3], "pair") == 4  # Highest pair
        assert calculate_score([1, 2, 3, 4, 5], "pair") == 0

    def test_two_pairs(self):
        assert calculate_score([1, 1, 2, 2, 3], "two_pairs") == 6
        assert calculate_score([1, 1, 2, 3, 4], "two_pairs") == 0

    def test_three_kind(self):
        assert calculate_score([1, 1, 1, 2, 3], "three_kind") == 3
        assert calculate_score([1, 2, 3, 4, 5], "three_kind") == 0

    def test_four_kind(self):
        assert calculate_score([1, 1, 1, 1, 2], "four_kind") == 4
        assert calculate_score([1, 1, 1, 2, 3], "four_kind") == 0

    def test_straights(self):
        assert calculate_score([1, 2, 3, 4, 5], "small_straight") == 15
        assert calculate_score([2, 3, 4, 5, 6], "large_straight") == 20
        assert calculate_score([1, 2, 3, 4, 6], "small_straight") == 0

    def test_full_house(self):
        assert calculate_score([1, 1, 2, 2, 2], "full_house") == 8
        assert calculate_score([1, 1, 1, 2, 2], "full_house") == 7
        assert calculate_score([1, 1, 1, 1, 2], "full_house") == 0

    def test_chance(self):
        assert calculate_score([1, 2, 3, 4, 5], "chance") == 15

    def test_yatzy(self):
        assert calculate_score([1, 1, 1, 1, 1], "yatzy") == 50
        assert calculate_score([1, 1, 1, 1, 2], "yatzy") == 0
