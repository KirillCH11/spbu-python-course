import random
from abc import ABC, abstractmethod
from .scorecard import ScoreCard


class Player(ABC):
    """Abstract base class for all players"""

    def __init__(self, name):
        self.name = name
        self.scorecard = ScoreCard()

    @abstractmethod
    def choose_dice_to_keep(self, dice_values, roll_count):
        """Choose which dice to keep for next roll"""
        pass

    @abstractmethod
    def choose_category(self, dice_values, available_categories):
        """Choose category to score in"""
        pass


class ConservativeBot(Player):
    """Bot that prefers safe moves and guaranteed points"""

    def choose_dice_to_keep(self, dice_values, roll_count):
        # Keep high values and pairs/triplets
        counts = [dice_values.count(i) for i in range(1, 7)]
        keep_mask = [False] * 5

        for i in range(5):
            value = dice_values[i]
            if counts[value - 1] >= 2 or value >= 5:
                keep_mask[i] = True

        return keep_mask

    def choose_category(self, dice_values, available_categories):
        from .scoring import calculate_score

        # Prefer categories with highest guaranteed score
        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category


class RiskyBot(Player):
    """Bot that goes for high-risk, high-reward moves"""

    def choose_dice_to_keep(self, dice_values, roll_count):
        # Keep only high values, aiming for straights or yatzy
        keep_mask = [value >= 4 for value in dice_values]

        # If we have many of a kind, keep them all
        counts = [dice_values.count(i) for i in range(1, 7)]
        if any(count >= 3 for count in counts):
            for i in range(5):
                if counts[dice_values[i] - 1] >= 3:
                    keep_mask[i] = True

        return keep_mask

    def choose_category(self, dice_values, available_categories):
        from .scoring import calculate_score

        # Prefer high-value categories even if score is low
        high_value_categories = [
            "yatzy",
            "large_straight",
            "small_straight",
            "four_kind",
        ]

        for category in high_value_categories:
            if category in available_categories:
                return category

        # Fallback to highest scoring category
        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category


class AdaptiveBot(Player):
    """Bot that adapts strategy based on game state"""

    def choose_dice_to_keep(self, dice_values, roll_count):
        counts = [dice_values.count(i) for i in range(1, 7)]
        keep_mask = [False] * 5

        # Strategy depends on roll count
        if roll_count == 1:
            # First roll: keep high values and pairs
            for i in range(5):
                value = dice_values[i]
                if counts[value - 1] >= 2 or value >= 4:
                    keep_mask[i] = True
        else:
            # Subsequent rolls: be more selective
            for i in range(5):
                value = dice_values[i]
                if counts[value - 1] >= 2 or value >= 5:
                    keep_mask[i] = True

        return keep_mask

    def choose_category(self, dice_values, available_categories):
        from .scoring import calculate_score

        # Fill upper section first if it helps get bonus
        upper_categories = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        upper_available = [
            cat for cat in available_categories if cat in upper_categories
        ]

        if upper_available:
            # Calculate current upper score
            current_upper = sum(
                self.scorecard.categories[cat] or 0 for cat in upper_categories
            )

            # If close to bonus, prioritize upper section
            if current_upper >= 50:
                best_upper_score = -1
                best_upper_category = None

                for category in upper_available:
                    score = calculate_score(dice_values, category)
                    if score > best_upper_score:
                        best_upper_score = score
                        best_upper_category = category

                if best_upper_category:
                    return best_upper_category

        # Otherwise choose highest scoring category
        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category
