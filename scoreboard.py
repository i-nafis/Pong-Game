from turtle import Turtle
from typing import Tuple
import json

FONT = ("Courier", 40, "bold")
SMALL_FONT = ("Courier", 16, "normal")
ALIGNMENT = "center"
HIGH_SCORE_FILE = "pong_scores.json"


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.winning_score = 11
        self.game_active = True
        self.high_score = self._load_high_score()
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        self.clear()
        # Main scores at the top
        self.goto(-100, 240)
        self.write(self.l_score, align=ALIGNMENT, font=FONT)
        self.goto(100, 240)
        self.write(self.r_score, align=ALIGNMENT, font=FONT)

        # Small high score display
        self.goto(0, 260)
        self.write(f"Best: {self.high_score}", align=ALIGNMENT, font=SMALL_FONT)

    def l_point(self) -> None:
        self.l_score += 1
        self._check_winner()
        self.update_scoreboard()

    def r_point(self) -> None:
        self.r_score += 1
        self._check_winner()
        self.update_scoreboard()

    def _check_winner(self) -> None:
        """Check for winner and update high score if needed"""
        if max(self.l_score, self.r_score) >= self.winning_score:
            self.game_active = False
            # Update high score if needed
            current_max = max(self.l_score, self.r_score)
            if current_max > self.high_score:
                self.high_score = current_max
                self._save_high_score()
            # Display winner message
            winner = "LEFT" if self.l_score > self.r_score else "RIGHT"
            self.show_winner_message(winner)

    def show_winner_message(self, winner: str) -> None:
        """Briefly show winner message"""
        self.goto(0, 0)
        self.write(f"{winner} WINS!", align=ALIGNMENT, font=FONT)

    def reset_scores(self) -> None:
        """Reset game state"""
        self.l_score = 0
        self.r_score = 0
        self.game_active = True
        self.clear()
        self.update_scoreboard()

    def _load_high_score(self) -> int:
        """Load high score from file"""
        try:
            with open(HIGH_SCORE_FILE, 'r') as file:
                data = json.load(file)
                return data.get('high_score', 0)
        except FileNotFoundError:
            return 0

    def _save_high_score(self) -> None:
        """Save high score to file"""
        with open(HIGH_SCORE_FILE, 'w') as file:
            json.dump({'high_score': self.high_score}, file)

    def get_score(self) -> Tuple[int, int]:
        """Return current scores"""
        return self.l_score, self.r_score

    def is_game_active(self) -> bool:
        """Check if game is still active"""
        return self.game_active

    def set_winning_score(self, score: int) -> None:
        """Set custom winning score"""
        if score > 0:
            self.winning_score = score