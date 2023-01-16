# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 15:18:06 2023

@author: Arce
"""
import turtle

# Initial state of the pattern, represented as a 32-bit binary number
state = 1 << 31

# Set up turtle graphics window with width and height of 800 pixels
turtle.screensize(canvwidth=7680, canvheight=4800, bg='black')
# Set turtle speed to be the fastest possible
turtle.speed('fastest')
turtle.color('red')
# Pick the pen up and move turtle to starting position
turtle.penup()
turtle.setpos(0, 0)

# Create an empty 2D array to store the pattern
data = []

# Iterate over 32 rows
for i in range(32):
    # Create an empty list for the current row
    row = []
    # Iterate over 64 columns
    for j in range(64):
        # Append 1 to the current row if the corresponding bit in state is 1, else append 0
        row.append(1 if state >> j & 1 else 0)
    # Append the current row to the data array
    data.append(row)
    # Update the state using bitwise operations
    state = (state >> 1) ^ (state | state << 1)

for i in range(36):
    for j in range(64):
        if data[i][j] == 1:
            turtle.dot()
        turtle.forward(10)
    turtle.setpos(0, turtle.ycor() - 10)

# Wait for a mouse click before exiting turtle graphics window
turtle.exitonclick()
