from project.Yatzy.player import ConservativeBot, RiskyBot, AdaptiveBot
from project.Yatzy.game import Game


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
