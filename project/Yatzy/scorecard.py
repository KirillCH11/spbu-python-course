from .scoring import Category


class ScoreCard:
    """Tracks scores for all scoring categories."""

    def __init__(self):
        self.categories = {category: None for category in Category}

    def record_score(self, category: Category, score: int) -> bool:
        """Record score for a category if it's not already filled."""
        if self.categories[category] is None:
            self.categories[category] = score
            return True
        return False

    def get_available_categories(self) -> list:
        """Return list of categories that haven't been scored yet."""
        return [cat for cat, score in self.categories.items() if score is None]

    def get_total_score(self) -> int:
        """Calculate total score including bonus if applicable."""
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
        """Check if all categories are filled."""
        return all(score is not None for score in self.categories.values())
