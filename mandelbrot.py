"""
Created on Tue Dec 27 23:22:20 2022

@author: Arce
"""
import turtle

# Set the screen size and the maximum number of iterations
turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')
max_iterations = 256

# Define the escape time function
def escape_time(c):
    z = 0
    for i in range(max_iterations):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iterations

# Set the screen's background color
turtle.bgcolor("black")

# Set the turtle's pen color to white
turtle.pencolor("white")

# Set the turtle's pen size to 1 pixel
turtle.pensize(1)

# Set the turtle's speed to the maximum
turtle.speed(0)

# Iterate over the complex plane
for x in range(-400, 400):
    for y in range(-400, 400):
        c = complex(x/200, y/200)
        i = escape_time(c)
        if i == max_iterations:
            turtle.goto(x, y)
            turtle.dot()

# Hide the turtle and keep the screen open
turtle.hideturtle()
turtle.exitonclick()
