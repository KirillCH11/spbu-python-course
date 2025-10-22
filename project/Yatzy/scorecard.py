class ScoreCard:
    """Tracks scores for all scoring categories"""

    def __init__(self):
        self.categories = {
            # Upper section
            "ones": None,
            "twos": None,
            "threes": None,
            "fours": None,
            "fives": None,
            "sixes": None,
            # Lower section
            "pair": None,
            "two_pairs": None,
            "three_kind": None,
            "four_kind": None,
            "small_straight": None,
            "large_straight": None,
            "full_house": None,
            "chance": None,
            "yatzy": None,
        }

    def record_score(self, category, score):
        """Record score for a category if it's not already filled"""
        if self.categories[category] is None:
            self.categories[category] = score
            return True
        return False

    def get_available_categories(self):
        """Return list of categories that haven't been scored yet"""
        return [cat for cat, score in self.categories.items() if score is None]

    def get_total_score(self):
        """Calculate total score including bonus if applicable"""
        upper_sum = sum(
            score
            for cat, score in self.categories.items()
            if cat in ["ones", "twos", "threes", "fours", "fives", "sixes"]
            and score is not None
        )

        bonus = 50 if upper_sum >= 63 else 0

        lower_sum = sum(
            score
            for cat, score in self.categories.items()
            if cat not in ["ones", "twos", "threes", "fours", "fives", "sixes"]
            and score is not None
        )

        return upper_sum + bonus + lower_sum

    def is_complete(self):
        """Check if all categories are filled"""
        return all(score is not None for score in self.categories.values())
