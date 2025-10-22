import pytest
from project.Yatzy.player import ConservativeBot, RiskyBot, AdaptiveBot


class TestPlayers:
    def test_bot_creation(self):
        bot1 = ConservativeBot("SafeBot")
        bot2 = RiskyBot("RiskyBot")
        bot3 = AdaptiveBot("AdaptiveBot")

        assert bot1.name == "SafeBot"
        assert bot2.name == "RiskyBot"
        assert bot3.name == "AdaptiveBot"

    def test_choose_dice_to_keep(self):
        bot = ConservativeBot("TestBot")
        dice = [1, 1, 3, 4, 6]
        keep_mask = bot.choose_dice_to_keep(dice, 1)

        assert len(keep_mask) == 5
        assert isinstance(keep_mask[0], bool)

    def test_choose_category(self):
        bot = ConservativeBot("TestBot")
        dice = [1, 1, 1, 2, 2]
        available = ["ones", "twos", "three_kind", "full_house"]

        chosen = bot.choose_category(dice, available)
        assert chosen in available

    def test_scorecard_integration(self):
        bot = ConservativeBot("TestBot")
        assert bot.scorecard.get_total_score() == 0

        bot.scorecard.record_score("ones", 3)
        assert bot.scorecard.get_total_score() == 3
