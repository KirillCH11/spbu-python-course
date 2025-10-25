import random
from abc import ABC, abstractmethod
from .scorecard import ScoreCard
from .scoring import Category, calculate_score


class Player(ABC):
    """Abstract base class for all players."""

    def __init__(self, name: str):
        self.name = name
        self.scorecard = ScoreCard()

    @abstractmethod
    def choose_dice_to_keep(self, dice_values: list, roll_count: int) -> list:
        """Choose which dice to keep for next roll."""
        pass

    @abstractmethod
    def choose_category(
        self, dice_values: list, available_categories: list
    ) -> Category:
        """Choose category to score in."""
        pass


class ConservativeBot(Player):
    """Bot that prefers safe moves and guaranteed points."""

    def choose_dice_to_keep(self, dice_values: list, roll_count: int) -> list:
        counts = [dice_values.count(i) for i in range(1, 7)]
        keep_mask = [False] * 5

        for i in range(5):
            value = dice_values[i]
            if counts[value - 1] >= 2 or value >= 5:
                keep_mask[i] = True

        return keep_mask

    def choose_category(
        self, dice_values: list, available_categories: list
    ) -> Category:
        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category


class RiskyBot(Player):
    """Bot that goes for high-risk, high-reward moves."""

    def choose_dice_to_keep(self, dice_values: list, roll_count: int) -> list:
        keep_mask = [value >= 4 for value in dice_values]

        counts = [dice_values.count(i) for i in range(1, 7)]
        if any(count >= 3 for count in counts):
            for i in range(5):
                if counts[dice_values[i] - 1] >= 3:
                    keep_mask[i] = True

        return keep_mask

    def choose_category(
        self, dice_values: list, available_categories: list
    ) -> Category:
        high_value_categories = [
            Category.YATZY,
            Category.LARGE_STRAIGHT,
            Category.SMALL_STRAIGHT,
            Category.FOUR_KIND,
        ]

        for category in high_value_categories:
            if category in available_categories:
                return category

        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category


class AdaptiveBot(Player):
    """Bot that adapts strategy based on game state."""

    def choose_dice_to_keep(self, dice_values: list, roll_count: int) -> list:
        counts = [dice_values.count(i) for i in range(1, 7)]
        keep_mask = [False] * 5

        if roll_count == 1:
            for i in range(5):
                value = dice_values[i]
                if counts[value - 1] >= 2 or value >= 4:
                    keep_mask[i] = True
        else:
            for i in range(5):
                value = dice_values[i]
                if counts[value - 1] >= 2 or value >= 5:
                    keep_mask[i] = True

        return keep_mask

    def choose_category(
        self, dice_values: list, available_categories: list
    ) -> Category:
        upper_categories = [
            Category.ONES,
            Category.TWOS,
            Category.THREES,
            Category.FOURS,
            Category.FIVES,
            Category.SIXES,
        ]
        upper_available = [
            cat for cat in available_categories if cat in upper_categories
        ]

        if upper_available:
            current_upper = sum(
                self.scorecard.categories[cat] or 0 for cat in upper_categories
            )

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

        best_score = -1
        best_category = None

        for category in available_categories:
            score = calculate_score(dice_values, category)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category
