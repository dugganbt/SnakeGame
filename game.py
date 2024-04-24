from turtle import Turtle, Screen, ontimer
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

# Constants in this code
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BG_COLOR = "black"
TITLE = "Snake"
ALIGNMENT = "center"
FONT = ("Helvetica", 18, "bold")


class Game(Turtle):
    """The game class handles the GUI and the game logic, integrating the
    snake, food, scoreboard and the game loop"""

    def __init__(self):
        super().__init__()
        self.game_is_on = True
        self.initialize_screen()
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard(high_score=0)
        self.setup_bindings()

        """blinking is done at the end of a game to ask the user to restart"""
        self.blinking_allowed = True
        self.blinker_state = True
        self.blinker = self.create_blinker()

    def initialize_screen(self):
        """Starts the screen on which the game is played."""
        self.screen = Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor(BG_COLOR)
        self.screen.title(TITLE)
        self.screen.tracer(0)  # turn on the tracer, automatic updating of screens

    def create_blinker(self):
        """Create and return a turtle for blinking text."""
        blinker = Turtle()
        blinker.hideturtle()
        blinker.penup()
        blinker.color("white")
        blinker.goto(0, -60)
        return blinker

    def setup_bindings(self):
        """Set up keyboard bindings for the game"""
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")
        self.screen.onkey(self.restart_game, "y")
        self.screen.onkey(self.quit_game, "n")

    def game_loop(self):
        """Loop during which game is run"""
        while self.game_is_on:
            self.screen.update()  # moves all segments forward before the screen updates
            time.sleep(0.1)  # sets the speed at which the snake moves
            self.snake.move()

            # Detect collision with food
            if self.snake.head.distance(self.food) < 15:
                self.food.refresh()
                self.snake.extend()
                self.scoreboard.increase_score()

            # Detect collision with wall
            if self.snake.head.xcor() > 280 or self.snake.head.xcor() < -280 or self.snake.head.ycor() > 280 or self.snake.head.ycor() < -280:
                self.game_is_on = False
                self.game_over()

            # Detect collision with tail
            for segment in self.snake.segments[1:]:
                if self.snake.head.distance(segment) < 10:
                    self.game_is_on = False
                    self.game_over()

    def game_over(self):
        """End the current game."""
        if self.scoreboard.score > self.scoreboard.high_score:
            self.scoreboard.new_high_score()
        self.scoreboard.goto(0, 0)
        self.scoreboard.write("GAME OVER.", align=ALIGNMENT, font=FONT)
        self.screen.update()
        self.prompt_restart()

    def prompt_restart(self):
        """Prompt for restarting the game."""
        self.blinker.clear()

        if self.blinker_state:
            self.blinker.write("RESTART GAME? (Y/N)", align=ALIGNMENT, font=FONT)
        # Toggle the blinker state
        self.blinker_state = not self.blinker_state

        # Only continue blinking if allowed
        if self.blinking_allowed:
            self.screen.ontimer(self.prompt_restart, 500)

    def restart_game(self):
        """Restart the game, but force the blinking prompt to end"""
        self.blinking_allowed = False
        self.screen.ontimer(self.complete_restart, 600)  # Wait slightly longer than a blink interval before resetting

    def complete_restart(self):
        """Reset all components of the game. Start game at the end"""
        self.blinker.clear()

        # Clear the screen and dispose of all items
        self.screen.clearscreen()

        # Re-setup the screen and game components
        self.initialize_screen()
        self.snake = Snake()  # recreate the snake object to ensure it's fully reset
        self.food = Food()  # recreate the food object
        self.scoreboard = Scoreboard(self.scoreboard.high_score)  # recreate the scoreboard

        self.setup_bindings()  # Reset key bindings

        # Reset game state variables
        self.game_is_on = True
        self.blinker_state = True  # Ensure the blinker state is reset
        self.blinking_allowed = True  # Allow blinking text again if needed

        # Start the game loop
        self.start_game()

    def quit_game(self):
        """Ends the game, closes the screen"""
        self.screen.bye()

    def start_game(self):
        """Initiates the game"""
        self.game_loop()