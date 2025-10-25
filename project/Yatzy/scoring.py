from enum import Enum
from typing import List


class Category(Enum):
    """Scoring categories for Yatzy game"""

    ONES = "ones"
    TWOS = "twos"
    THREES = "threes"
    FOURS = "fours"
    FIVES = "fives"
    SIXES = "sixes"
    PAIR = "pair"
    TWO_PAIRS = "two_pairs"
    THREE_KIND = "three_kind"
    FOUR_KIND = "four_kind"
    SMALL_STRAIGHT = "small_straight"
    LARGE_STRAIGHT = "large_straight"
    FULL_HOUSE = "full_house"
    CHANCE = "chance"
    YATZY = "yatzy"


def calculate_score(dice: List[int], category: Category) -> int:
    """
    Calculate score for given dice values and category.

    Args:
        dice: List of 5 dice values
        category: Scoring category

    Returns:
        Calculated score
    """
    counts = [dice.count(i) for i in range(1, 7)]

    if category == Category.ONES:
        return dice.count(1) * 1
    elif category == Category.TWOS:
        return dice.count(2) * 2
    elif category == Category.THREES:
        return dice.count(3) * 3
    elif category == Category.FOURS:
        return dice.count(4) * 4
    elif category == Category.FIVES:
        return dice.count(5) * 5
    elif category == Category.SIXES:
        return dice.count(6) * 6
    elif category == Category.PAIR:
        for i in range(6, 0, -1):
            if counts[i - 1] >= 2:
                return i * 2
        return 0
    elif category == Category.TWO_PAIRS:
        pairs = []
        for i in range(6, 0, -1):
            if counts[i - 1] >= 2:
                pairs.append(i)
        if len(pairs) >= 2:
            return pairs[0] * 2 + pairs[1] * 2
        return 0
    elif category == Category.THREE_KIND:
        for i in range(6, 0, -1):
            if counts[i - 1] >= 3:
                return i * 3
        return 0
    elif category == Category.FOUR_KIND:
        for i in range(6, 0, -1):
            if counts[i - 1] >= 4:
                return i * 4
        return 0
    elif category == Category.SMALL_STRAIGHT:
        if sorted(dice) == [1, 2, 3, 4, 5]:
            return 15
        return 0
    elif category == Category.LARGE_STRAIGHT:
        if sorted(dice) == [2, 3, 4, 5, 6]:
            return 20
        return 0
    elif category == Category.FULL_HOUSE:
        has_three = any(count == 3 for count in counts)
        has_two = any(count == 2 for count in counts)
        if has_three and has_two:
            return sum(dice)
        return 0
    elif category == Category.CHANCE:
        return sum(dice)
    elif category == Category.YATZY:
        if any(count == 5 for count in counts):
            return 50
        return 0

    return 0
