from typing import List, Dict, Optional
from .scoring import Category


class ScoreCard:
    """Tracks scores for all Yatzy categories."""

    def __init__(self) -> None:
        """Initialize scorecard with all categories empty."""
        self.categories: Dict[Category, Optional[int]] = {
            category: None for category in Category
        }

    def record_score(self, category: Category, score: int) -> bool:
        """
        Record score in a category if it's not already filled.

        Args:
            category: Category to record score in
            score: Score to record

        Returns:
            True if score was recorded, False if category was already filled
        """
        if self.categories[category] is None:
            self.categories[category] = score
            return True
        return False

    def get_available_categories(self) -> List[Category]:
        """
        Get list of categories that haven't been scored yet.

        Returns:
            List of available categories
        """
        return [cat for cat, score in self.categories.items() if score is None]

    def get_total_score(self) -> int:
        """
        Calculate total score including bonus if applicable.

        Returns:
            Total score with bonus
        """
        upper_categories = [
            Category.ONES,
            Category.TWOS,
            Category.THREES,
            Category.FOURS,
            Category.FIVES,
            Category.SIXES,
        ]

        upper_sum = sum(
            score
            for cat, score in self.categories.items()
            if cat in upper_categories and score is not None
        )

        bonus = 50 if upper_sum >= 63 else 0

        lower_sum = sum(
            score
            for cat, score in self.categories.items()
            if cat not in upper_categories and score is not None
        )

        return upper_sum + bonus + lower_sum

    def is_complete(self) -> bool:
        """
        Check if all categories are filled.

        Returns:
            True if all categories have scores, False otherwise
        """
        return all(score is not None for score in self.categories.values())
