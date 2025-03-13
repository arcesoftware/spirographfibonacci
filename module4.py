import turtle
from random import randint
import math

# Number of sides and length of the star
n = 12  # Number of segments in the star pattern
s = 10  # Size scaling factor for each Fibonacci step

# Set up the screen
turtle.screensize(canvwidth=10000, canvheight=10000, bg="black")
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Symmetrical Fibonacci Design")

# Set up the turtle
skk = turtle.Turtle()
skk.speed(0)  # Fastest drawing speed
turtle.colormode(255)  # Enable RGB color mode
skk.width(2)  # Set the pen width
skk.goto(0, 0)

# Memoization for Fibonacci
memo = {}

def fibonacci(n):
    """Generate Fibonacci sequence with custom rules."""
    if n in memo:
        return memo[n]
    if n <= 2:
        f = 1
    else:
        f = fibonacci(n-2) + fibonacci(n-3)  # Adjust Fibonacci relation
    memo[n] = f
    return f

# Function to draw one "petal" of the pattern
def draw_petal(fib_num):
    """Draw one petal of the symmetrical flower pattern."""
    skk.color(randint(50, 255), randint(50, 255), randint(50, 255))  # Random but somewhat harmonious colors
    for i in range(n):
        skk.forward(fib_num * s)  # Length based on Fibonacci number
        skk.left(360 / n)  # Equal angle turns to maintain symmetry

# Function to draw the full pattern
def draw_pattern():
    """Draw a beautiful and symmetrical pattern."""
    for i in range(10, 30, 2):  # Loop to create a pattern with increasing Fibonacci numbers
        fib_num = fibonacci(i)
        draw_petal(fib_num)  # Draw one petal
        skk.right(360 / 5)  # Rotate to make the pattern symmetrical
    skk.hideturtle()

# Start the drawing
draw_pattern()

# Hide the turtle and finish drawing
turtle.done()

