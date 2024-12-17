import turtle
import math
turtle.screensize(canvwidth=680, canvheight=800, bg='black')
def seed_of_life(radius):
    skk = turtle.Turtle()
    skk.color("red")
    skk.speed(0)  # Set maximum speed for faster drawing
    skk.hideturtle()  # Hide the turtle pointer
    initial_rotation = 90  # Rotate the pattern by 90 degrees
    positions = [
        (
            radius * math.cos(math.radians(i * 60 + initial_rotation)),
            radius * math.sin(math.radians(i * 60 + initial_rotation))
        )
        for i in range(6)
    ]
    # Draw circles
    for x, y in positions:
        skk.penup()
        skk.goto(x, y)
        skk.pendown()
        skk.circle(radius)
    turtle.done()
seed_of_life(180)

