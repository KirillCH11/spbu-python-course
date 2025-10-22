def calculate_score(dice, category):
    """
    Calculate score for given dice values and category

    Args:
        dice (list): List of 5 dice values
        category (str): Scoring category

    Returns:
        int: Calculated score
    """
    counts = [dice.count(i) for i in range(1, 7)]

    if category == "ones":
        return dice.count(1) * 1
    elif category == "twos":
        return dice.count(2) * 2
    elif category == "threes":
        return dice.count(3) * 3
    elif category == "fours":
        return dice.count(4) * 4
    elif category == "fives":
        return dice.count(5) * 5
    elif category == "sixes":
        return dice.count(6) * 6

    elif category == "pair":
        for i in range(6, 0, -1):
            if counts[i - 1] >= 2:
                return i * 2
        return 0

    elif category == "two_pairs":
        pairs = []
        for i in range(6, 0, -1):
            if counts[i - 1] >= 2:
                pairs.append(i)
        if len(pairs) >= 2:
            return pairs[0] * 2 + pairs[1] * 2
        return 0

    elif category == "three_kind":
        for i in range(6, 0, -1):
            if counts[i - 1] >= 3:
                return i * 3
        return 0

    elif category == "four_kind":
        for i in range(6, 0, -1):
            if counts[i - 1] >= 4:
                return i * 4
        return 0

    elif category == "small_straight":
        if sorted(dice) == [1, 2, 3, 4, 5]:
            return 15
        return 0

    elif category == "large_straight":
        if sorted(dice) == [2, 3, 4, 5, 6]:
            return 20
        return 0

    elif category == "full_house":
        has_three = any(count == 3 for count in counts)
        has_two = any(count == 2 for count in counts)
        if has_three and has_two:
            return sum(dice)
        return 0

    elif category == "chance":
        return sum(dice)

    elif category == "yatzy":
        if any(count == 5 for count in counts):
            return 50
        return 0

    return 0
