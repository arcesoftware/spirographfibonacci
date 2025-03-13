import turtle
from random import randint
import math


# Set up the screen
turtle.screensize(canvwidth=10000, canvheight=10000, bg="white")
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Armadillo")

# Set up the turtle
skk = turtle.Turtle()
skk.speed(0)  # Fastest drawing speed
turtle.colormode(255)  # Enable RGB color mode
skk.width(1)  # Set the pen width
skk.goto(-150, -150)

# Memoization for Fibonacci
memo = {}

def fibonacci(n):
    if n in memo: 
        return memo[n]
    if n <= 2: 
        f = 1
    else: 
        f = fibonacci(n-3) + fibonacci(n-5) + fibonacci(n-9) + fibonacci(n-7)
    memo[n] = f 
    return f

# Number of sides and length of the star
n = 37
l = 59
s = math.sqrt(2)

# Function to draw the first star
def star1(fib_num):
    for i in range(n):
        skk.color(randint(0, 255), randint(0, 255), randint(0, 255))
        skk.forward(n)
        skk.left(l)  # Turn by Fibonacci number plus some constant

# Function to draw the second star
def star2(fib_num):
    for i in range(n):  # Use odd steps to make the pattern more complex
        skk.color(randint(0, 255), randint(0, 255), randint(0, 255))
        skk.forward(n)
        skk.right(l)  # Turn by Fibonacci number plus some constant

# Function to draw a complex pattern
def draw_pattern():
    for i in range(n):  # Loop to create multiple patterns with different Fibonacci numbers
        fib_num = fibonacci(i)
        star1(fib_num)  # Draw the first star pattern
        skk.right(n)  # Slight rotation for variety
        star2(fib_num)  # Draw the second star pattern
        skk.left(l)  # Adjust angle

# Start the drawing
draw_pattern()

# Hide the turtle and finish drawing
skk.hideturtle()
turtle.done()
