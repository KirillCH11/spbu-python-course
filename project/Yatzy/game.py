from .dice import Dice


class Game:
    """Manages the Yatzy game flow"""

    def __init__(self, players, max_rounds=15):
        self.players = players
        self.max_rounds = max_rounds
        self.current_round = 0
        self.dice = Dice()

    def play_round(self):
        """Play one round for all players"""
        self.current_round += 1
        print(f"\n--- Round {self.current_round} ---")

        for player in self.players:
            print(f"\n{player.name}'s turn:")
            self.play_turn(player)

            print(f"Score: {player.scorecard.get_total_score()}")

    def play_turn(self, player):
        """Play one turn for a player"""
        self.dice.reset_roll_count()
        self.dice.roll()  # First roll

        # Up to 2 re-rolls
        while self.dice.roll_count < 3:
            print(f"Dice: {self.dice.get_values()} (Roll {self.dice.roll_count})")

            if self.dice.roll_count < 3:
                keep_mask = player.choose_dice_to_keep(
                    self.dice.get_values(), self.dice.roll_count
                )
                if any(keep_mask):
                    print(
                        f"Keeping dice at positions: {[i + 1 for i, keep in enumerate(keep_mask) if keep]}"
                    )
                self.dice.roll(keep_mask)
            else:
                break

        final_dice = self.dice.get_values()
        print(f"Final dice: {final_dice}")

        available_categories = player.scorecard.get_available_categories()
        chosen_category = player.choose_category(final_dice, available_categories)

        from .scoring import calculate_score

        score = calculate_score(final_dice, chosen_category)

        player.scorecard.record_score(chosen_category, score)
        print(f"Scored {score} points in {chosen_category}")

    def play_game(self):
        """Play complete game until max rounds or all players finished"""
        print("Starting Yatzy Game!")
        print("Players:", [player.name for player in self.players])

        while self.current_round < self.max_rounds and not all(
            player.scorecard.is_complete() for player in self.players
        ):
            self.play_round()

        self.display_final_results()

    def display_final_results(self):
        """Display final scores and winner"""
        print("\n=== FINAL RESULTS ===")

        scores = []
        for player in self.players:
            total = player.scorecard.get_total_score()
            scores.append((player.name, total))
            print(f"{player.name}: {total} points")

        scores.sort(key=lambda x: x[1], reverse=True)
        print(f"\n🎉 Winner: {scores[0][0]} with {scores[0][1]} points!")

    def get_game_state(self):
        """Return current game state for testing"""
        return {
            "round": self.current_round,
            "scores": {
                player.name: player.scorecard.get_total_score()
                for player in self.players
            },
        }
