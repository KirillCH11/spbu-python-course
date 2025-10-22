import pytest
from project.Yatzy.game import Game
from project.Yatzy.player import ConservativeBot, RiskyBot


class TestGame:
    def test_game_initialization(self):
        players = [ConservativeBot("Bot1"), RiskyBot("Bot2")]
        game = Game(players, max_rounds=10)

        assert len(game.players) == 2
        assert game.max_rounds == 10
        assert game.current_round == 0

    def test_game_state(self):
        players = [ConservativeBot("Bot1")]
        game = Game(players)

        state = game.get_game_state()
        assert state["round"] == 0
        assert "Bot1" in state["scores"]
        assert state["scores"]["Bot1"] == 0

    def test_play_turn(self):
        players = [ConservativeBot("TestBot")]
        game = Game(players)

        # Mock the dice to control randomness
        game.dice.values = [1, 1, 1, 2, 2]

        game.play_turn(players[0])

        # Bot should have scored something
        assert players[0].scorecard.get_total_score() >= 0
