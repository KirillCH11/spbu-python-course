import random


class Dice:
    """Represents a set of 5 dice for Yatzy game"""

    def __init__(self):
        self.values = [1] * 5
        self.roll_count = 0

    def roll(self, keep_mask=None):
        """
        Roll all dice that are not kept
        Args:
            keep_mask (list): List of booleans indicating which dice to keep
        """
        if keep_mask is None:
            keep_mask = [False] * 5

        for i in range(5):
            if not keep_mask[i]:
                self.values[i] = random.randint(1, 6)

        self.roll_count += 1

    def reset_roll_count(self):
        """Reset roll counter for new turn"""
        self.roll_count = 0

    def get_values(self):
        """Return current dice values"""
        return self.values.copy()
