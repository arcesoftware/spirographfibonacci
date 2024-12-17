
import turtle
import math

turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')
radius = 180

def seed_of_life(radius):
    skk = turtle.Turtle()
    skk.color("red")
    skk.speed(3)
    skk.penup()
    skk.goto(0, 0)
    skk.pendown()
    skk.hideturtle()

    # Rotate the pattern by 45 degrees by adding 45 to the angles
    initial_rotation = 90

    for i in range(6):
        angle = i * 60 + initial_rotation
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        skk.penup()
        skk.goto(x, y)
        skk.pendown()
        skk.circle(radius)

    turtle.done()

seed_of_life(radius)
