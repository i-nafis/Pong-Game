import tkinter as tk
from tkinter import colorchooser, messagebox
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

class PongGame:
    # Constants for setup
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PADDLE_WIDTH = 20
    PADDLE_HEIGHT = 100
    R_PADDLE_POSITION = (350, 0)
    L_PADDLE_POSITION = (-350, 0)
    UPPER_BOUNDARY = SCREEN_HEIGHT / 2 - 10
    LOWER_BOUNDARY = -SCREEN_HEIGHT / 2 + 10
    RIGHT_BOUNDARY = SCREEN_WIDTH / 2
    LEFT_BOUNDARY = -SCREEN_WIDTH / 2

    def __init__(self):
        # Screen setup
        self.screen = Screen()
        self.screen.setup(width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT)
        self.screen.title("PONG GAME - ENHANCED EDITION")
        self.screen.bgcolor("black")
        self.screen.tracer(0)

        # Game objects
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.r_paddle = Paddle(self.R_PADDLE_POSITION)
        self.l_paddle = Paddle(self.L_PADDLE_POSITION)

        # Game state
        self.is_paused = False
        self.game_speed = 1.0
        self.winning_score = 5
        self.game_active = True
        self.current_difficulty = "default"

        # Initialize UI
        self.setup_controls()
        self.setup_keybindings()

        # Start game
        self.game_loop()

    def setup_controls(self):
        """Initialize the control window and buttons"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Pong Game Controls")
        self.root.geometry("400x300")

        # Game controls frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)

        # Pause button
        self.pause_button = tk.Button(
            controls_frame,
            text="Pause",
            command=self.toggle_pause,
            width=15
        )
        self.pause_button.pack(pady=5)

        # Reset button
        tk.Button(
            controls_frame,
            text="Reset Game",
            command=self.reset_game,
            width=15
        ).pack(pady=5)

        # Speed control
        speed_frame = tk.Frame(controls_frame)
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="Game Speed:").pack(side=tk.LEFT)
        self.speed_entry = tk.Entry(speed_frame, width=5)
        self.speed_entry.insert(0, str(self.game_speed))
        self.speed_entry.pack(side=tk.LEFT)
        tk.Button(
            speed_frame,
            text="Set Speed",
            command=self.update_speed_from_entry
        ).pack(side=tk.LEFT)

        # Winning score setter
        score_frame = tk.Frame(controls_frame)
        score_frame.pack(pady=5)
        tk.Label(score_frame, text="Winning Score:").pack(side=tk.LEFT)
        tk.Entry(
            score_frame,
            width=5,
            textvariable=tk.StringVar(value=str(self.winning_score))
        ).pack(side=tk.LEFT)

        # Color controls
        tk.Button(
            controls_frame,
            text="Change Background Color",
            command=self.change_background_color,
            width=25
        ).pack(pady=5)

        # Add difficulty modes
        tk.Button(
            controls_frame,
            text="Easy Mode",
            command=lambda: self.set_difficulty("easy"),
            width=15
        ).pack(pady=2)

        tk.Button(
            controls_frame,
            text="Hard Mode",
            command=lambda: self.set_difficulty("hard"),
            width=15
        ).pack(pady=2)

        self.root.protocol("WM_DELETE_WINDOW", self.hide_controls)

    def setup_keybindings(self):
        """Set up keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.r_paddle.go_up, "Up")
        self.screen.onkeypress(self.r_paddle.go_down, "Down")
        self.screen.onkeypress(self.l_paddle.go_up, "w")
        self.screen.onkeypress(self.l_paddle.go_down, "s")
        self.screen.onkey(self.toggle_pause, "space")
        self.screen.onclick(self.open_controls)

    def toggle_pause(self):
        """Toggle game pause state"""
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")
        self.setup_keybindings()  # Re-bind keys after pausing or resuming

    def reset_game(self):
        """Reset the game state"""
        self.scoreboard.reset_scores()
        self.ball.reset_position()
        self.game_active = True
        self.is_paused = False
        self.pause_button.config(text="Pause")
        self.setup_keybindings()  # Re-bind keys after resetting the game

    def update_speed(self, value):
        """Update game speed"""
        self.game_speed = float(value)
        self.ball.move_speed = 0.1 / self.game_speed

    def update_speed_from_entry(self):
        """Update game speed from the entry widget"""
        try:
            speed_value = float(self.speed_entry.get())
            if speed_value > 0:
                self.update_speed(speed_value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for speed.")

    def set_difficulty(self, mode):
        """Set game difficulty"""
        if mode == "easy":
            if self.current_difficulty != "easy":
                self.current_difficulty = "easy"
                self.ball.move_speed = 0.1
                self.r_paddle.shapesize(stretch_wid=6, stretch_len=1)  # More spread out in Y-axis only
                self.l_paddle.shapesize(stretch_wid=6, stretch_len=1)
            else:
                self.current_difficulty = "default"
                self.ball.move_speed = 0.1
                self.r_paddle.shapesize(stretch_wid=5, stretch_len=1)
                self.l_paddle.shapesize(stretch_wid=5, stretch_len=1)
        elif mode == "hard":
            self.current_difficulty = "hard"
            self.ball.move_speed = 0.05
            self.r_paddle.shapesize(stretch_wid=3, stretch_len=1)  # Smaller paddle in Y-axis only
            self.l_paddle.shapesize(stretch_wid=3, stretch_len=1)
        self.reset_game()

    def change_background_color(self):
        """Change background color with automatic contrast adjustment"""
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.screen.bgcolor(color)
            # Adjust object colors based on background brightness
            contrast_color = "black" if self.is_light_color(color) else "white"
            for obj in [self.ball, self.r_paddle, self.l_paddle, self.scoreboard]:
                obj.color(contrast_color)
        self.setup_keybindings()  # Re-bind keys after changing the color

    @staticmethod
    def is_light_color(hex_color):
        """Determine if a color is light or dark"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness > 128

    def open_controls(self, x, y):
        """Show the control window"""
        self.root.deiconify()
        self.root.lift()  # Bring window to front
        self.root.focus_force()  # Force focus on window
        self.setup_keybindings()  # Ensure keybindings are active after opening the control window

    def hide_controls(self):
        """Hide the control window"""
        self.root.withdraw()
        self.screen.listen()  # Re-enable screen key listening when the control window is hidden
        self.setup_keybindings()  # Re-bind keys after hiding the control window

    def check_win_condition(self):
        """Check if either player has won"""
        if max(self.scoreboard.l_score, self.scoreboard.r_score) >= self.winning_score:
            winner = "Left" if self.scoreboard.l_score > self.scoreboard.r_score else "Right"
            messagebox.showinfo("Game Over", f"{winner} player wins!")
            self.game_active = False
            return True
        return False

    def game_loop(self):
        """Main game loop"""
        if not self.is_paused and self.game_active:
            time.sleep(self.ball.move_speed)
            self.screen.update()
            self.ball.move()

            # Boundary collisions
            if self.ball.ycor() > self.UPPER_BOUNDARY or self.ball.ycor() < self.LOWER_BOUNDARY:
                self.ball.bounce_y()

            # Paddle collisions
            if ((self.ball.distance(self.r_paddle) < 50 and self.ball.xcor() > 330) or
                    (self.ball.distance(self.l_paddle) < 50 and self.ball.xcor() < -330)):
                self.ball.bounce_x()

            # Scoring
            if self.ball.xcor() > self.RIGHT_BOUNDARY:
                self.ball.reset_position()
                self.scoreboard.l_point()
                self.check_win_condition()
            elif self.ball.xcor() < self.LEFT_BOUNDARY:
                self.ball.reset_position()
                self.scoreboard.r_point()
                self.check_win_condition()

        self.screen.ontimer(self.game_loop, 20)

if __name__ == "__main__":
    game = PongGame()
    game.root.mainloop()
