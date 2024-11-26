from turtle import Turtle
from typing import Tuple, Optional


class Paddle(Turtle):
    """
    A paddle class for the Pong game that handles paddle movement and appearance
    """

    DEFAULT_COLOR = "white"
    DEFAULT_MOVE_INCREMENT = 20
    DEFAULT_SIZE = (5, 1)  # (height, width)
    UPPER_BOUNDARY = 250
    LOWER_BOUNDARY = -250

    def __init__(
            self,
            position: Tuple[int, int],
            color: str = DEFAULT_COLOR,
            move_increment: int = DEFAULT_MOVE_INCREMENT,
            size: Optional[Tuple[int, int]] = None
    ):
        """
        Initialize a new paddle

        Args:
            position: Initial (x, y) position of the paddle
            color: Color of the paddle (default: white)
            move_increment: Movement speed in pixels (default: 20)
            size: Optional tuple of (height, width) for paddle size
        """
        super().__init__()
        self.size = size or self.DEFAULT_SIZE
        self._setup_paddle(position, color)
        self.move_increment = move_increment
        self.moving = False  # For smooth continuous movement
        self.direction = 0  # Current movement direction (-1, 0, or 1)

    def _setup_paddle(self, position: Tuple[int, int], color: str) -> None:
        """Set up the initial paddle appearance and position"""
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=self.size[0], stretch_len=self.size[1])
        self.penup()
        self.goto(position)

    def go_up(self) -> None:
        """Move the paddle up if within bounds"""
        if self.ycor() < self.UPPER_BOUNDARY:
            new_y = self.ycor() + self.move_increment
            self.goto(self.xcor(), min(new_y, self.UPPER_BOUNDARY))

    def go_down(self) -> None:
        """Move the paddle down if within bounds"""
        if self.ycor() > self.LOWER_BOUNDARY:
            new_y = self.ycor() - self.move_increment
            self.goto(self.xcor(), max(new_y, self.LOWER_BOUNDARY))

    def start_move(self, direction: int) -> None:
        """Start continuous movement in the specified direction"""
        self.moving = True
        self.direction = direction

    def stop_move(self) -> None:
        """Stop continuous movement"""
        self.moving = False
        self.direction = 0

    def update(self) -> None:
        """Update paddle position for continuous movement"""
        if self.moving:
            if self.direction > 0:
                self.go_up()
            elif self.direction < 0:
                self.go_down()

    def stretch_y(self, factor: float) -> None:
        """
        Adjust the paddle height by a factor

        Args:
            factor: Multiplication factor for paddle height
        """
        new_height = self.size[0] * factor
        self.size = (new_height, self.size[1])
        self.shapesize(stretch_wid=new_height, stretch_len=self.size[1])

    def reset_size(self) -> None:
        """Reset paddle to default size"""
        self.size = self.DEFAULT_SIZE
        self.shapesize(stretch_wid=self.size[0], stretch_len=self.size[1])

    def get_edges(self) -> Tuple[float, float, float, float]:
        """
        Get the coordinates of paddle edges for precise collision detection

        Returns:
            Tuple of (left, right, top, bottom) edge coordinates
        """
        half_width = self.size[1] * 10  # 10 is default turtle size
        half_height = self.size[0] * 10
        return (
            self.xcor() - half_width,
            self.xcor() + half_width,
            self.ycor() + half_height,
            self.ycor() - half_height
        )