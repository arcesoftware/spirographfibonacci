# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 02:24:01 2022

@author: Juan Arce
"""
import turtle
import numpy as np
from math import atan2

# Set the values of ρ, σ, and β
rho = 28
sigma = 10
beta = 8/3
scale = 10
dt = 0.01  # time step

# Set the initial conditions
x, y, z = 1.0, 1.0, 1.0
dx, dy = 0.0, 0.0  # initialize the x velocity
# Create a turtle and set the pen size
t = turtle.Turtle()
t.speed('fastest')
t.pensize(1)
t.pencolor('red')
t.radians()
t.pendown()

while True:
    t.setpos(x*scale, y*scale)
    t.setheading(atan2(dy, dx))
    
    # Solve the differential equations
    dx = (sigma * (y - x)) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    
    x += dx
    y += dy
    z += dz

# Keep the window open until it is closed
turtle.mainloop()
