from typing import List, Dict, Any
from .dice import Dice
from .scoring import calculate_score


class Game:
    """
    Manages the Yatzy game flow and coordinates players.

    Responsible for game rounds, player turns, and final scoring.
    """

    def __init__(self, players: List[Any], max_rounds: int = 15) -> None:
        """
        Initialize game with players and settings.

        Args:
            players: List of Player instances
            max_rounds: Maximum number of rounds to play (default 15)
        """
        self.players: List[Any] = players
        self.max_rounds: int = max_rounds
        self.current_round: int = 0
        self.dice: Dice = Dice()

    def play_round(self) -> None:
        """Play one round where each player takes a turn."""
        self.current_round += 1
        print(f"\n--- Round {self.current_round} ---")

        for player in self.players:
            print(f"\n{player.name}'s turn:")
            self.play_turn(player)
            print(f"Score: {player.scorecard.get_total_score()}")

    def play_turn(self, player: Any) -> None:
        """
        Play one turn for a player.

        Args:
            player: Player taking the turn
        """
        self.dice.reset_roll_count()
        self.dice.roll()

        while self.dice.roll_count < 3:
            print(f"Dice: {self.dice.get_values()} (Roll {self.dice.roll_count})")

            if self.dice.roll_count < 3:
                keep_mask = player.choose_dice_to_keep(
                    self.dice.get_values(), self.dice.roll_count
                )
                if any(keep_mask):
                    kept_positions = [i + 1 for i, keep in enumerate(keep_mask) if keep]
                    print(f"Keeping dice at positions: {kept_positions}")
                self.dice.roll(keep_mask)
            else:
                break

        final_dice = self.dice.get_values()
        print(f"Final dice: {final_dice}")

        available_categories = player.scorecard.get_available_categories()
        chosen_category = player.choose_category(final_dice, available_categories)

        score = calculate_score(final_dice, chosen_category)
        player.scorecard.record_score(chosen_category, score)
        print(f"Scored {score} points in {chosen_category.value}")

    def play_game(self) -> None:
        """Play complete game until max rounds or all players finished."""
        print("Starting Yatzy Game!")
        print("Players:", [player.name for player in self.players])

        while self.current_round < self.max_rounds and not all(
            player.scorecard.is_complete() for player in self.players
        ):
            self.play_round()

        self.display_final_results()

    def display_final_results(self) -> None:
        """Display final scores and announce winner."""
        print("\n=== FINAL RESULTS ===")

        scores = []
        for player in self.players:
            total = player.scorecard.get_total_score()
            scores.append((player.name, total))
            print(f"{player.name}: {total} points")

        scores.sort(key=lambda x: x[1], reverse=True)
        print(f"\nWinner: {scores[0][0]} with {scores[0][1]} points!")

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get current game state for testing.

        Returns:
            Dictionary with round number and player scores
        """
        return {
            "round": self.current_round,
            "scores": {
                player.name: player.scorecard.get_total_score()
                for player in self.players
            },
        }
