import pytest
from project.Yatzy.dice import Dice


class TestDice:
    def test_initial_values(self):
        dice = Dice()
        assert dice.values == [1, 1, 1, 1, 1]
        assert dice.roll_count == 0

    def test_roll_all_dice(self):
        dice = Dice()
        dice.roll()
        assert len(dice.values) == 5
        assert all(1 <= value <= 6 for value in dice.values)
        assert dice.roll_count == 1

    def test_roll_with_keep_mask(self):
        dice = Dice()
        dice.values = [1, 2, 3, 4, 5]
        keep_mask = [True, False, True, False, True]
        dice.roll(keep_mask)

        # Check that kept dice remained the same
        assert dice.values[0] == 1
        assert dice.values[2] == 3
        assert dice.values[4] == 5

    def test_reset_roll_count(self):
        dice = Dice()
        dice.roll_count = 3
        dice.reset_roll_count()
        assert dice.roll_count == 0

    def test_get_values(self):
        dice = Dice()
        dice.values = [1, 2, 3, 4, 5]
        values = dice.get_values()
        assert values == [1, 2, 3, 4, 5]
        # Test that it returns a copy
        values[0] = 6
        assert dice.values[0] == 1
