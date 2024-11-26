from turtle import Turtle
from typing import Tuple, Optional
import random
import math


class Ball(Turtle):
    """
    A ball class for the Pong game that handles movement, collisions, and effects
    """

    DEFAULT_COLOR = "white"
    DEFAULT_SPEED = 0.1
    DEFAULT_MOVE_DISTANCE = (10, 10)
    DEFAULT_SIZE = 1.0
    MIN_SPEED = 0.02
    SPEED_DECAY = 0.9
    SPEED_BOOST = 1.1

    def __init__(
            self,
            color: str = DEFAULT_COLOR,
            initial_speed: float = DEFAULT_SPEED,
            move_distance: Tuple[int, int] = DEFAULT_MOVE_DISTANCE,
            size: float = DEFAULT_SIZE,
            random_start: bool = True
    ):
        """
        Initialize a new ball

        Args:
            color: Ball color (default: white)
            initial_speed: Starting movement speed (default: 0.1)
            move_distance: (x, y) movement increments (default: (10, 10))
            size: Size multiplier for the ball (default: 1.0)
            random_start: Whether to randomize initial direction (default: True)
        """
        super().__init__()
        self._setup_ball(color, size)
        self.x_move, self.y_move = move_distance
        self.move_speed = initial_speed
        self.initial_speed = initial_speed
        self.initial_move_distance = move_distance
        self.random_start = random_start
        self.is_active = True
        self.trail_effect = False
        self._setup_trail()

        if random_start:
            self._randomize_direction()

    def _setup_ball(self, color: str, size: float) -> None:
        """Set up the initial ball appearance"""
        self.color(color)
        self.shape("circle")
        self.shapesize(size, size)
        self.penup()
        self.goto(0, 0)

    def _setup_trail(self) -> None:
        """Set up trail effect settings"""
        self.trail = Turtle()
        self.trail.hideturtle()
        self.trail.penup()
        self.trail.color(self.color()[0])

    def _randomize_direction(self) -> None:
        """Randomize the ball's initial direction"""
        angle = random.uniform(-60, 60)  # Increase the range for more angular movement
        if random.random() < 0.5:
            angle += 180

        # Convert angle to movement components
        rad = math.radians(angle)
        speed = math.sqrt(self.x_move ** 2 + self.y_move ** 2)
        self.x_move = speed * math.cos(rad)
        self.y_move = speed * math.sin(rad)

    def move(self) -> None:
        """Move the ball according to current velocity"""
        if not self.is_active:
            return

        if self.trail_effect:
            self.trail.goto(self.pos())
            self.trail.pendown()

        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

        if self.trail_effect:
            self.trail.penup()

    def bounce_y(self, speed_boost: bool = False) -> None:
        """
        Bounce the ball vertically

        Args:
            speed_boost: Whether to increase speed after bounce
        """
        self.y_move *= -1
        self._add_randomness_to_bounce()
        if speed_boost:
            self._boost_speed()

    def bounce_x(self, speed_boost: bool = False) -> None:
        """
        Bounce the ball horizontally

        Args:
            speed_boost: Whether to increase speed after bounce
        """
        self.x_move *= -1
        self._add_randomness_to_bounce()
        if speed_boost:
            self._boost_speed()
        else:
            self._decay_speed()

    def _add_randomness_to_bounce(self) -> None:
        """Add slight randomness to the bounce to avoid straight paths"""
        angle_variation = random.uniform(-15, 15)  # Increase angle variation for more angular bounces
        rad = math.radians(angle_variation)
        new_x_move = self.x_move * math.cos(rad) - self.y_move * math.sin(rad)
        new_y_move = self.x_move * math.sin(rad) + self.y_move * math.cos(rad)
        self.x_move = new_x_move
        self.y_move = new_y_move

    def _boost_speed(self) -> None:
        """Increase ball speed"""
        self.move_speed *= self.SPEED_BOOST

    def _decay_speed(self) -> None:
        """Decrease ball speed but not below minimum"""
        self.move_speed = max(self.MIN_SPEED, self.move_speed * self.SPEED_DECAY)

    def reset_position(self) -> None:
        """Reset ball to center with initial speed"""
        self.goto(0, 0)
        self.move_speed = self.initial_speed
        self.x_move, self.y_move = self.initial_move_distance

        if self.random_start:
            self._randomize_direction()
        else:
            self.bounce_x()

        if self.trail_effect:
            self.clear_trail()

    def toggle_trail(self) -> None:
        """Toggle trail effect on/off"""
        self.trail_effect = not self.trail_effect
        if not self.trail_effect:
            self.clear_trail()

    def clear_trail(self) -> None:
        """Clear the trail effect"""
        self.trail.clear()

    def pause(self) -> None:
        """Pause ball movement"""
        self.is_active = False

    def resume(self) -> None:
        """Resume ball movement"""
        self.is_active = True

    def get_velocity(self) -> Tuple[float, float]:
        """Get current velocity components"""
        return (self.x_move, self.y_move)

    def get_speed(self) -> float:
        """Get current speed"""
        return math.sqrt(self.x_move ** 2 + self.y_move ** 2)

    def set_color(self, color: str) -> None:
        """Set ball and trail color"""
        self.color(color)
        self.trail.color(color)

    def predict_path(self, steps: int = 10) -> list[Tuple[float, float]]:
        """
        Predict future ball positions

        Args:
            steps: Number of future positions to predict

        Returns:
            List of predicted (x, y) positions
        """
        positions = []
        x, y = self.xcor(), self.ycor()
        dx, dy = self.x_move, self.y_move

        for _ in range(steps):
            x += dx
            y += dy
            positions.append((x, y))

        return positions
