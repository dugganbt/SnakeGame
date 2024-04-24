from turtle import Turtle, Screen, ontimer, bye

ALIGNMENT = "center"
FONT = ("Helvetica", 18, "bold")


class Scoreboard(Turtle):

    def __init__(self, high_score):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, 270)
        self.score = 0
        self.high_score = high_score
        self.update_scoreboard()

    def update_scoreboard(self):
        if self.high_score ==0:
            self.clear()
            self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
        else:
            self.clear()
            self.write(f"Score: {self.score} | Highscore: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset_score(self):
        self.score = 0
        self.goto(0, 270)
        self.update_scoreboard()

    def new_high_score(self):
        self.high_score = self.score
        self.update_scoreboard()

