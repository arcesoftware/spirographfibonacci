"""
Created on Fri Jan 13 10:55:16 2023

@author: Arce
"""
import turtle
import math
turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')

def seed_of_life(radius):
    skk = turtle.Turtle()
    skk.color("red")
    skk.speed(3)
    skk.penup()
    skk.goto(0,0)
    skk.pendown()

    for i in range(6):
        angle = i * 60
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        skk.penup()
        skk.goto(x, y)
        skk.pendown()
        skk.circle(radius)
    turtle.done()

radius = int(input("Enter the radius of the circles: "))
seed_of_life(radius)
