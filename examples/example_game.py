#!/usr/bin/env python3

import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from project.Yatzy.player import ConservativeBot, RiskyBot, AdaptiveBot
from project.Yatzy.game import Game
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def main():
    # Create bots with different strategies
    bots = [
        ConservativeBot("SafePlayer"),
        RiskyBot("RiskyPlayer"),
        AdaptiveBot("SmartPlayer"),
    ]

    # Create and play game
    game = Game(bots, max_rounds=15)
    game.play_game()


if __name__ == "__main__":
    main()
