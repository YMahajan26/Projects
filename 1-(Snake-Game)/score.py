from turtle import Turtle

ALIGNMENT = "center"
FONT = ('Ariel',20,'bold')

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.color("White")
        self.hideturtle()
        self.penup()
        self.goto(0,270)
        self.write(f"Score: {self.points} ",align=ALIGNMENT,font=FONT)

    def increase_score(self):
        self.clear()
        self.points +=1
        self.write(f"Score: {self.points} ", align=ALIGNMENT, font=FONT)


    def game_over(self):
        self.goto(0,0)
        self.color("Yellow")
        self.write("GAME OVER ", align=ALIGNMENT, font=FONT)
