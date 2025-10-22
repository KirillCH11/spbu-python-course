import pytest
from project.Yatzy.scorecard import ScoreCard


class TestScoreCard:
    def test_initial_state(self):
        card = ScoreCard()
        assert len(card.categories) == 15
        assert all(score is None for score in card.categories.values())

    def test_record_score(self):
        card = ScoreCard()
        assert card.record_score("ones", 5) == True
        assert card.categories["ones"] == 5

        # Should not overwrite existing score
        assert card.record_score("ones", 10) == False
        assert card.categories["ones"] == 5

    def test_get_available_categories(self):
        card = ScoreCard()
        card.record_score("ones", 3)
        card.record_score("twos", 6)

        available = card.get_available_categories()
        assert "ones" not in available
        assert "twos" not in available
        assert "threes" in available
        assert len(available) == 13

    def test_get_total_score_no_bonus(self):
        card = ScoreCard()
        card.record_score("ones", 3)
        card.record_score("sixes", 12)
        card.record_score("chance", 15)

        assert card.get_total_score() == 30  # 3 + 12 + 15

    def test_get_total_score_with_bonus(self):
        card = ScoreCard()
        card.record_score("ones", 3)
        card.record_score("twos", 12)
        card.record_score("threes", 9)
        card.record_score("fours", 16)
        card.record_score("fives", 15)
        card.record_score("sixes", 18)  # Total upper = 73

        card.record_score("chance", 20)

        assert card.get_total_score() == 73 + 50 + 20

    def test_is_complete(self):
        card = ScoreCard()
        assert card.is_complete() == False

        # Fill all categories
        for category in card.categories:
            card.record_score(category, 0)

        assert card.is_complete() == True
