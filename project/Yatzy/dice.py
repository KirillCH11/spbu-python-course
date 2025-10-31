import random
from typing import List, Optional


class Dice:
    """A set of 5 dice for the Yatzy game."""

    def __init__(self) -> None:
        """Initialize dice with all values set to 1 and roll count to 0."""
        self.values: List[int] = [1] * 5
        self.roll_count: int = 0

    def roll(self, keep_mask: Optional[List[bool]] = None) -> None:
        """
        Roll dice that are not marked to be kept.

        Args:
            keep_mask: List of booleans indicating which dice to keep.
                      If None, all dice are rerolled.
        """
        if keep_mask is None:
            keep_mask = [False] * 5

        for i in range(5):
            if not keep_mask[i]:
                self.values[i] = random.randint(1, 6)

        self.roll_count += 1

    def reset_roll_count(self) -> None:
        """Reset the roll counter for a new turn."""
        self.roll_count = 0

    def get_values(self) -> List[int]:
        """
        Get current dice values.

        Returns:
            Copy of current dice values.
        """
        return self.values.copy()
